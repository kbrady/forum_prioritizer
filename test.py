import feed
import datetime
import heap
import unittest
import analize
import forum

class TestStream(unittest.TestCase):
	def setUp(self):
		self.database = 'OnlineGames'
		self.feed = feed.feed(self.database)
	
	def tearDown(self):
		feed.content_stream = None

class TestFeed(TestStream):
	def test_types(self):
		self.first_value = self.feed.retrieve_content()
		self.assertEqual(True, self.first_value.ispost())
		self.assertEqual(str, type(self.first_value.text))
		self.assertEqual(int, type(self.first_value.id))
		self.assertEqual(int, type(self.first_value.thread_id))
		self.assertEqual(datetime.datetime, type(self.first_value.post_time))
		if self.database in ['POSA', 'POSA2']:
			self.assertEqual(str, type(self.first_value.poster_id))
		else:
			self.assertEqual(long, type(self.first_value.poster_id))

class TestHeap(TestStream):
	def setUp(self):
		super(TestHeap, self).setUp()
		self.threads = set()
		self.content_stream = []
		self.content_counter = 0
		self.forum = forum.forum(self.feed)
		heap.priority_list(self.forum, lambda x: analize.evaluate(x))
		heap.priority_list(self.forum, lambda x: -analize.evaluate(x))
	
	def test_build(self):
		# check correct before first content
		self.assertEqual(0,len(self.forum.thread_list))
		for pl in self.forum.heap_list:
			self.assertEqual(0,len(pl.thread_heap_map))
			self.assertEqual(True,pl.heap_root is None)
		# check the first content gets added correctly
		self.pull_thread()
		self.assertEqual(1,len(self.forum.thread_list))
		for pl in self.forum.heap_list:
			self.assertEqual(1,len(pl.thread_heap_map))
			self.assertEqual(False,pl.heap_root is None)
		# check the heap builds itself to three threads correctly
		num_threads = 900
		last_check = 1
		while len(self.threads) < num_threads and len(self.feed.content_stream) > 0:
			self.pull_thread()
			if len(self.threads) >= last_check * 2:
				self.examine_heap()
				last_check = last_check * 2
			if len(self.feed.content_stream) == 0:
				print len(self.threads)
		self.examine_heap()
		self.check_to_list()
	
	def pull_thread(self):
		next_content = self.forum.get_thread()
		self.threads.add(next_content.thread_id)
		self.content_stream.append(next_content.thread_id)
		self.content_counter += 1
		if len(self.content_stream) > 10:
			self.content_stream.pop(0)
	
	def threads_have_correct_num_contnet(self):
		thread_content_count = 0
		for t in self.forum.thread_list.values():
			thread_content_count += t.depth()
		self.assertEqual(thread_content_count, self.content_counter)
	
	def heap_has_correct_num_elements(self):
		num_threads = len(self.threads)
		for pl in self.forum.heap_list:
			self.assertEqual(num_threads,len(pl.thread_heap_map))
			self.assertEqual(num_threads + 1,len(pl.border))
		self.assertEqual(num_threads,len(self.forum.thread_list))
	
	def heap_values_match_function(self):
		# check the heap uses it's evaluation function
		for pl in self.forum.heap_list:
			for tid in pl.thread_heap_map:
				h = pl.thread_heap_map[tid]
				self.assertEqual(h.value, h.thread_node.evaluate(h.parent_heap.eval_fun))
	
	def heap_values_are_correct_in_relation_to_eachother(self):
		# check the structure of the heap
		for pl in self.forum.heap_list:
			for tid in pl.thread_heap_map:
				h = pl.thread_heap_map[tid]
				try:
					if h.children[0] is not None:
						self.assertEqual(h, h.children[0].parent)
						self.assertEqual(True,h.children[0].value <= h.value)
						self.assertEqual(False, (h, 0) in pl.border)
					else:
						self.assertEqual(True, (h, 0) in pl.border)
					if h.children[1] is not None:
						self.assertEqual(h, h.children[1].parent)
						self.assertEqual(True,h.children[1].value <= h.value)
						self.assertEqual(False, (h, 1) in pl.border)
					else:
						self.assertEqual(True, (h, 1) in pl.border)
					if h.parent is not None:
						self.assertEqual(True, h.parent.children[0] == h or h.parent.children[1] == h)
					else:
						self.assertEqual(h, pl.heap_root)
				except Exception as e:
					print e
					print (h_val(h), h), (h_val(h.parent), h.parent), [(h_val(x),x) for x in h.children]
					print len(heap.thread_list)
					print self.content_stream
					raise e
	
	def check_to_list(self):
		num_threads = len(self.threads)
		# check the list building function
		for pl in self.forum.heap_list:
			heap_list = pl.get_heap_list()
			self.assertEqual(num_threads, len(heap_list))
			for i in range(len(heap_list)-1):
				self.assertEqual(True, heap_list[i][0] >= heap_list[i+1][0])
	
	def examine_heap(self):
		self.heap_has_correct_num_elements()
		self.heap_values_are_correct_in_relation_to_eachother()
		self.heap_values_match_function()
		self.threads_have_correct_num_contnet()
	
def h_val(h):
	if h is None:
		return None
	return h.value, h.thread_id

if __name__ == '__main__':
	unittest.main()
