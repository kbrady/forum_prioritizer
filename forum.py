import analize
import heap
from feed import feed
from datetime import datetime, timedelta

# thread organization
class forum:
	def __init__(self, feed):
		self.feed = feed
		self.thread_list = {}
		self.last_content_time = None
		self.heap_list = []
	
	def get_thread(self):
		next_content = self.feed.retrieve_content()
		thread_node(self, next_content)
		return next_content
	
	def get_next_day(self):
		if self.last_content_time is None:
			self.get_thread()
		to_time = self.last_content_time + timedelta(days=1)
		while self.last_content_time < to_time:
			self.get_thread()
	
	def __str__(self):
		return self.feed.database_name

class thread_node:
	def __init__(self, forum, content):
		self.forum = forum
		self.content = content
		self.parent = None
		self.child = None
		self.forum.last_content_time = self.content.post_time
		if content.thread_id in self.forum.thread_list:
			bottom = self.forum.thread_list[content.thread_id]
			while bottom.child is not None:
				bottom = bottom.child
			bottom.child = self
			self.parent = bottom
			self.thread_title = self.parent.thread_title
			self.forum_id = self.parent.forum_id
			for pl in self.forum.heap_list:
				pl.thread_heap_map[self.content.thread_id].update()
		else:
			self.forum.thread_list[self.content.thread_id] = self
			self.thread_title, self.forum_id = self.forum.feed.getThreadTitle(self.content.thread_id)
			for pl in self.forum.heap_list:
				heap.heap_node(pl, self)
	
	def post_list(self):
		my_list = [self.content]
		if self.child is not None:
			my_list += self.child.post_list()
		return my_list
	
	def evaluate(self, eval_fun=analize.evaluate):
		return eval_fun(self)
	
	def __repr__(self):
		return str(str(self.depth()) + ' ' + self.thread_title)
	
	def depth(self):
		if self.child == None:
			return 1
		return 1 + self.child.depth()
