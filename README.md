Everyone Panic!
===============

This is an easy way to set up a monitoring system that calls your phone number
if any of your websites go down. It uses Uptime Robot for continual
monitoring and Twilio for voice calls. You can set it up to call multiple
phone numbers as well.

It's almost free! You will have to pay for each voice call at the Twilio voice
rate ($0.02 per call per callee in the USA).

It should be easy to set up as a cronjob on a server that runs Python and talks
to the Internet.  Obviously, you should use a hosting platform that isn't also
used for your sites. If you want something that can run on AppEngine or
Heroku, see the [original project](https://github.com/doublemap/everyonepanic).

This script uses [the Echo Twimlet from Twilio Labs](https://www.twilio.com/labs/twimlets/echo) to provide a TwiML endpoint for the Twilio API to use. This allows Everyone Panic to run as a standalone script instead of a web app.

It's the closest thing we've had to a "set it and forget it" service, since we
don't need to touch it in order to add additional sites in Uptime Robot. This
app has been dutifully watchful for us ever since we whipped it up one day,
and since our automated monitoring has grown a lot more since then, we figured
that it was time to release it into the wild.


Configuration
-------------

You need to set a few different environment variables:

* `TWILIO_SID` - find this in your Twilio account
* `TWILIO_TOKEN` - also find this in your Twilio account
* `TWILIO_FROM` - a Twilio purchased or validated phone number
* `CALLEES` - a comma separated list of phone numbers:
`+15551111111,+15552222222`
* `UPTIME_ROBOT_KEY` - your Uptime Robot account's API key

Setup
-----

 * `git clone`
 * `cd everyonepanic`
 * `mkvirtualenv everyonepanic -r requirements.txt`
 * ...

Cron job
--------

...

