# 	Run this code the first time you use the bot. It will create a
# database called images.db for you, and initialize a table for storing
# Reddit submissions and Imgur text posts.

import sqlite3
import sys

def makeDB():
	'''
	Creates the database
	'''
	db = sqlite3.connect("images.db")
	db.execute("CREATE TABLE images (reddit text, imgur text)")
	db.close()

def test():
	'''
	Tests to see if the database works
	'''	
	db = sqlite3.connect("images.db")
	# I'll add code later
	db.close()

def reset():
	'''
	Resets the database
	'''
	db = sqlite3.connect("images.db")
	db.execute("DROP TABLE IF EXISTS images")
	db.execute("CREATE TABLE images (reddit text, imgur text)")
	db.close()

def main():
	if len(sys.argv) > 1:
		if sys.argv[1] == "make":
			print("Making database")
			makeDB()
		elif sys.argv[1] == "test":
			test()
		elif sys.argv[1] == "reset":
			reset()
		else:
			print("Invalid argument.")
	else:
		print("Argument required.")
		print("Use 'make' if running for first time")
		print("Use 'test' to test the database")	
		print("Use 'reset' to reset the database")

if __name__ == "__main__": main()