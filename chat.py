# -*- coding: utf-8 -*-

import socket
import time
import sys
from bot import *

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "genius_fortnite_player"
PASS = 'oauth:a1zwujz3psgt8cqrdfiqhpi91x9fgh'
CHANNEL = "pe4enko"

def send_message(msg):
    s.send(bytes("PRIVMSG #" + CHANNEL + " :" + msg + "\r\n"))
    print("ANS: " + msg)

s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n"))
s.send(bytes("NICK " + NICK + "\r\n"))
s.send(bytes("JOIN #" + CHANNEL + " \r\n"))

while True:
    ans = ""
    user = NICK
    response = s.recv(1024).decode('utf-8')
    resp = response.split(":")
    try:
	msg = resp[2]
        user = resp[1].split("!")[0].encode("utf-8")
	print ("RESP:" + msg)
    except:
	pass
    if NICK not in user:
	ans = textMessage(msg)
    time.sleep(1)
    if ans:
        send_message(ans.encode("utf-8"))


