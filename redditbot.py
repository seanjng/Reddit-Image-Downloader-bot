from imgurpython.helpers.error import ImgurClientError
from imgurpython import ImgurClient
from pprint import pprint
import bot
import json
import praw
import os
import re
import sqlite3
import time
import urllib

# Imgur API client ID
aID = bot.imgurID
# Imgur API client secret
aSecret = bot.imgurSecret
# Reddit bot username
aName = bot.rengeName
# Reddit bot password
aPass = bot.rengePass

# Reddit useragent
aUserAgent = bot.rengeUserAgent

# List of subreddits to pull from
aSublist = bot.sublist
# These are for whenever I'd like to test just one subreddit or a subset of the subreddits
aTestSublist = aSublist[0:23]
aTestSub = aSublist[0]

def createDir(subreddit):
	'''
		Checks to see if a directory for the subreddit exists. If
	it doesn't exist, it creates that directory.
	'''
	if not os.path.exists(os.path.abspath("images/{}/".format(subreddit))):
		os.makedirs(os.path.abspath("images/{}/".format(subreddit)))

def getImgurID(url):
	'''
		Takes a url and strips the domain and file type. Returns a
	valid Imgur image ID
	'''
	imgid = re.sub("(?i)http(s)*://(\w.)*imgur.com/(r/\w*/)*", "", url)
	while "." in imgid:
		imgid = imgid[:-1]
	return imgid

def getImgurAlbumID(url):
	'''
		Takes a url and strips the domain. Returns a valid Imgur
	album ID.
	'''
	albid = re.sub("(?i)http(s)*://(\w.)*imgur.com/(a|gallery)/(r/\w*/)*", "", url)
	while ("#" in albid) | ("?" in albid):
		albid = albid[:-1]
	return albid

def saveImage(client, subreddit, url, reddID):
	'''
		Takes an image id, checks for the file type and creates an
	appropriate savepath. It then checks to see if the image has
	already been saved. If the image has been saved, it skips that
	image.

		In the future, the check will be performed after getImgurID()
	is called in checkIfSaved() in order to conserve API calls and
	prevent rate limiting. It will also be compared against a database
	that contains Reddit submission IDs and Imgur Image/Album IDs in
	order to allow for checking against other subreddit posts since
	usually users will submit an image to more than one subreddit.
	'''
	print("  Image: {}".format(url))
	imgid = getImgurID(url)

	if checkIfSaved(reddID, imgid):
		print("    Saving")
		# Check to see if saving the image returns an error
		try:
			# Determine the save path by image type
			if "jpeg" in client.get_image(imgid).type:
				savepath = os.path.abspath("images/{}/{}.jpg".format(subreddit, imgid))
			elif "png" in client.get_image(imgid).type:
				savepath = os.path.abspath("images/{}/{}.png".format(subreddit, imgid))

			# Check to see if the image has already been saved.
			# If it has, skip that image.
			# I'm going to replace this in the future with a database check
			#	that occurs earlier in the parrent if statement
			if not os.path.exists(os.path.abspath(savepath)):
				urllib.request.urlretrieve(client.get_image(imgid).link, savepath)
				time.sleep(2)
			else:
				print("    just kidding :P")
		except ImgurClientError as e:
			print(e.error_message)
			print(e.status_code)
		# I want to have it send a PM to me here if the error code matches certain things
		else:
			pass
		finally:
			pass
	else:
		print("    Skipping")

def saveAlbum(client, subreddit, url, reddID):
	'''
		Takes post url and gets the album ID. It then iterates
	through the album and calls saveImage().
	'''
	print("  Album: {}".format(url))
	albid = getImgurAlbumID(url)

	print("    Saving")
	for image in client.get_album_images(albid):
		saveImage(client, subreddit, image.link, reddID)

	# this is to prevent rate limits after saving a very large album
	print("  Album done. Sleeping.")
	time.sleep(30)
	

def checkIfSaved(reddID, imgid):
	'''
		Takes a Reddit post ID and Imgur image ID and checks the
	database to see if it's been entered.
	'''
	db = sqlite3.connect("images.db")

	c = db.execute("SELECT * FROM images WHERE imgur = ?", (imgid,))

	if c.fetchone() == None:		# If it's not found in imgur, save
		c = db.execute("SELECT * FROM images WHERE reddit = ?", (reddID,))
		db.execute("insert into images (reddit, imgur) values (?, ?)", (reddID, imgid))
		db.commit()
		db.close()
		return True
	else:							# If it's found in imgur, don't save
		db.close()
		return False

def main():
	# Authentification with Reddit and Imgur
	r = praw.Reddit(aUserAgent)
	client = ImgurClient(aID, aSecret)


	# for sub in aTestSublist:
	for sub in aSublist:
		subreddit = r.get_subreddit(sub)

		createDir(subreddit)

		print("SAVING PICTURES FROM /r/{}".format(sub))

		# Grab the current top 25 posts in subreddit
		for post in subreddit.get_hot():
			if (("/a/" in post.url) | ("/gallery" in post.url)) & ("imgur.com" in post.url):
				saveAlbum(client, subreddit, post.url, post.id)
			elif "imgur.com" in post.url:
				saveImage(client, subreddit, post.url, post.id)
			else:	# This is for non-imgur links
				print("Found non-Imgur link")
				time.sleep(1)

			# For now, just wait 3 seconds bewteen images.
			# Don't want to break the PRAW API rate limit
			time.sleep(1)

		# Wait 2 minute between subreddits
		# time.sleep(60)



if __name__ == "__main__":
	main()