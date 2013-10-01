from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.utils import simplejson
import itertools

from random import choice, randrange

from djangominilean.models import Experiment

# Architecture note: as it is now, the experimental variants and generation of the random variant all
# happen here in the view. Eventually this will probably move either to a view decorator or to a custom
# template processor, but as this is primarily a demo of the technique, we're keeping it here now for
# maximum clarity.

CURRENT_EXPERIMENT = 'test1'

# For the purposes of this demo, you can create the tests easily as a dict here. Note that the
# initial label for each set of test variants should correspond to CURRENT_EXPERIMENT.
# Due to the nifty matrix calculation in loadexperiment, any of these can be of any length.
EXPERIMENTS = \
    {
        'test1':
        {
            'titles':
            [
                'Welcome to Django Mini Lean',
                'Try Django Mini Lean',
                'Django Mini Lean Is So Metal'
            ],
            'descriptions': 
            [
                'Django Mini Lean is an open source example of how to easily do split testing.',
                'Want an easy way to do split testing in the django web framework? Give this open source demo a whirl!'
            ],
            'images': 
            [
                'cow1.png',
                'cow2.png'
            ]
        }
    }

# Build the variant data structure
def build_variant(code):
    variant = {}
    for element in code.split('.'):
        print element
    return variant

# This is the main page, with the code for creating the experimental variant, and a code to track that
# that is dropped into a cookie.
def home(request):
    # If there's a testing code in the link, get it, drop it into the session and redirect
    # so no one shares the link with the query string appended. The variant code returned
    # is a string that looks like 0.1.0, where each integer corresponds to a component of the
    # test.
    code = request.GET.get('code', None)
    if code:
        request.session['code'] = code
        print 'home: code in GET, redirecting'
        return HttpResponseRedirect('/')
    # If the code isn't in the query string, try the session...
    else:
        code = request.session.get('code', None)

    # If there's no testing code in the link or in the session,
    # make up a new random code & save it in the session. This
    # should work generally for any given EXPERIMENTS dict.
    # code should be like titles:0.descriptions:1.images:0
    current_exp = EXPERIMENTS[CURRENT_EXPERIMENT]
    if code is None:
        variant_list = []
        # go through each array and pick an index at random
        for element in current_exp:
            element_index = randrange(0, len(current_exp[element]))
            variant_list.append(element + ':' + str(element_index))
        
        variant = str.join('.', variant_list)
        print variant
        code = CURRENT_EXPERIMENT + '-' + variant
        request.session['code'] = code
    else:
        [excode, variant] = code.split('-')
        variants = variant.split('.')
        itext = int(variants[0])
        iimage = int(variants[1])
        idesc = int(variants[2])

    variant = build_variant(code)
#     title = current_exp['titles'][itext]
#     description = current_exp['descriptions'][idesc]
#     img = current_exp['images'][iimage]
    
    exp = Experiment.objects.get(code=CURRENT_EXPERIMENT, variant=variant)
    exp.pageviews += 1
    exp.save()

    return render_to_response('home.html',
            {'title': title, 'description': description, 'img': img, 'code': code,
             'FB_APPID': settings.FB_APPID, 'FB_SECRET': settings.FB_SECRET},
            context_instance=RequestContext(request))

# 
def loadexperiment(request):
    status = None
    current_exp = EXPERIMENTS[CURRENT_EXPERIMENT]
    # Don't create the experiment if it's already in the db.
    existing_experiments = Experiment.objects.filter(code=CURRENT_EXPERIMENT)
    if len(existing_experiments) > 0:
        status = "found experiment ", code, "- not created."
        return HttpResponse(status)
        
    # If it's not found, create rows in Experiment for each possible variant.
    # make an array list of all the options
    # then combinations_with_replacement
    all_variants = []
    for element in current_exp:
        variant_list = current_exp[element]
        for variant in variant_list:
            all_variants.append('%s:%i' % (element, variant_list.index(variant)))
            
    print all_variants

    x = [ 0, 1 ]
    y = [ 0, 1, 2 ]
    z = [ 0, 1]
    m = [ x, y, z]
    for t in itertools.product(*m):
        print t
    print [item for sublist in m for item in sublist]
    
#     num_elements = len(exp)
# 
#     for element in exp:
# 
#     
#     for i in range(0, numvariants):
#         for j in range(0, numvariants):
#         	for k in range(0, numvariants):
# 	            variant = str.join('.', [str(i), str(j), str(k)])
# 	            newexp = Experiment(code=code, variant=variant)
# 	            newexp.save()
    status = "experiment ", code, " loaded"
    
    # Then generate all the posts to FB
    return HttpResponse(status)

def fbshare(request, code):
    success = False
    [excode, variant] = code.split('-')
    exp = Experiment.objects.get(code=excode, variant=variant)
    exp.shares += 1
    exp.save()
    success = True
    results = {'success': success}
    json = simplejson.dumps(results)
    print "fbshare: survived, returning json " + str(json)
    return HttpResponse(json, mimetype='application/json')

def reset(request):
    request.session['code'] = None
    return HttpResponseRedirect('/')
