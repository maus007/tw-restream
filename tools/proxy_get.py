import proxy_check
import requests

roxy = requests.get("https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt")
proxys = roxy.text.split("\n")
for proxy in proxys:
	#print "Start checking proxy: "+ str(proxy.split(" ")[0])
	if proxy_check.is_bad_proxy(proxy.split(" ")[0]):
		pass
	else:
		print str(proxy.split(" ")[0])
