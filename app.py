from flask import Flask, render_template, g, url_for, request, flash, redirect
#from flask_wtf import Form
import praw, jinja2
import pprint
import sqlite3
import collections
from config import *
from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, BooleanField, SubmitField
#from wtforms.validators import DataRequired
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


pp = pprint.PrettyPrinter(indent=4)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\MGLafayette\\Desktop\\Projects\\Flask\\data.db'
db = SQLAlchemy(app)

class posts(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    link = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(120), unique=True, nullable=False)
    date_added = db.Column(db.String(120), unique=False, nullable=False)
    thread_text = db.Column(db.String(400), unique=True, nullable=False)
    image = db.Column(db.String(400), unique=True, nullable=False)


if __name__ == '__main__':
	app.run(debug=True)

env = jinja2.Environment()
env.globals.update(zip=zip)

def get_users(offset=0, per_page=10):
    return users[offset: offset + per_page]


def get_results(offset=0, per_page=10):
    return results[offset: offset + per_page]


bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'you-will-never-guess'

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=client_secret,
                     username=username,
                     password=password)

test = reddit.redditor('here_comes_ice_king').saved(limit=None)
subscribed = list(reddit.user.subreddits(limit=None))

results = []

for post in test:
	results.append(post.subreddit.display_name)


counter = collections.Counter(results).most_common(10)

name_list = []
value_list = []
desc_list = []
html_list = []
css_list = []

for x,y in counter:
	name_list.append(x)
	value_list.append(y)



for b in name_list:
	desc_list.append(reddit.subreddit(b).public_description)
	html_list.append(reddit.subreddit(b).description_html)
	css_list.append(reddit.subreddit(b).stylesheet())

#prints avail dicts
	#pp.pprint(reddit.redditor('here_comes_ice_king').saved())
#	print("post id: " + str(post))
#	print(vars(post))
#prints all available .title stuff you can pull from post
#	pp.pprint(vars(post))
#needs the .encode or else errors
	#return '{}'.format(array)

categories = ['None', 'Funny', 'Food', 'Gaming', 'Programming', 'Console Hacking', 'Raspberry Pi', 'Security', 'Projects', 'IT']


# from index.html not sure if it makes it faster or slower

reddit = praw.Reddit(client_id=client_id,
                 client_secret=client_secret,
                 user_agent=user_agent,
                 username=username,
                 password=password)
test = reddit.redditor('here_comes_ice_king').saved(limit=None)
subscribed = list(reddit.user.subreddits(limit=None))

sub_list = []
img = []
results = []

for post in test:
	results.append(post.subreddit.display_name)

counter = collections.Counter(results).most_common(10)

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


# end

@app.context_processor
def utility_functions():
    def print_in_console(message):
        print (str(message))

    return dict(mdebug=print_in_console)


@app.context_processor
def inject_user():
    return dict(category=categories)

def posts_all():
	db = get_db()
	cur = db.execute('select id, title, link, category from posts')
	results = cur.fetchall()
	return results

def posts_unsorted():
	db = get_db()
	cur = db.execute('SELECT * FROM posts WHERE category = "None"')  
	results2 = cur.fetchall()
	return results2

def connect_db():
	sql = sqlite3.connect('C:\\Users\\MGLafayette\\Desktop\\Projects\\Flask\\data.db')
	sql.row_factory = sqlite3.Row
	return sql

