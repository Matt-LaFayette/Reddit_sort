from flask import Flask, render_template, g, url_for, request, flash, redirect
#from flask_wtf import Form
import praw, jinja2
import pprint
import sqlite3
import collections
from config import *
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, BooleanField, SubmitField
#from wtforms.validators import DataRequired

pp = pprint.PrettyPrinter(indent=4)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=client_secret,
                     username=username,
                     password=password)
test = reddit.redditor('here_comes_ice_king').saved(limit=None)
subscribed = list(reddit.user.subreddits(limit=None))



#prints avail dicts
	#pp.pprint(reddit.redditor('here_comes_ice_king').saved())
#	print("post id: " + str(post))
#	print(vars(post))
#prints all available .title stuff you can pull from post
#	pp.pprint(vars(post))
#needs the .encode or else errors
	#return '{}'.format(array)

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

if __name__ == '__main__':
	app.run(debug=True)


@app.route('/updateTable', methods=['GET', 'POST'])
def updateTable():
	db = get_db()
	categories = ['None', 'Funny', 'Food', 'Gaming', 'Programming', 'Console Hacking', 'Raspberry Pi', 'Security', 'Projects', 'IT']
	results = posts_all()
	if request.method == 'POST':
		x = 1
		results = posts_all()
		if request.form['name'] == 'View Tables':
			for post in results:
				db = get_db()
				catx = str(x) + 'cat'
				results = posts_all()
				cat = request.form[catx]
				#print(cat)
				post_title = post['title']
				#print(post_title)
				x = x + 1
				if cat != post['category']:
					db.execute("UPDATE posts SET category = (?) WHERE title = (?);", (cat, post_title))
					db.commit()
			return redirect(url_for('updateTable'))		
	return render_template('updateTable.html', categories=categories, results=results)

@app.route('/updateTableUnsorted', methods=['GET', 'POST'])
def updateTableUnsorted():
	db = get_db()
	categories = ['None', 'Funny', 'Food', 'Gaming', 'Programming', 'Console Hacking', 'Raspberry Pi', 'Security', 'Projects', 'IT']
	results2 = posts_unsorted()
	if request.method == 'POST':
		x = 1
		results2 = posts_unsorted()
		if request.form['name'] == 'View Tables':
			for post in results2:
				db = get_db()
				catx = str(x) + 'cat2'
				results2 = posts_unsorted()
				cat = request.form[catx]
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
	reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)
	test = reddit.redditor('here_comes_ice_king').saved(limit=None)
	db = get_db()
	for post in test:
		link = 'https://www.reddit.com' + post.permalink
		title = trim_title(post.title)
		empty = "None"
		db.execute('insert or ignore into posts (id, title, link, category) values (?, ?, ?, ?)', [str(post), title, link, empty])
	db.commit()
	return '''stuff added<br/>
	<button type='button'><a href='http://127.0.0.1:5000/devArea'>Go Back</a></button>
	</br>
	<button type='button'><a href='http://127.0.0.1:5000/viewresults'>View Results</a></button>
	'''

@app.route('/', methods=['GET', 'POST'])
def index():
	env = jinja2.Environment()
	env.globals.update(zip=zip)
	env.globals.update(str=str)

	reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)
	test = reddit.redditor('here_comes_ice_king').saved(limit=None)
	
	results = []

	for post in test:
		results.append(post.subreddit.display_name)

	counter = collections.Counter(results).most_common(10)

	name_list = []
	value_list = []

	for x,y in counter:
		name_list.append(x)
		value_list.append(y)
		
	return render_template('index.html', name_list=name_list, value_list=value_list, zip=zip, str=str)


@app.route('/birthdays')
def birthdays():
	return render_template("birthdays.html", test=test)

