import re

def evaluate(thread):
	if thread.child is not None:
		return evaluate(thread.child)
	return question_marks(thread) - 20 * thank_you(thread) + question_words(thread)

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
	if thread.child is not None:
		return question_words(thread.child)
	num_whys = len(re.split('[Ww]hy', thread.content.text)) - 1
	num_quizzes = len(re.split('[Qq]uiz', thread.content.text)) - 1
	num_qs = num_whys + num_quizzes
	return num_qs
