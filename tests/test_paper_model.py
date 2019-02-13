import unittest
from app.models import PaperInfo, PaperTables, User

p = PaperInfo(table_name="paper_test", paper_name="测试", questions="z@z@z", questions_img="_@_@_",
              answers="1/2/3/4@1/2/3/5@1/2/3/6", answers_img="///@///@///",
              answers_score="-1#-2#-3#0/1#2#3#4/3#4#5#6/2#1#4#5@-1#-2#-3#0/1#2#3#4/3#4#5#6/2#1#4#6@-1#-2#-3#0/1#2#3#4/3#4#5#6/2#1#4#7",
              answers_multiple="0@1@0", comments_condition="50#70/10#100@0#10@20#100",
              comments="很有责任心@责任心@有责任心", score_attr="责任心@爱心@激情@努力")


class TestPaper(unittest.TestCase):

	def test_paper_table_exist(self):
		self.assertIsNotNone(PaperTables["paper_test"])

	def test_paper_table_cols_num(self):
		for i in range(4, 1):
			self.assertTrue(hasattr(PaperTables["paper_test"], "col_" + str(i)))

	def test_foreign_keys(self):
		key = "paper_test_id"
		self.assertTrue(hasattr(User, key))

	def test_questions_to_json(self):
		self.assertEqual(p.questions_to_json(), [
			{'question': 'z', 'question_img': ''},
			{'question': 'z', 'question_img': ''},
			{'question': 'z', 'question_img': ''}])

	def test_answers_to_json(self):
		self.assertEqual(p.answers_to_json(), [
			{'answers': ['1', '2', '3', '4'], 'answers_img': ['', '', '', ''],
			 'multiple': False},
			{'answers': ['1', '2', '3', '5'], 'answers_img': ['', '', '', ''],
			 'multiple': True},
			{'answers': ['1', '2', '3', '6'], 'answers_img': ['', '', '', ''],
			 'multiple': False}])

	def test_paper_to_json(self):
		self.assertEqual([
			{'question': 'z', 'question_img': '', 'answers': ['1', '2', '3', '4'], 'answers_img': ['', '', '', ''],
			 'multiple': False},
			{'question': 'z', 'question_img': '', 'answers': ['1', '2', '3', '5'], 'answers_img': ['', '', '', ''],
			 'multiple': True},
			{'question': 'z', 'question_img': '', 'answers': ['1', '2', '3', '6'], 'answers_img': ['', '', '', ''],
			 'multiple': False}], p.to_json())
