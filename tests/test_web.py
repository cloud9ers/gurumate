import unittest
import gurumate.web
from gurumate.base import ValidationError

class TestWebOps(unittest.TestCase):
	def testAccessibility(self):
		gurumate.web.check_url_accessibility("http://google.com")
		try:
			gurumate.web.check_url_accessibility("http://127.0.0.5")
		except ValidationError, e:
			pass
	
	def testAccessibilityNot200(self):
		try:
			gurumate.web.check_url_accessibility("http://google.com/mazagatshy")
		except ValidationError, e:
			pass
	
	def testCheckResponseCode(self):
		self.assertEquals(200, gurumate.web.get_response_code("http://google.com"))
		self.assertEquals(404, gurumate.web.get_response_code("http://google.com/kokowawatotolala"))
		try:
			gurumate.web.check_response_code("http://google.com", 404)
		except ValidationError:
			pass
		
			gurumate.web.check_response_code("http://google.com", 200)
	
	def testWebContents(self):
		self.assertTrue(gurumate.web.url_has_contents("http://google.com", "google", True))
		try:
			gurumate.web.url_has_contents("http://google.com", "googlE", True)
		except ValidationError:
			pass
		try:
			gurumate.web.url_has_contents("http://google.com", "Batates", False)
		except ValidationError:
			pass
		