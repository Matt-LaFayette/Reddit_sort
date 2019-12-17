def backImgAlt(subscribed):
		sub_list = []
		img = []
		results = []

		test = reddit.redditor('here_comes_ice_king').saved(limit=None)

		# Adds display names to results array
		for post in test:
			results.append(post.subreddit.display_name)

		counter = collections.Counter(results).most_common(10)

		# Adds images to img array
		for x in counter:
			img.append(x[0])
			for x in subscribed:
		 		sub_list.append(x.display_name)

		bkgrnd = []
		imgkv = {}
		altimgkv = {}

		for i in subscribed:
			for x in range (0,len(img)):
			#print (i.display_name + " : " + img[x])
				if img[x] == i.display_name:
					bkgrnd.append(str(i.banner_background_image))
					imgkv[i.display_name] = i.banner_background_image
					altimgkv[i.display_name] = i.community_icon
		print(bkgrnd)
		return bkgrnd, imgkv, altimgkv