@app.route('/createtable')
def createtable():
	db = get_db()
	cur = db.execute('CREATE TABLE IF NOT EXISTS posts (id text primary key unique, title text, link text, category text)')
	db.commit()
	return "Table \"Posts\" created<br/><button type='button'><a href='http://127.0.0.1:5000/devArea'>Go Back</a></button>"


@app.route('/droptable')
def droptable():
	db = get_db()
	cur = db.execute('DROP TABLE IF EXISTS posts')
	db.commit()
	return "table dropped<br/><button type='button'><a href='http://127.0.0.1:5000/devArea'>Go Back</a></button>"

@app.route('/viewresults', methods=['GET', 'POST'])
def viewresults():
	db = get_db()
	cur = db.execute('select id, title, link, category from posts')
	results = cur.fetchall()
	print('Table exists.')
	return render_template("viewresults.html", results=results)


@app.route('/devArea')
def devArea():
	return render_template("devArea.html")


@app.route('/sortbyfood', methods=['GET', 'POST'])
def sortbyfood():
	db = get_db()
	cur = db.execute('SELECT id, title, link, category FROM posts WHERE category = "Food"')
	results = cur.fetchall()
	return render_template("sortbyfood.html", results=results)

@app.route('/sortbygaming', methods=['GET', 'POST'])
def sortbygaming():
	db = get_db()
	cur = db.execute('SELECT id, title, link, category FROM posts WHERE category = "Gaming"')
	results = cur.fetchall()
	return render_template("sortbygaming.html", results=results)

@app.route('/sortbyfunny', methods=['GET', 'POST'])
def sortbyfunny():
	db = get_db()
	cur = db.execute('SELECT id, title, link, category FROM posts WHERE category = "Funny"')
	results = cur.fetchall()
	return render_template("sortbyfunny.html", results=results)

@app.route('/sortbyprogramming', methods=['GET', 'POST'])
def sortbyprogramming():
	db = get_db()
	cur = db.execute('SELECT id, title, link, category FROM posts WHERE category = "Programming"')
	results = cur.fetchall()
	return render_template("sortbyprogramming.html", results=results)

@app.route('/sortbyconsolehacking', methods=['GET', 'POST'])
def sortbyconsolehacking():
	db = get_db()
	cur = db.execute('SELECT id, title, link, category FROM posts WHERE category = "Console Hacking"')
	results = cur.fetchall()
	return render_template("sortbyconsolehacking.html", results=results)

@app.route('/deleteposts', methods=['GET', 'POST'])
def deleteposts():
	db = get_db()
	results = posts_all()
	if request.method == 'POST':
		db = get_db()
		results = posts_all()
		x = 1
		#if request.form
		for post in results:
			removex = str(x) + 'delete'
			st = str(removex)
			#print (st)
			removefield = request.form.get(st)
			post_title = post['title']
			#removefield = request.form['{}'.format(strdel)]
			#print(removefield)
			x = x + 1
			if removefield == 'delete':
				print("yes")
				db = get_db()
				db.execute("DELETE FROM posts WHERE title = (?);", [post_title])
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
				db.execute("DELETE FROM posts WHERE title = (?);", [post_title])
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
				print ("unsaved")
				db = get_db()
				db.execute("DELETE FROM posts WHERE title = (?);", [post_title])
				db.commit()
				print ("deleted")
		return redirect(url_for('unfavunsort'))
	return render_template("unfavunsort.html", results=results)


#print(vars(test))

#@app.route('/viewtables')
#def viewtables():
#	db = get_db()
#	cur = db.execute('SELECT name FROM sqlite_master WHERE type="table";')
#	db.commit()
#	results = cur.fetchall()
#	tables = []
#	for result in results:
#		for test in result:
#			tables.append(test)
	#return str(results)

#def viewtabless():
#	db = get_db()
#	cur = db.execute('SELECT name FROM sqlite_master WHERE type="table";')
#	db.commit()
#	results = cur.fetchall()
#	tables = []
#	for result in results:
#		for test in result:
#			return test