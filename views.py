EXPERIMENT = 'friends1'
MSGS    = [
        "Dan scored 255 and 86% progressive. Curious to see how political you are on Facebook?",
        "Dan just saw how his most conservative, most progressive and least political friends are connected. Curious to see yours?"
        ]
DESCS   = [
        "See your score and how you compare with friends.",
        "Your most progressive, most conservative and least political friends -- and how they are connected."
        ]
IMAGES  = [
        "friendstest-d3.png",
        "friendstest-nodexl.png"
        ]

def friendstest(request):
    nums = {}
    head = None
    subhead = None
    msg = None
    ideology = None
    img = None
    graph = None
    fb_user = None

    user = request.user
    fb_user = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET_KEY)
    if fb_user == None:
        fb_user = new_get_user_from_cookie(request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET_KEY)
    if fb_user == None or fb_user['access_token'] == None:
        pass
#         auth.logout(request)
#         return render_to_response('friendstest.html', {'msg': 'login failed'},
#                 context_instance=RequestContext(request))
########
###
#     createexperimentrows()
###
########

    # if there's a testing code in the link, get it, drop it into the session and redirect
    # so no one shares the link w/ get foo appended
    code = None
    try:
        code = request.GET['code']
        request.session['code'] = code
        deb('friendstest: code in GET, redirecting')
        return HttpResponseRedirect('/friends')
    except:
        deb('friendstest: no test code in session or GET')

    # if not in the GET, try the session...
    if code is None:
        try:
            code = request.session['code']
            deb("friendtest: found code in session")
        except:
            deb("friendstest: code not in session")

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
    exp = Experiment.objects.get(excode=excode, variant=variant)
    exp.pageviews += 1
    exp.save()
    mod = PoliticalThingSummary.objects.filter(ideology='mod').latest()
    con = PoliticalThingSummary.objects.filter(ideology='con').latest()
    pro = PoliticalThingSummary.objects.filter(ideology='pro').latest()
    summary = {'pro': pro, 'con': con, 'mod': mod}


    return render_to_response('friendstest.html', {'head': head, 'subhead': subhead, 'msg': msg, 'img': img, 'code': code, 'summary': summary, 'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID},
            context_instance=RequestContext(request))

def createexperimentrows():
    # first create rows in Experiment for each variant
    for i in range(0,2):
        for j in range(0,2):
            variant = str.join('.', [str(i), str(j)])
            newexp = Experiment(excode=EXPERIMENT, variant=variant)
            newexp.save()
    # then generate all the posts to FB
    return

def fbshare(request, code):
    success = False
    [excode, variant] = code.split('-')
    exp = Experiment.objects.get(excode=excode, variant=variant)
    exp.shares += 1
    exp.save()
    success = True
    results = {'success': success}
    json = simplejson.dumps(results)
    deb("fbshare: survived, returning json " + str(json))
    return HttpResponse(json, mimetype='application/json')

