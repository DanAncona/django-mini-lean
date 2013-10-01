Welcome to Django Mini Lean!
============================

Summary
-------
Django Mini Lean is a farily minimal, django-based lean split testing (sometimes called A/B testing) framework. This is pretty nerdy stuff: Django is a web framework that people use to build custom websites. Django is easy and fun to learn and use, but you definitely need programming skills. If you've already got a site using a different framework or CMS, Django Mini Lean probably isn't so helpful for you. There's lots of other tools you could try first, [Optimizely](https://www.optimizely.com/) and [Google Analytics Content Experiments](https://support.google.com/analytics/answer/1745152?hl=en).

If you're curious about split testing in general, try [A/B Testing: The Most Powerful Way to Turn Clicks Into Customers](http://www.amazon.com/Testing-Most-Powerful-Clicks-Customers/dp/1118536096).

Try it Out
----------

There's an instance of Django Mini Lean running on heroku, here:

http://django-mini-lean.herokuapp.com/

When you come to the page, one experimental variant is served, and if you reload that variant stays put via a cookie. If you click to reset, the cookie that saves the variant is smashed and it serves you a new one. Variants can be anything; in this demo, we're varying the headline text, the subhead text, the text above the cow and the picture of the cow. It's easy to modify it to test any sorts of variations you'd like. When someone clicks on a share, a version of the page with a different variant is displayed for the new user.

Background
----------

From 2010 to October 2012, I led a team that built a wonderful little application called Democracy Dashboard. Based on some early feedback around a voting slate grid tool that we built that our users really loved, we tried to turn it into a startup. However, as much as our users loved that part of the tool, they only loved it for four days every two years. We proceeded to build and test small versions of about a half dozen features over the next year and a half. All of these growth hypotheses failed to produce organic growth or paid growth at a price we thought was likely to be sustainable. The data the app was giving us was outstanding and we thought potentially extremely lucrative; sadly, we just couldn't get enough of it to make the unit economics work.

Despite having lead The Lean Startup halfway through the development process and starting a round of user interviews that was nothing short of mind altering, we hadn't implemented anything for split testing content on our site. The very last experiment we built was something we codenamed Democracy With Friends. It was a little Facebook app that went through stuff you've liked and compared it against a database of a couple thousand political pages to see both how generally political you were and whether you leaned left, right or center. We also built a demo of but did not have time to finish a little D3 based network visualizer that was going to show you how your most progressive, most conservative and least political friends were connected.

It was REALLY fun and interesting to build. It was a little complicated to be something that would take off on it's own, but we thought it had a shot at least. To improve those odds we wanted to split test the content and how we described it. We quickly evaluated the various django split testing frameworks out there as well as external tools like Optimizely. For various different reasons, none of them quite fit the bill, so I whipped a quick version of this up in a couple of days.

DemDash folded in October 2012. Probably permanently, although the $5B political communications market remains tantalizingly in dire need of massive disruption. But I'd always thought this would be a nice thing to release as open source. Think of it as the daisies growing out of DemDash's tombstone. (and who knows, maybe someday Zombie DemDash will rise again)

One note: this is neither a python module nor a django package; it's more of a demo of a technique. This is deliberate, since it seems like everyone needs A/B testing to do something slightly different. But if anyone has ideas about how to better package it, I'd certainly be open to hearing them.

Future Plans
------------

Move tests out of the view and into a model

Could possibly be packaged up as either a module, or as template processor.

A nicer reporting page, showing the variants visually, would be lovely. I'd also like to get into including statistical significance analysis.

Funnel analysis isn't hard to add. The deployed version of this did that to track logins created from the different variants. To implement this, just create another method like fbshare in the view and add the counter to the Experiment. Or you could add a funnel code to that method.


To Run Django Mini Lean Yourself
--------------------------------

Clone the repo

Set up and register a FB app via https://developers.facebook.com/apps

Plug the FB app ID into an environment variables (make your life easier, put it in your virtual env bin/activate script)

Don't forget to add any test users as developers in the app (otherwise you will get a hopelessly generic error from FB when you try the sharing)

Next, edit the EXPERIMENTS dict in views.py - if you run the local server and load the root at this point, you will get this error:

'''
"DoesNotExist at /
Experiment matching query does not exist."
'''

You're on the right path now. Just go to /loadexperiment and the experiment you set up in the EXPERIMENTS dict will be loaded into the Experiment model

Then go back to / and you should have your own copy up and running!

