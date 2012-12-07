from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from random import choice, randrange

from djangominilean.models import Experiment

EXPERIMENTS = \
    {
        'test1':
        {
            'titles':
            {
            'The most interesting thing on the internet!',
            'The least interesting thing on the internet!'
            },
            'descriptions': 
            {
            'This is a cow. Curious? Click the button.',
            'This is a cow. Click the button to share.'
            },
            'images': 
            {
            'cow1.png',
            'cow2.png'
            }
        }
    }

def home(request):
    nums = {}
    head = None
    subhead = None
    msg = None
    ideology = None
    img = None
    graph = None
    fb_user = None

    # if there's a testing code in the link, get it, drop it into the session and redirect
    # so no one shares the link w/ get foo appended
    code = None
    try:
        code = request.GET['code']
        request.session['code'] = code
        print 'friendstest: code in GET, redirecting'
        return HttpResponseRedirect('/friends')
    except:
        print 'friendstest: no test code in session or GET'

    # if not in the GET, try the session...
    if code is None:
        try:
            code = request.session['code']
            print "friendtest: found code in session"
        except:
            print "friendstest: code not in session"

    # if there's no testing code in the link or in the session, make up a new random code & save it in the session
    if code is None:
        isubhead = randrange(0, len(DESCS))
        iimage = randrange(0, len(IMAGES))
        #testcode = str(ihead) + str(isubhead) + str(imsg) + str(iideo) + str(iimage)
        code = EXPERIMENT + '-' + str.join('.', [str(isubhead), str(iimage)])
        request.session['code'] = code
        
#         head = heads[ihead]
#         subhead = subheads[isubhead]
#         msg = msgs[imsg]
#         img = images[iimage]
#         icon = icons[iimage]

    [excode, variant] = code.split('-')
    variants = variant.split('.')
    vcopy = int(variants[0])
    vimage = int(variants[1])
    
    subhead = DESCS[vcopy]
    img = IMAGES[vimage]
    exp = Experiment.objects.get(experiment_code=excode, variant=variant)
    exp.pageviews += 1
    exp.save()

    return render_to_response('home.html', {'head': head, 'subhead': subhead, 'msg': msg, 'img': img, 'code': code},
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
    return
