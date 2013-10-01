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
# template processor, but as this is primarily a demo of the technique, we're keeping it all here now
# for maximum clarity.

CURRENT_EXPERIMENT = 'test1'

# For the purposes of this demo, you can create the tests easily as a dict here. Note that the
# initial label for each set of test variants should correspond to CURRENT_EXPERIMENT.
# Due to the nifty matrix calculation in loadexperiment, any of these can be of any length.
EXPERIMENTS = \
    {
        'test1':
        {
            'title':
            [
                'Welcome to Django Mini Lean',
                'Try Django Mini Lean',
                'Django Mini Lean Is So Metal'
            ],
            'description': 
            [
                'Django Mini Lean is an open source example of how to easily do split testing.',
                'Want an easy way to do split testing in the django web framework? Give this open source demo a whirl!'
            ],
            'img': 
            [
                'cow1.png',
                'cow2.png'
            ],
            'cowtext':
            [
                'Please, enjoy this cow, and click the button below to share this on Facebook.',
                'Please click the button below to share this on Facebook.'
            ]
        }
    }

# Build the variant data structure
def build_variant(code):
    variant = {}
    [exp_code, variant_str] = code.split('-')
    variants = variant_str.split('.')
    for element in variants:
        [var_label, var_index] = element.split(':')
        print var_label, var_index
        variant[var_label] = EXPERIMENTS[CURRENT_EXPERIMENT][var_label][int(var_index)]
    print variant
    return variant

# This is the main page, with the code for creating the experimental variant, and a code to track that
# that is dropped into a cookie.
def home(request):
    # If there's a testing code in the link, get it, drop it into the session and redirect
    # so no one shares the link with the query string appended.
    variant_code_with_exp = request.GET.get('code', None)
    if variant_code_with_exp:
        request.session['code'] = variant_code_with_exp
        return HttpResponseRedirect('/')
    # If the code isn't in the query string, try the session...
    else:
        variant_code_with_exp = request.session.get('code', None)

    # If there's no testing code in the link or in the session,
    # make up a new random code & save it in the session. This
    # should work generally for any given EXPERIMENTS dict.
    # The code format is element_label:element_index,
    # i.e. titles:0.descriptions:1.images:0
    current_exp = EXPERIMENTS[CURRENT_EXPERIMENT]
    if variant_code_with_exp is None:
        variant_list = []
        # Go through each array and pick an index at random.
        for element in current_exp:
            element_index = randrange(0, len(current_exp[element]))
            variant_list.append(element + ':' + str(element_index))

        variant_code = str.join('.', variant_list)
        variant_code_with_exp = CURRENT_EXPERIMENT + '-' + variant_code
        request.session['code'] = variant_code_with_exp
    else:
        [exp_code, variant_code] = variant_code_with_exp.split('-')
        
    print variant_code, variant_code_with_exp
    # Now we definitely have our variant code, so build out the dictionary to hand off to the template.
    variant_details = build_variant(variant_code_with_exp)
    print variant_details

    # And increment the pageviews for this variant.
    exp = Experiment.objects.get(code=CURRENT_EXPERIMENT, variant=variant_code)
    exp.pageviews += 1
    exp.save()

    return render_to_response('home.html',
            {'variant_details': variant_details, 'code': variant_code_with_exp,
             'FB_APPID': settings.FB_APPID, 'FB_SECRET': settings.FB_SECRET},
            context_instance=RequestContext(request))

# If the the rows for the Experiment aren't found in the db, calculate all the combinations
# of the current experiment matrix via Cartesian product. Python's itertools makes this easy.
def loadexperiment(request):
    status = ''
    current_exp = EXPERIMENTS[CURRENT_EXPERIMENT]

    # Don't create the experiment if it's already in the db.
    existing_experiments = Experiment.objects.filter(code=CURRENT_EXPERIMENT)
    if len(existing_experiments) > 0:
        status = "found experiment ", CURRENT_EXPERIMENT, "- not created."
        return HttpResponse(status)
        
    # If it's not found, create rows in Experiment for each possible variant.
    # Make a list of all the options, with each array in element:index form.
    variant_matrix = []
    for element in current_exp:
        variant_list = current_exp[element]
        for i, item in enumerate(variant_list):
            variant_list[i] = '%s:%i' % (element, i)
        variant_matrix.append(variant_list)

    # The Cartesian product of the matrix gives us all possible variants.
    for t in itertools.product(*variant_matrix):
        variant = str.join('.', list(t))
        newexp = Experiment(code=CURRENT_EXPERIMENT, variant=variant)
        newexp.save()
        status += 'variant %s saved<br/>' % (variant)
        
    status += '<br/><br/>experiment ' + CURRENT_EXPERIMENT + ' loaded successfully.'

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
