# -*- coding: utf-8 -*-
# Author: Mateusz "Knopers" Knop
import os
import sys
import time
import shelve
import ctypes
import shutil
import struct
import subprocess

saveDir = "D:\\Spotlight"
shelveDir = "D:\\Spotlight\Script"

if(sys.platform != "win32"):
	print("It should be ran only on Windows")
	exit()

viewer = os.environ['SystemRoot'] + '\\System32\\rundll32.exe "' + \
			os.environ['ProgramFiles'] + '\\Windows Photo Viewer\\PhotoViewer.dll", ImageView_Fullscreen '

homeDir = os.environ['userprofile']
tempDir = os.environ['tmp']
spotlightDir = "AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets/"

def getDimensions(path):
	jpeg = open(path, 'rb')
	height = -1
	width = -1
	head = jpeg.read(2)
	if(len(head) == 2 and head == '\xFF\xD8'):
		byte = jpeg.read(1)
		try:
			while(byte and ord(byte) != 0xDA):
				while(ord(byte) != 0xFF):
					byte = jpeg.read(1)
				while (ord(byte) == 0xFF):
					byte = jpeg.read(1)
				if (ord(byte) >= 0xC0 and ord(byte) <= 0xC3):
					jpeg.read(3)
					h, w = struct.unpack(">HH", jpeg.read(4))
					break
				else:
					jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
				byte = jpeg.read(1)
			width = int(w)
			height = int(h)
		except Exception:
			pass
	return (width, height)

if __name__ == "__main__":

	db = shelve.open("%s/seena.slv" % (shelveDir))

	spotlightDir = "%s/%s" % (homeDir, spotlightDir)
	files = os.listdir(spotlightDir)
	for img in files:
		if(db.has_key(img)):
			continue

		w, h = getDimensions(spotlightDir + img)
		if(w < h):
			continue

		dest = '%s\\%s.jpg' % (tempDir, img)
		shutil.copy(spotlightDir + img, dest)
		process = subprocess.Popen(viewer + dest)

		db[img] = True
		time.sleep(1)

		resp = ctypes.windll.user32.MessageBoxW(0, u"Do you want to save this image?", u"Save this?", 4)
		if(resp == 6):
			shutil.copy(dest, "%s/%s.jpg" % (saveDir, img))

		os.remove(dest)
		process.terminate()

	db.close()
	exit()
