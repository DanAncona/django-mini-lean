Welcome to Django Mini Lean!
============================

World's absolute most minimal django based lean split testing framework.

From 2010 to October 2012, I led a team that built a wonderful little application called Democracy Dashboard. Based on some early feedback around a voting slate grid tool that we built that our users really loved, we tried to turn it into a startup. However, as much as our users loved that part of the tool, they only loved it for four days every two years. We proceeded to build and test small versions of about a half dozen features over the next year and a half. All of these growth hypotheses failed to produce organic growth or paid growth at a price we thought was likely to be sustainable. The data the app was giving us was outstanding and we thought potentially extremely lucrative; sadly, we just couldn't get enough of it to make the unit economics work.

Despite having lead The Lean Startup halfway through the development process and starting a round of user interviews that was nothing short of mind altering, we hadn't implemented anything for split testing content on our site. The very last experiment we built was something we codenamed Democracy With Friends. It was a little Facebook app that went through stuff you've liked and compared it against a database of a couple thousand political pages to see both how generally political you were and whether you leaned left, right or center. We also built a demo of but did not have time to finish a little D3 based network visualizer that was going to show you how your most progressive, most conservative and least political friends were connected.

It was REALLY fun and interesting to build. It was a little complicated to be something that would take off on it's own, but we thought it had a shot at least. To improve those odds we wanted to split test the content and how we described it. We quickly evaluated the various django split testing frameworks out there as well as external tools like Optimizely. For various different reasons, none of them quite fit the bill, so I whipped a quick version of this up in a couple of days.

DemDash folded in October 2012. Probably permanently, although the $5B political communications market remains tantalizingly in dire need of massive disruption. But I'd always thought this would be a nice thing to release as open source. Think of it as the daisies growing out of DemDash's tombstone. (and who knows, maybe someday Zombie DemDash will rise again)

One note: this is neither a python module nor a django package; it's more of a demo of a technique. This is deliberate, since it seems like everyone needs A/B testing to do something slightly different. But if anyone has ideas about how to better package it, I'd certainly be open to hearing them.






Try it here:

http://django-mini-lean.herokuapp.com/

How it works:

If a user is coming in to the raw URL, javascript on the page creates a randomized version.


What it needs:

FB app secret/id into config vars

get sharing loop working & documented

tidy everything up

*** launch ***

Move tests out of the view and into the model

Possibly, to be packaged up as a module

To run:

Clone repo
register an app https://developers.facebook.com/apps
plug the FB secret and app ID into environment variables (make your life easier, put it in your virtual env bin/activate script)

