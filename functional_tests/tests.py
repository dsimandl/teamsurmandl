from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase
from profiles.models import SurmandlUser

class VisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.user = SurmandlUser.objects.create_user('test@test.com', 'test', 'user', 'self', password='Passw0rd')


    def tearDown(self):
        self.browser.quit()

    def send_keys_for_login(self, text, creds):

        # Jenny now logs into the site
        for i in range(len(text)):
            self.browser.get(self.live_server_url)
            username_inputbox = self.browser.find_element_by_id('id_username')
            password_inputbox = self.browser.find_element_by_id('id_password')
            username_inputbox.send_keys(creds[i].get('username'))
            username_inputbox.send_keys(Keys.TAB)
            password_inputbox.send_keys(creds[i].get('password'))
            password_inputbox.send_keys(Keys.ENTER)
            login_lst = self.browser.find_elements_by_class_name('login-alert')
            if text[i] == 'Success':
                team_surmandl = self.browser.find_element_by_tag_name('h1')
                self.assertEqual(team_surmandl.text, 'Team Surmandl Yeah!')
            else:
                self.assertEquals(login_lst[0].text, text[i])


    def test_login_page(self):
        # Jenny hears about a cool new family CMS.  She goes to check it out
        self.browser.get(self.live_server_url)
        # Jenny notices the word surmandl in the browser title and the please log in on the page
        self.assertIn('Surmandl', self.browser.title)
        signin_text = self.browser.find_element_by_class_name('form_signin-heading')
        self.assertEqual('Please sign in', signin_text.text)
        # She is invited to enter a login right away
        username_inputbox = self.browser.find_element_by_id('id_username')
        password_inputbox = self.browser.find_element_by_id('id_password')
        self.assertEqual(username_inputbox.get_attribute('placeholder'), 'Email address')
        self.assertEqual(password_inputbox.get_attribute('placeholder'), 'Password')

        # Jenny tries the following actions:
        # 1. She trys to log in with no password or username
        # 2. Jenny now logs incorrectly into the site with an email present but not a password
        # 3. Jenny now logs incorrectly into the site with an email not present but a password present
        # 4. Jenny now tries to log in with an incorrect email address and password
        self.send_keys_for_login(['* Email address and password are required',
                                                                        '* Password is required', '* Email is required',
                                                                        '* Your email and password do not match', 'Success'],
                                    [{'username': '', 'password': ''},
                                        {'username': 'test@test.com', 'password': ''},
                                        {'username': '', 'password': 'Passw0rd'},
                                        {'username': 'test@test.com', 'password': 'Password'},
                                        {'username': 'test@test.com', 'password': 'Passw0rd'}]
                                 )

