def addPosts():
	test = reddit.redditor('here_comes_ice_king').saved(limit=None)
	db = get_db()
	count_list = []
	for post in test:
		link = 'https://www.reddit.com' + post.permalink
		title = trim_title(post.title)
		empty = "None"
		date_added = post.created_utc
		thread_text = post.selftext
		image = ""
		#add_count = add_count + 1
		if str(post.is_self) == "False":
			try:
				image = (post.preview['images'][0]['source']['url'])
			except:
				print("none provided")
		db.execute('insert or ignore into posts (id, title, link, category, date_added, thread_text, image) values (?, ?, ?, ?, ?, ?, ?)', [str(post), title, link, empty, date_added, thread_text, image])
		#count_list.append((str(db.execute('SELECT changes();'))))
		#print(count_list.count())
		chng = db.execute('SELECT changes();')
		for x in chng:
			for y in x:
				if (y == 1):
					count_list.append(db.execute('SELECT changes();'))
		data.a = (len(count_list))
		print (data.a)

	print (count_list)
	db.commit()
	print (data.a)