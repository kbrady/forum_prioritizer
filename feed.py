import MySQLdb
from datetime import datetime

database_user = 'root'

class content:
	def __init__(self, text, id, poster_id, thread_id, post_time):
		self.text = text
		self.id = int(id)
		self.poster_id = poster_id
		self.thread_id = int(thread_id)
		self.post_time = datetime.fromtimestamp(post_time)
	
	def __str__(self):
		return self.text

class post(content):
	def ispost(self):
		return True

class comment(content):
	def ispost(self):
		return False

class feed:
	def __init__(self, database):
		self.database_name = database
		self.db = MySQLdb.connect(user=database_user, db=database)
		self.cur = self.db.cursor()
		self.content_stream = None
	
	def retrieve_content(self):
		if self.content_stream is None:
			if self.database_name in ['POSA']:
				self.cur.execute('select * from ((select post_text as text, id, forum_user_id as user_id, thread_id, post_time, 1 as ispost from forum_posts) union (select comment_text as text, id, forum_user_id as user_id, thread_id, post_time, 0 as ispost from forum_comments) order by post_time) as t')
			else:
				self.cur.execute('select * from ((select post_text as text, id, user_id, thread_id, post_time, 1 as ispost from forum_posts) union (select comment_text as text, id, user_id, thread_id, post_time, 0 as ispost from forum_comments) order by post_time) as t')
			self.content_stream = list(self.cur.fetchall())
		if len(self.content_stream) == 0:
			return None
		result = self.content_stream.pop(0)
		text, id, poster_id, thread_id, post_time, ispost = result
		if ispost:
			next_val = post(text, id, poster_id, thread_id, post_time)
		else:
			next_val = comment(text, id, poster_id, thread_id, post_time)
		return next_val
	
	def getThreadTitle(self, thread_id):
		self.cur.execute('select title, forum_id from forum_threads where id = '+str(thread_id))
		return self.cur.fetchone()
