import re

def evaluate(thread):
	if thread.child is not None:
		return evaluate(thread.child)
	return question_marks(thread) + question_words(thread) - social_words(thread)

def thank_you(thread):
	if thread.child is not None:
		return thank_you(thread.child)
	if re.match('.*[Tt]hank.*', thread.content.text):
		return 1
	return 0

def question_marks(thread):
	num_qs = len(re.split('[?] ', thread.content.text)) - 1
	if thread.child is not None:
		return num_qs + question_marks(thread.child)
	return num_qs

def question_words(thread):
	num_qs = len(re.split('[Ww]hy', thread.content.text)) - 1
	num_qs += len(re.split('[Qq]uiz', thread.content.text)) - 1
	num_qs += len(re.split('[Hh]omework', thread.content.text)) - 1
	num_qs += len(re.split('[Ww]rong', thread.content.text)) - 1
	num_qs += len(re.split('[Gg]rade', thread.content.text)) - 1
	if thread.child is not None:
		return num_qs + question_words(thread.child)
	return num_qs

def social_words(thread):
	num_qs = len(re.split('[Ss]tudy[ \t\n]+[Gg]roup', thread.content.text)) - 1
	num_qs += len(re.split('[Hh]ello', thread.content.text)) - 1
	num_qs += len(re.split('[Nn]ame', thread.content.text)) - 1
	if thread.child is not None:
		return num_qs + social_words(thread.child)
	return num_qs
