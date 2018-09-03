# -*- coding: utf-8 -*-

import socket
import time
import sys
from bot import *

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "genius_fortnite_player"
PASS = 'oauth:a1zwujz3psgt8cqrdfiqhpi91x9fgh'
CHANNEL = "meelluje"

def send_message(msg):
    s.send(bytes("PRIVMSG #" + CHANNEL + " :" + msg + "\r\n"))
    print("ANS: " + msg)

s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n"))
s.send(bytes("NICK " + NICK + "\r\n"))
s.send(bytes("JOIN #" + CHANNEL + " \r\n"))

send_message("Что с звуком?")