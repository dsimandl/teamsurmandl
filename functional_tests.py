from selenium import webdriver
import unittest

class VisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_user_login(self):
        # Jenny hears about a cool new family CMS.  She goes to check it out
        self.browser.get('http://127.0.0.1:8000')
        # Jenny notices the word surmandl in the browser title and the please log in on the page
        self.assertIn('Surmandl', self.browser.title)
        signin_text = self.browser.find_element_by_class_name('form_signin-heading')
        self.assertEqual('Please sign in', signin_text.text)
        # She is invited to enter a login right away
        username_inputbox = self.browser.find_element_by_id('id_username')
        password_inputbox = self.browser.find_element_by_id('id_password')
        self.assertEqual(username_inputbox.get_attribute('placeholder'), 'Email address')
        self.assertEqual(password_inputbox.get_attribute('placeholder'), 'Password')
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
