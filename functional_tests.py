from selenium import webdriver
import unittest

class VisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_user_login(self):
        self.browser.get('http://127.0.0.1:8000')
        self.assertIn('Surmandl', self.browser.title)
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
