import converse

class TestConverseBase(object):
	def test_process_issue_with_bad_issue(self):
		returned=converse.process_issue(None)
		assert not returned['upload']