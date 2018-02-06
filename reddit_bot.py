import praw
import config
import time
import datetime
import update_html

def bot_login():
	r = praw.Reddit(username = config.username,
		password = config.password,
		client_id = config.client_id,
		client_secret = config.client_secret,
		user_agent = "hkffbjb's url grabber")
	return r

def run_bot(r):
	f = open("all_entries.txt",'r+')
	filetext = f.read()
	new_entries = ""
	for post in r.subreddit('summonerswar').new(limit=10):
		new_discussion = True
		if "Monster Family Discussion" in post.title:
			print('X', end="", flush=True)
			author = post.author
			if not author:
				print("\n\nFound \"" + post.title + "\" by a user with name errors.")
			else:
				print("\n\nFound \"" + post.title + "\" by " + author.name)
				if author.name == "Ellia_Bot":
					monster = post.title[27:]
					print("The discussion is about the \"" + monster + "\"")
					for line in post.selftext.split("\n"):
						if "**Star level**" in line:
							star_levels = line.split("|")
							star_levels = star_levels[1:len(star_levels)-1]
							len_star_text = find_star_text(star_levels[0])
							monster_star_level = 0
							for star_box_text in star_levels:
								star_box_text = star_box_text.strip(" ")
								star_level = int(len(star_box_text)/len_star_text)
								if monster_star_level == 0:
									monster_star_level = star_level
								elif star_level == monster_star_level + 0.5 or star_level == monster_star_level - 0.5:
									continue
								elif monster_star_level != star_level:
									monster_star_level = (star_level + monster_star_level)/2
								else:
									continue
					monster_star_level = str(monster_star_level).strip(".0")
					print("This monster is of star level: " + monster_star_level)
					url = post.url
					print("The url is: " + url + "\n")
					filebyline = filetext.split("\n")
					for line in filebyline:
						data = line.split(",")
						stored_monster = data[0]
						stored_url = data[1]
						if monster == stored_monster and stored_url == url:
							new_discussion = False
					if new_discussion:
						print("Updating logs & commenting")
						new_entries += "\n" + monster + "," + url + "," + monster_star_level
						update_html.update_html(monster,url,monster_star_level,"../Monster_Discussions.html")
		else:
			print('.', end="", flush=True)
	f.write(new_entries)
	f.close()

def find_star_text(text):
	text = text.strip(' ')
	if len(text) > 5:
		length = len(text)
		possible_fits = []
		for num in range(4,-1,-1):
			num += 1
			star_length = int(length/(num))
			star_text = text[0:star_length]
			star_level = 0
			matching = True
			for section in range(num):
				if not star_text == text[star_length*(section):star_length*(section+1)]:
					matching = False
			if matching:
				possible_fits.append(num)
		star_length = int(length/(max(possible_fits)))
		star_text = text[0:star_length]
		return len(star_text)
	else:
		return len(text[0])

j = 1
r = bot_login()
while True:
	if j == 4:
		r = bot_login()
		j = 1
	print("\nChecking", end="", flush=True)
	run_bot(r)
	print(" Done", flush=True)
	j += 1
	time.sleep(300)