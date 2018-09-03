# -*- coding: utf8 -*-

import av
import io
import livestreamer
import time
import sys
import cv2
import numpy as np

from io import BytesIO


def overlay_image_alpha(img, img_overlay, pos, alpha_mask):
	"""Overlay img_overlay on top of img at the position specified by
	pos and blend using alpha_mask.

	Alpha mask must contain values within the range [0, 1] and be the
	same size as img_overlay.
	"""

	x, y = pos
	# Image ranges
	y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
	x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

	# Overlay ranges
	y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
	x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

	# Exit if nothing to do
	if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
	    return

	channels = img.shape[2]

	alpha = alpha_mask[y1o:y2o, x1o:x2o]
	alpha_inv = 1.0 - alpha

	for c in range(channels):
	    img[y1:y2, x1:x2, c] = (alpha * img_overlay[y1o:y2o, x1o:x2o, c] +
				alpha_inv * img[y1:y2, x1:x2, c])


def input_stream_read():
	for packet in input.demux(input_streams):
		for frame in packet.decode():
		    frame.pts = None
		    for stream in output_streams:
			    if packet.stream.type == stream.type:
				    if stream.type == "video":
					    img = frame.to_nd_array(format='bgr24')
					    height, width = img.shape[:2]
					    stream.width = width
					    stream.height = height
					    overlay_image_alpha(img, arrows[:, :, 0:3], (0,450), arrows[:, :, 3] / 255.0)
					    frame = av.VideoFrame.from_ndarray(img, format='bgr24')
					    pack = stream.encode(frame)
				    else:
					    pack = stream.encode(frame)
				    if pack:
					    buffer.mux(pack)


def output_stream_write():
	#time.sleep(5)
	while True:
		container = av.open(tmp)
		print (container)
		output.mux(frame)


session = livestreamer.Livestreamer()
session.set_option("http-headers","Client-ID=ewvlchtxgqq88ru9gmfp1gmyt6h2b93")
streams = session.streams("http://www.twitch.tv/kalashz0r")
print (streams)
stream = streams['1080p60']


input = av.open(
		stream.url,
		options={
				'buffer_size':'1000000'
			}
		)

tmp = BytesIO()

buffer = av.open(tmp, 'w', 'mp4')


output = av.open(
    'rtmp://live.restream.io/live/re_882197_78625223222fd0769d68',
    mode='w',
    format='flv'
)


input_streams = list()
output_streams = list()
buffer_streams = list()

arrows = cv2.imread("/root/rama.png", -1)


for stream in input.streams:
    if stream.type == 'video':
	    input_streams += [stream]
	    buffer_streams += [buffer.add_stream('h264',30)]
	    output_streams += [output.add_stream('h264',30)]
	    break

for stream in input.streams:
    if stream.type == 'audio':
	    input_streams += [stream]
	    buffer_streams += [output.add_stream('aac')]
	    output_streams += [output.add_stream('aac')]
	    break

import threading

threading.Thread(target=input_stream_read).start()
#threading.Thread(target=output_stream_write).start()








