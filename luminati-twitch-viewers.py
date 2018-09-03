'''
Copyright 2015 ohyou

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import requests
import subprocess
import json
import sys
import multiprocessing
import time
import random
import six
from six.moves.urllib import request

channel_url = "twitch.tv/"
processes = []

username = 'lum-customer-hl_cad12176-zone-static'
password = 'rp6pe9i0kkrv'
port = 22225

def get_channel():
    # Reading the channel name - passed as an argument to this script
    if len(sys.argv) >= 2:
        global channel_url
        channel_url += sys.argv[1]
    else:
        print "An error has occurred while trying to read arguments. Did you specify the channel?"
        sys.exit(1)


def get_url():
    # Getting the json with all data regarding the stream
    try:
        response = subprocess.Popen(
            ["livestreamer", "--http-header", "Client-ID=ewvlchtxgqq88ru9gmfp1gmyt6h2b93",
            channel_url, "-j","--yes-run-as-root"], stdout=subprocess.PIPE).communicate()[0]
    except subprocess.CalledProcessError:
        print "An error has occurred while trying to get the stream data. Is the channel online? Is the channel name correct?"
        sys.exit(1)
    except OSError:
        print "An error has occurred while trying to use livestreamer package. Is it installed? Do you have Python in your PATH variable?"

    # Decoding the url to the worst quality of the stream
    try:
        url = json.loads(response)['streams']['audio_only']['url']
    except:
        try:
            url = json.loads(response)['streams']['worst']['url']
        except (ValueError, KeyError):
            print "An error has occurred while trying to get the stream data. Is the channel online? Is the channel name correct?"
            sys.exit(1)

    return url


def open_url(url,session_id):
    # Sending HEAD requests
    while True:
        try:
	    super_proxy_url = ('http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' %
        (username, session_id, password, port))
	    proxy_handler = request.ProxyHandler({
    	    'http': super_proxy_url,
    	    'https': super_proxy_url,
	    })
	    opener = request.build_opener(proxy_handler)
	    print('Performing request')
	    r = opener.open(r'http://jsonip.com').read()
	    ip = json.loads(r)['ip']
	    print 'Your IP is', ip
	    rss = opener.open(url)
	    print rss
            print "Sent HEAD request"
            time.sleep(10)
        except Exception, e:
            print e


def prepare_processes():
    global processes
    i = 0
    n = 100

    while i < n:
        # Preparing the process and giving it its own proxy
        processes.append(
            multiprocessing.Process(
                target=open_url, kwargs={
                    "url": get_url(),
		    "session_id": random.random()
	    }))

        print '.',
	i += 1

    print ''

if __name__ == "__main__":
    print "Obtaining the channel..."
    get_channel()
    print "Obtained the channel"
    print "Preparing the processes..."
    prepare_processes()
    print "Prepared the processes"
    print "Booting up the processes..."

    # Timer multiplier
    n = 1

    # Starting up the processes
    for process in processes:
        time.sleep(random.randint(1, 5) * n)
        process.daemon = True
        process.start()
        if n > 1:
            n -= 1

    # Running infinitely
    while True:
        time.sleep(1)

