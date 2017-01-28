# -*- coding: utf-8 -*-
# Author: Mateusz "Knopers" Knop
import os
import sys
import time
import shelve
import ctypes
from multiprocessing import Process

saveDir = "D:\\Spotlight"
shelveDir = "D:\\Spotlight\Script"

try:
	from PIL import Image
except:
	print("Please install Pillow package")
	exit()

if(sys.platform != "win32"):
	print("It should be ran only on Windows")
	exit()

homeDir = os.environ['userprofile']
spotlightDir = "AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets/"

def show(image):
	image.show()

if __name__ == "__main__":

	db = shelve.open("%s/seen.slv" % (shelveDir))

	spotlightDir = "%s/%s" % (homeDir, spotlightDir)
	files = os.listdir(spotlightDir)
	for img in files:
		if(db.has_key(img)):
			continue

		image = Image.open(spotlightDir + img)
		if (image is None or image.width < image.height):
			continue

		proc = Process(target=show, args=(image,))
		proc.start()

		db[img] = True
		time.sleep(1)

		proc.terminate()

		resp = ctypes.windll.user32.MessageBoxW(0, u"Do you want to save this image?", u"Save this?", 4)
		if(resp == 6):
			image.save("%s/%s.jpg" % (saveDir, img), format='JPEG')

	db.close()
	exit()
