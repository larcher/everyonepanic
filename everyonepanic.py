import contextlib
import json
import os
import urllib2
from twilio.rest import TwilioRestClient

# Calls you when your sites go down.
# License is GPLv3.
# Author: Eric Jiang <eric@doublemap.com>

TWILIO_SID = os.environ['TWILIO_SID']
TWILIO_TOKEN = os.environ['TWILIO_TOKEN']
TWILIO_FROM = os.environ['TWILIO_FROM']
CALLEES = os.environ['CALLEES'].split(',')

UPTIME_ROBOT_KEY = os.environ['UPTIME_ROBOT_KEY']
UPTIME_ROBOT = "http://api.uptimerobot.com/getMonitors?apiKey=" + UPTIME_ROBOT_KEY + "&format=json&noJsonCallback=1"

TWILIO_TWIML_ECHO = 'http://twimlets.com/echo?Twiml='

def get_uptime_status():
    with contextlib.closing(urllib2.urlopen(UPTIME_ROBOT)) as ustream:
        resp = json.load(ustream)

    downsites = []

    for m in resp['monitors']['monitor']:
        if m['status'] == "9":  # 9 == "Down", 8 == "Seems down"
            downsites.append(m['friendlyname'])
    return {"total": len(resp['monitors']['monitor']), "down": len(downsites), "downsites": downsites}

def trigger_call(recipients, uptime_status=None):
    if uptime_status is None:
        uptime_status = get_uptime_status()
    client = TwilioRestClient(TWILIO_SID, TWILIO_TOKEN)
    for recp in recipients:
        twiml = downtime_message(uptime_status)
        twimlet_echo_url = TWILIO_TWIML_ECHO + urllib2.quote(twiml)
        call = client.calls.create(url=twimlet_echo_url, to=recp, from_=TWILIO_FROM)


def check_uptimes():
    res = get_uptime_status()
    print "%d sites being monitored\n" % res['total']
    if res['down'] != 0:
        print "Everybody panic!\n"
        for site in res['downsites']:
            print "%s is down.\n" % site
        trigger_call(CALLEES, res)
    else:
        print "Everything seems fine\n"


def downtime_message(uptime_status):
    response = ""
    res = get_uptime_status()
    if res['down'] != 0:
        response = """<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say voice="alice">Everyone panic! %s</Say>
        </Response>""" % " ".join(map(lambda s: ("%s is down." % s.replace("doublemap", "double map")), res['downsites']))
    else:
        response = """<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say voice="alice">False alarm. %d of %d sites are down.</Say>
        </Response>""" % (res['down'], res['total'])
    return response

