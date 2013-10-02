Welcome to Django Mini Lean!
============================

Summary
-------
Django Mini Lean is a farily minimal, [Django](https://www.djangoproject.com/) based lean split testing framework. (If you're not sure what this all means but you're intrigued by split testing, also known as A/B testing, this is pretty nerdy stuff: Django is a web framework for building custom websites. Django is easy and fun to learn and use, but you definitely need programming skills. If you've already got a site using a different framework or CMS, Django Mini Lean probably isn't so helpful for you. There's lots of other tools you could try first, [Optimizely](https://www.optimizely.com/) and [Google Analytics Content Experiments](https://support.google.com/analytics/answer/1745152?hl=en). If you're curious about split testing in general, try this book: [A/B Testing: The Most Powerful Way to Turn Clicks Into Customers](http://www.amazon.com/Testing-Most-Powerful-Clicks-Customers/dp/1118536096). And above all, read the book that turned me onto this, Eric Ries' [The Lean Startup](http://theleanstartup.com/)!)

If you're into Django and you'd like an easy way to make split testing go, read on and try it out. I hope you will find this helpful!

Try it Out
----------

There's an instance of Django Mini Lean running on heroku, here:

http://django-mini-lean.herokuapp.com/

When you come to the page, one experimental variant is served. If you click reload while on that page, the initial variant stays put via a cookie. If you click to reset, the cookie that saves the variant is smashed and it serves you a new, randomized variants. Variants can be anything; in this demo, we're varying the headline text, the subhead text, and the picture of the cow. It's easy to modify it to test any sorts of variations you'd like; there's a bit of cleverness in loadexperiment() method that automatically generates a matrix for tracking all the options. When someone clicks on a share, a version of the page with a different variant is displayed for the new user. It's possible to keep variants stable through shares as well. (although this is currently turned off: I think it's most helpful for )

Background
----------

From 2010 to October 2012, I led a team that built a wonderful little application called Democracy Dashboard. Based on some early feedback around a slate building tool our users really loved, we tried to turn it into a startup. However, as much as our users loved it, they only loved it for four days every two years. We proceeded to build and test small versions of about a half dozen features over the next year and a half. All of these growth hypotheses failed to produce organic growth or paid growth at a price we thought was likely to be sustainable. The data the app was giving us was outstanding and we thought potentially extremely lucrative; sadly, we just couldn't get enough of it to make the unit economics work.

Despite having lead The Lean Startup halfway through the development process and starting a round of user interviews that was nothing short of mind altering, we hadn't implemented anything for split testing content on our site. The very last experiment we built was around a feature codenamed Democracy With Friends. It was a little Facebook app that went through stuff you've liked and compared it against a database of a couple thousand political pages to see both how generally political you were and whether you leaned left, right or center. We also built a demo of (but did not have time to finish) a little [D3](http://d3js.org/) based network visualizer that was going to show you how your most progressive, most conservative and least political friends were connected.

This stuff was a lot of fun and interesting to build. The concept was a little too complicated to be something that would take off on it's own, but we thought it had a shot at least. To improve those odds we wanted to split test the content and how we described it. I evaluated the various django split testing frameworks, as well as external tools like Optimizely. For various different reasons, none of them quite fit the bill, so I whipped a quick version of this up in a couple of days.

DemDash folded in October 2012. Probably permanently, although the $5B political communications market remains tantalizingly in dire need of massive disruption. But I'd always thought this would be a nice thing to release as open source. Think of it as the daisies growing out of DemDash's tombstone. (and who knows, maybe someday Zombie DemDash will rise again)

One note: this is neither a python module nor a django package; it's more of a demo of a technique. This is deliberate, since it seems like everyone needs A/B testing to do something slightly different. But if anyone has ideas about how to better package it, I'd certainly be open to hearing them.

Future Plans
------------

Move the variants out of the global EXPERIMENTS dictionary in views.py and into a model.

Could possibly be packaged up as either a module or as template context processor.

A nicer reporting page that shows the variants visually would be lovely. (pretty cool how easy the django admin based one was though)

Automatic calculation of statistical significance in the reporting.

Funnel analysis. The deployed version of this did in fact track logins created from the different variants. To implement this, just create another method like fbshare in the view and add the counter to the Experiment. Or you could add a funnel code to that method.


To Run Django Mini Lean Yourself
--------------------------------

Exact steps coming soon, but if you're pretty familiar with running django already, here are the basics.

1. Clone the repository.

2. Set up and register a [Facebook App](https://developers.facebook.com/apps). (or two, if you want to run one live somewhere and one for local development)

3. Plug the FB app ID into an environment variable (make your life easier: put it in your virtual env bin/activate script).

4. Don't forget to add any test users as developers in the app. (otherwise you will get a hopelessly generic error from FB when you try the sharing)

5. Edit the EXPERIMENTS dict in views.py. If you run the local server and load the root at this point, you will get this error: "DoesNotExist at /
Experiment matching query does not exist."

6. You're on the right path now. Go to /loadexperiment and the experiment you set up in the EXPERIMENTS dict will be loaded into the Experiment model.

7. Then go back to / and you should have your own copy up and running!