def get_db():
	if not hasattr(g, 'sqlite3'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def trim_title(title):
	if len(title) > 120:
		return title[0:120] + "..."
	else:
		return title


@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()		

@app.route('/topnav', methods=['GET', 'POST'])
def topnav():
	categories = ['None', 'Funny', 'Food', 'Gaming', 'Programming', 'Console Hacking', 'Raspberry Pi', 'Security', 'Projects', 'IT']
	return render_template('topnav.html')

@app.route('/updateTable', methods=['GET', 'POST'])
def updateTable():
	db = get_db()
	#categories = ['None', 'Funny', 'Food', 'Gaming', 'Programming', 'Console Hacking', 'Raspberry Pi', 'Security', 'Projects', 'IT']
	results = posts_all()
	if request.method == 'POST':
		x = 1
		results = posts_all()
		if request.form['name'] == 'View Tables':
			for post in results:
				db = get_db()
				catx = str(x) + 'cat'
				results = posts_all()
				cat = request.form.get(catx)
				post_title = post['title']
				x = x + 1
				if cat != post['category']:
					db.execute("UPDATE posts SET category = (?) WHERE title = (?);", (cat, post_title))
					db.commit()
			return redirect(url_for('updateTable'))		
	return render_template('updateTable.html', categories=categories, results=results)

@app.route('/updateTableUnsorted', methods=['GET', 'POST'])
def updateTableUnsorted():
	db = get_db()
	
	results2 = posts_unsorted()
	if request.method == 'POST':
		x = 1
		results2 = posts_unsorted()
		if request.form.get('name') == 'View Tables':
			for post in results2:
				db = get_db()
				catx = str(x) + 'cat2'
				results2 = posts_unsorted()
				#print(catx)
				cat = request.form.get(catx)
				#print(cat)
				post_title = post['title']
				#print(post_title)
				x = x + 1
				if cat != post['category']:
					db.execute("UPDATE posts SET category = (?) WHERE title = (?);", (cat, post_title))
					db.commit()
			return redirect(url_for('updateTableUnsorted'))
		
	return render_template('updateTableUnsorted.html', categories=categories, results2=results2)

@app.route('/addRedditInfo', methods=['GET', 'POST'])
def addRedditInfo():
	test = reddit.redditor('here_comes_ice_king').saved(limit=None)
	db = get_db()
	for post in test:
		link = 'https://www.reddit.com' + post.permalink
		title = trim_title(post.title)
		empty = "None"
		date_added = post.created_utc
		thread_text = post.selftext
		image = ""
		if str(post.is_self) == "False":
			try:
				image = (post.preview['images'][0]['source']['url'])
			except:
				print("none provided")
		db.execute('insert or ignore into posts (id, title, link, category, date_added, thread_text, image) values (?, ?, ?, ?, ?, ?, ?)', [str(post), title, link, empty, date_added, thread_text, image])
		print(db.execute('SELECT changes();'))
	db.commit()

	return '''stuff added<br/>
	<button type='button'><a href='http://127.0.0.1:5000/devArea'>Go Back</a></button>
	</br>
	<button type='button'><a href='url_for('viewresults') page_num=1'>View Results</a></button>
	
	'''

@app.route('/test2', methods=['GET', 'POST'])
def test2():
	test = reddit.redditor('here_comes_ice_king').saved(limit=None)
	for post in test:
		link = 'https://www.reddit.com' + post.permalink
		title = trim_title(post.title)
		empty = "None"
		date_added = post.created_utc
		thread_text = post.selftext
		if str(post.is_self) == "False":
			try:
				print(post.preview['images'][0]['source']['url'])
			except:
				print("none provided")
				print(vars(post))
	return "done"

@app.route('/', methods=['GET', 'POST'])
def index():
	env = jinja2.Environment()
	env.globals.update(zip=zip)
	env.globals.update(str=str)
	test = reddit.redditor('here_comes_ice_king').saved(limit=None)
	for x in test:
		pp.pprint(vars(x))
	return render_template('index.html', altimgkv=altimgkv, imgkv=imgkv, bkgrnd=bkgrnd, desc_list=desc_list, name_list=name_list, value_list=value_list, zip=zip, str=str)


@app.route('/createtable')
def createtable():
	db = get_db()
	cur = db.execute('CREATE TABLE IF NOT EXISTS posts (id text primary key unique, title text, link text, category text, date_added int, thread_text TEXT, image text)')
	db.commit()
	return "Table \"Posts\" created<br/><button type='button'><a href='http://127.0.0.1:5000/devArea'>Go Back</a></button>"


@app.route('/droptable')
def droptable():
	db = get_db()
	cur = db.execute('DROP TABLE IF EXISTS posts')
	db.commit()
	return "table dropped<br/><button type='button'><a href='http://127.0.0.1:5000/devArea'>Go Back</a></button>"

@app.route('/viewresults/<int:page_num>/<int:per_page_res>', methods=['GET', 'POST'])
def viewresults(page_num, per_page_res):
	env = jinja2.Environment()
	env.globals.update(zip=zip)
	t3 = posts.query.paginate(per_page=per_page_res, page=page_num, error_out=True)
	return render_template('viewresults.html', zip=zip, t3=t3)

@app.route('/devArea')
def devArea():
	return render_template("devArea.html")

@app.route('/sortby/<int:page_num>/<int:per_page_res>', methods=['GET', 'POST'])
def sortby(page_num, per_page_res):
	sort_cat = request.args.get('sort_cat', None)
	order_by = request.args.get('order_by', None)
	print(sort_cat)
	per_page = per_page_res
	t3 = posts.query.filter_by(category=sort_cat).order_by(order_by).paginate(per_page=per_page_res, page=page_num, error_out=True)
	return render_template("sortby.html", order_by=order_by, t3=t3, per_page=per_page, posts=posts, zip=zip, sort_cat=sort_cat)

@app.route('/deleteposts', methods=['GET', 'POST'])
def deleteposts():
	db = get_db()
	results = posts_all()
	if request.method == 'POST':
		db = get_db()
		results = posts_all()
		x = 1
		for post in results:
			removex = str(x) + 'delete'
			st = str(removex)
			removefield = request.form.get(st)
			post_title = post['id']
			x = x + 1
			if removefield == 'delete':
				print("yes")
				db = get_db()
				db.execute("DELETE FROM posts WHERE id = (?);", [post_title])
				db.commit()
		return redirect(url_for('deleteposts'))
	return render_template("deleteposts.html", results=results)

@app.route('/unfavpost', methods=['GET', 'POST'])
def unfavpost():
	db = get_db()
	results = posts_all()
	if request.method == 'POST':
		db = get_db()
		results = posts_all()
		x = 1
		for post in results:
			removex = str(x) + 'unsub'
			st = str(removex)
			unsub = request.form.get(st)
			post_title = post['title']
			x = x + 1
			test = post['id']
			name = post['title']
			if unsub == 'unsub':
				print(test + " " + name)
				submission = reddit.submission(id=test)
				submission.unsave()
				print ("unsaved")
				db = get_db()
				db.execute("DELETE FROM posts WHERE id = (?);", [test])
				db.commit()
				print ("deleted")
		return redirect(url_for('unfavpost'))
	return render_template("unfavpost.html", results=results)

@app.route('/unfavunsort', methods=['GET', 'POST'])
def unfavunsort():
	db = get_db()
	cur = db.execute('SELECT id, title, link, category FROM posts WHERE category = "None"')
	results = cur.fetchall()
	if request.method == 'POST':
		x = 1
		for post in results:
			removex = str(x) + 'unsub'
			st = str(removex)
			unsub = request.form.get(st)
			post_title = post['title']
			x = x + 1
			test = post['id']
			name = post['title']
			if unsub == 'unsub':
				print(test + " " + name)
				submission = reddit.submission(id=test)
				submission.unsave()
				db = get_db()
				db.execute("DELETE FROM posts WHERE id = (?);", [test])
				db.commit()
				print ("deleted")
		return redirect(url_for('unfavunsort'))
	return render_template("unfavunsort.html", results=results)