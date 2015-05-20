# Image Downloader Bot

This is a Reddit bot that I'm working on that downloads images from various subreddits. I'm currently learning Python, and thought this would be a fun project to work on, especially because I have a minor (not really) wallpaper addiction.

This bot was written in Python 3.4.

## Installation

1. `git clone http://github.com/hizinfiz/Reddit-Image-Downloader-Bot.git`
1. Install `sqlite3`, `PRAW`, and `ImgurClient` using pip.
1. Register an [Imgur Client](https://api.imgur.com/oauth2/addclient).  
Under "Authorization Type", you can select "OAuth 2 authorization without a callback URL". I'm including this because when I first did it, I had to Google to find out which one I should choose.
1. Create `bot.py` in your Python directory. This allows you to privately store your Imgur client ID, secret, and bot login credentials without worrying about it getting out online. I also use `bot.py` (for now) to store the list of subreddits I'd like my bot to download wallpapers from.   
 The directory on OS X is:
`/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4`  
I've included `sample_bot.py` as an example of what to do.
1. Come up with a list of subreddits you'd like to grab images from. I included the subreddits I'm checking in `sample_bot.py`.

## Running the bot

For now, the bot doesn't currently log in to Reddit, it just runs via the command line. I'm planning to add logging in in the future, that way I can communicate with the bot without having to access it via the command line.

Before starting the bot, you should run `initializeDatabase.py make`. This will initialize the database that keeps track of what images you've saved already.

If at any time you want to reset the database, `initializeDatabase.py reset` will do that for you.

Then, you can run `RedditBot.py` and it'll get on its way!

## Current Functionality

1. Save the top 25 posts from each subreddit you've specified. It will only look at Imgur posts, everything else will be ignored. If a user decides to link to their Imgur profile page, it'll ignore that as well.
2. Keep a log of each image saved so that you don't end up with duplicates.  
This works across subreddits as well because I find that people like to submit their wallpapers to multiple subreddits at the same time.  
However, it won't detect reuploads of the same image, so unfortunately you're out of luck there. I believe there's software available that can do that for you so why bother making my own.
3. On the first run, it'll make a directory named `Images` for you. The first time you save images from a subreddit, it'll make a directory for that subreddit in `Images`.
4. It also likes to crap out if you save images too quickly because of the Imgur API rate limit, that's something I'll fix in the next few days when I have time. For now, I just made it take short breaks after each save and long breaks after each album. I would recommend skipping /r/wallpaperdump because it doesn't like that subreddit very much.

## Planned Functionality

1. Actually log into Reddit and automatically save from /hot once per day.
2. Fix the Imgur API rate limit issue.
3. Save from other image sources. Planned includes iminus, awwnime, and deviantart. This is mostly based on whatever I'm most interested in saving from, I'm not planning on hitting every single major image hosting service.
4. Accept requests via Reddit PM
	- Add/Remove subreddit (probably going to have to move the subreddit list over to the database rather than keep it in bot.py)
	- Save Top - All Time, Past Year, Past Month, Past Week & specify how many to save (default = 100)
5. If I give it an image ID, tell me the Reddit post
6. Tell me if I incorrectly added a subreddit.
7. Ignore images below a certain resolution because nobody wants low res wallpapers.
8. Sort based on resolution into desktop and mobile wallpapers