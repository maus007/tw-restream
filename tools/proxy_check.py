import urllib2, socket
import argparse

socket.setdefaulttimeout(20)

# read the list of proxy IPs in proxyList

def is_bad_proxy(pip):    
    try:        
        proxy_handler = urllib2.ProxyHandler({'http': pip})        
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)
        req=urllib2.Request('http://www.google.com')  # change the url address here
        sock=urllib2.urlopen(req)
    except urllib2.HTTPError, e:        
        print 'Error code: ', e.code
        return e.code
    except Exception, detail:

        print "ERROR:", detail
        return 1
    return 0


if __name__ == "__main__":
    	arg_parser = argparse.ArgumentParser(description='Proxy checker')
	arg_parser.add_argument('-r', '--roxy', help="Proxy for test", required=True)
	args = arg_parser.parse_args()
        if is_bad_proxy(args.roxy):
		print {"proxy":args.roxy, "state": "bad"}
        else:
		print {"proxy": args.roxy, "state": "good"}

