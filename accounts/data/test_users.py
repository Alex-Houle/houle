import unittest

from user_api import UserAPI
um = UserAPI()

class TestUserManager(unittest.TestCase):

    # @unittest.skip
    def test_basic(self):
        ''' Initialize, create user, read_by_id user'''

        um.delete_all()

        u = {'username':'joe','password':'pw'}
        uid = um.create(u)

        u = um.read_by_id(uid)
        print(u)

        self.assertIsNotNone(u)

    # @unittest.skip
    def test_unique(self):
        ''' try to create a user with the same username twice'''

        um.delete_all()

        u = {'username':'joe','password':'pw'}
        uid = um.create(u)

        try:
            uid = um.create(u)
        except Exception as e:
            print(e)
        else:
            raise Exception('should have been an error here')

    # @unittest.skip
    def test_reads(self):
        ''' read all, read by username'''

        um.delete_all()

        us = [{'username':'joe','password':'pw'},
            {'username':'jane','password':'pw'}]
        
        for u in us:
            uid = um.create(u)

        us = um.read_all()
        self.assertEqual(len(us.get('users')),2)

        q = {'username':'jane'}
        us = um.read(q)
        u = us.get('users')[0]
        self.assertEqual(u.get('username'),'jane')
        
    # @unittest.skip
    def test_update(self):
        ''' update password '''

        um.delete_all()

        u = {'username':'joe','password':'pw'}
        uid = um.create(u)

        updates = {'password':'newpw'}
        um.update(uid,updates)

        u = um.read_by_id(uid)
        self.assertEqual(u.get('password'),'newpw')

    # @unittest.skip
    def test_delete(self):
        '''reset, create, delete, read'''

        um.delete_all()

        u = {'username':'joe','password':'pw'}
        uid = um.create(u)

        result = um.delete_by_id(uid)
        self.assertEqual(result,1)

        u = um.read_by_id(uid)
        self.assertIsNone(u)


if __name__ == '__main__':
    unittest.main()