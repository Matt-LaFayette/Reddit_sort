def get_img(subscribed):
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
		 		
		imgkv = {}

		or i in subscribed:
			for x in range (0,len(img)):
				if img[x] == i.display_name:
					imgkv[i.display_name] = i.banner_background_image