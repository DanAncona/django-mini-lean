from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings

from random import choice, randrange

from djangominilean.models import Experiment

CURRENT_EXPERIMENT_CODE = 'test1'

# Make sure the titles, descriptions & images arrays have the same number of elements!
# TODO: add checking for this. (and models/admin for it)
EXPERIMENTS = \
    {
        'test1':
        {
            'titles':
            [
                'Welcome to Django Mini Lean',
                'Split Testing Made Easy, for Django'
            ],
            'descriptions': 
            [
                'Django mini lean is an open source example of how to easily do split testing.',
                'This is an example of how to very easily do split testing in the django web framework.'
            ],
            'images': 
            [
                'cow1.png',
                'cow2.png'
            ]
        }
    }

# the randomization happens in the template, so the share text matches but when a new page is created it's random
def home(request):
    # if there's a testing code in the link, get it, drop it into the session and redirect
    # so no one shares the link w/ get foo appended
    code = None
    try:
        code = request.GET['code']
        request.session['code'] = code
        print 'home: code in GET, redirecting'
        return HttpResponseRedirect('/')
    except:
        print 'home: no test code in session or GET'

    # If the code isn't in the query string, try the session...
    if code is None:
        try:
            code = request.session['code']
            print "friendtest: found code in session"
        except:
            print "friendstest: code not in session"

    # if there's no testing code in the link or in the session,
    # make up a new random code & save it in the session
    exp = EXPERIMENTS[CURRENT_EXPERIMENT_CODE]
    print code
    if code is None:
        images = exp['images']
        titles = exp['titles']
        itext = randrange(0, len(titles))
        iimage = randrange(0, len(images))
        excode = CURRENT_EXPERIMENT_CODE
        variant = str.join('.', [str(itext), str(iimage)])
        code = excode + '-' + variant
        request.session['code'] = code
    else:
        [excode, variant] = code.split('-')
        variants = variant.split('.')
        itext = int(variants[0])
        iimage = int(variants[1])

    title = exp['titles'][itext]
    description = exp['descriptions'][itext]
    img = exp['images'][iimage]
    print title, description, img
    
    exp = Experiment.objects.get(code=CURRENT_EXPERIMENT_CODE, variant=variant)
    exp.pageviews += 1
    exp.save()

    return render_to_response('home.html',
            {'title': title, 'description': description, 'img': img, 'code': code,
             'FB_APPID': settings.FB_APPID, 'FB_SECRET': settings.FB_SECRET},
            context_instance=RequestContext(request))

def loadexperiment(request):
    status = None
    code = 'test1'
    exp = EXPERIMENTS[code]
    # don't create the experiment if it's already in the db
    existing_experiments = Experiment.objects.filter(code=code)
    if len(existing_experiments) > 0:
        status = "found experiment ", code, "- not created."
        return HttpResponse(status)
        
    # if it's not found, create rows in Experiment for each variant
    numvariants = len(exp['titles'])
    for i in range(0, numvariants):
        for j in range(0, numvariants):
            variant = str.join('.', [str(i), str(j)])
            newexp = Experiment(code=code, variant=variant)
            newexp.save()
    status = "experiment ", code, " loaded"
    # then generate all the posts to FB
    return HttpResponse(status)

def fbshare(request, code):
    success = False
    [excode, variant] = code.split('-')
    exp = Experiment.objects.get(excode=excode, variant=variant)
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
