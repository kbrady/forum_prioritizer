from flask import Flask, render_template, request, jsonify, Markup, redirect, url_for
import analize
import string
from forum import forum
import heap
from feed import feed

app = Flask(__name__)

class thread_title:
	def __init__(self, id, title):
		self.id = id
		self.title = make_ascii(title)

class list_title:
	def __init__(self, index, title):
		self.index = index
		self.title = title

class forum_title:
	def __init__(self, index, title):
		self.index = index
		self.title = title

def get_thread_list():
	the_list = [thread_title(n[1].content.thread_id, str((n[0], n[1]))) for n in forum_list[forum_index].heap_list[pl_index].get_heap_list()]
	print 'test', len( the_list )
	return the_list

def get_heap_list():
	return [list_title(i, forum_list[forum_index].heap_list[i].title) for i in range(len(forum_list[forum_index].heap_list))]

def get_forum_list():
	return [forum_title(i, str(forum_list[i])) for i in range(len(forum_list))]

pl_index = 0
forum_list = []
forum_index = 0

@app.route('/')
def home():
	return render_template('home.html', threads=get_thread_list(), lists=get_heap_list(), index=pl_index, forums=get_forum_list(), forum_index=forum_index)

@app.route('/list/<new_index>')
def switch_list(new_index):
	global pl_index
	pl_index = int(new_index)
	return redirect('/')

@app.route('/forum/<new_index>')
def switch_forum(new_index):
	global forum_index
	forum_index = int(new_index)
	return redirect('/')

@app.route('/read/thread')
def read_thread():
	forum_list[forum_index].get_thread()
	return redirect('/')

@app.route('/read/thread_day')
def read_next_day():
	forum_list[forum_index].get_next_day()
	return redirect('/')

@app.route('/thread/<int:thread_id>')
def thread_page(thread_id):
	posts = [make_ascii(p.text) for p in forum_list[forum_index].thread_list[int(thread_id)].post_list()]
	return render_template('thread.html', posts=posts)

def make_ascii(text):
	return Markup(filter(lambda x: x in string.printable, text))

if __name__ == '__main__':
	forum_list.append(forum(feed('OnlineGames')))
	forum_list.append(forum(feed('OnlineGames2')))
	forum_list.append(forum(feed('Nutrition')))
	forum_list.append(forum(feed('Nutrition2')))
	forum_list.append(forum(feed('Innovation')))
	forum_list.append(forum(feed('Innovation2')))
	for f in forum_list:
		heap.priority_list(f, analize.evaluate, 'default')
		heap.priority_list(f, analize.question_marks, 'question_marks')
		heap.priority_list(f, lambda x: -analize.evaluate(x), 'reversed')
		f.get_next_day()
	app.run(debug=True, host='0.0.0.0')
	
