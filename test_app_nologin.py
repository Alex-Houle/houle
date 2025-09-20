# import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from bs4 import BeautifulSoup as bs
import unittest
from datetime import datetime

try:
    from gradescope_utils.autograder_utils.decorators import weight, number
except Exception as e:
    print(e)
    from test_dummy import weight,number
    

client = app.test_client()

class TestApp(unittest.TestCase):

    def setUp(self):
        response = client.post("/users/delete/all")
        # text = response.data.decode()
        # print(text)    

        response = client.post("/users/create",data={
            'username':'test1',
            'password':'test1'
        })          

        print(self.id())

    @classmethod
    def tearDownClass(self):
        response = client.post("/users/delete/all")
        # text = response.data.decode()
        # print(text)    

        response = client.post("/users/create",data={
            'username':'admin',
            'password':'admin',
            'admin':True
        })  
        # text = response.data.decode()

    #-------------- INDEX ------------------------

    @weight(1)
    @number("1")
    def testGetIndex(self):
        '''get index, 
        assert nav links are present'''

        response = client.get("/")
        text = response.data.decode()

        soup = bs(text,'lxml')
        links = soup.find_all('a')

        refs = [l.get('href') for l in links]
        # print(refs)

        self.assertIn('/users/create',refs)
        self.assertIn('/users/',refs)

    #----------------- CREATE --------------------

    @weight(1)
    @number("2")
    def testGetCreate(self):
        ''' get create form, 
        assert input names are correct'''

        response = client.get("/users/create")
        text = response.data.decode()
        # print(text)

        soup = bs(text,'lxml')
        inputs = soup.find_all('input')

        names = [i.get('name') for i in inputs]

        self.assertIn('username',names)
        self.assertIn('password',names)

    @weight(1)
    @number("3")
    def testPostCreate(self):
        ''' post to /users/create, 
        assert redirect to /users/
        assert new user is in users table'''

        ms = datetime.now().microsecond
        un = f"user{ms}"

        response = client.post("/users/create",data={
            'username':un,
            'password':'pass'
        })
        text = response.data.decode()

        # get redirect url
        soup = bs(text,'lxml')
        ref = soup.find('a').get('href')
        # print(ref)

        # get user listing
        response = client.get(ref)
        text = response.data.decode()
        soup = bs(text,'lxml')

        # get all text in data table
        tds=soup.find_all('td')
        contents = [td.text for td in tds]
        # print(contents)

        self.assertIn(un,contents)

    #--------------- READ -------------------------

    ''' GET users is tested above in POST create
    GET user
    '''

    @weight(1)
    @number("4")
    def testGetUser(self):
        '''
        get one user by username
        '''

        un = "test1"

        response = client.get(f"/users/{un}")
        text = response.data.decode()
        # print(text)

        soup = bs(text,'lxml')

        # get username input
        un_input = soup.find('input', {'name':'username'})

        self.assertEqual(un_input.get('value'), un)

    #--------------- UPDATE ------------------

    @weight(1)
    @number("5")
    def testPostUpdate(self):
        '''
        update user password
        '''

        un = 'test1'
        newpw = 'test2'

        response = client.post(f"/users/{un}",data={
            'password':newpw
        })
        text = response.data.decode()        
        # print(text)

        # get redirect url
        soup = bs(text,'lxml')
        ref = soup.find('a').get('href')
        # print(ref)

        # get user view
        response = client.get(ref)
        text = response.data.decode()
        # print(text)
        
        # get password input
        soup = bs(text,'lxml')
        pw_input = soup.find('input', {'name':'password'})

        self.assertEqual(pw_input.get('value'), newpw)


    #----------------- DELETE --------------------

    @weight(1)
    @number("6")
    def testPostDelete(self):
        ''' create user, delete user, get redirect'''

        ms = datetime.now().microsecond
        un = f"user{ms}"

        response = client.post("/users/create",data={
            'username':un,
            'password':'pass'
        })        

        response = client.post(f"/users/delete/{un}")
        text = response.data.decode()

        # get redirect url
        soup = bs(text,'lxml')
        ref = soup.find('a').get('href')

        # get user listing
        response = client.get(ref)
        text = response.data.decode()
        soup = bs(text,'lxml') 

        # get all text in data table
        tds=soup.find_all('td')
        contents = [td.text for td in tds]
        # print(contents)

        self.assertNotIn(un,contents)                       

if __name__ == '__main__':
    unittest.main()
        

