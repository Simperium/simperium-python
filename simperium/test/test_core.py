import os
import sys
import unittest
import uuid

from simperium import core

api_key = os.environ.get('SIMPERIUM_CLIENT_TEST_APIKEY')
appname = os.environ.get('SIMPERIUM_CLIENT_TEST_APPNAME')

if not appname:
    print
    print
    print "\tset SIMPERIUM_CLIENT_TEST_APPNAME and SIMPERIUM_CLIENT_TEST_APIKEY"
    print
    sys.exit()

# cache user create to cut down on the number of users created by the test suite
_username = None
_password = None
_auth_token = None
def get_auth_token():
    global _username
    global _password
    global _auth_token
    if not _auth_token:
        auth = core.Auth(appname, api_key)
        _username = uuid.uuid4().hex + '@foo.com'
        _password = uuid.uuid4().hex
        _auth_token = auth.create(_username, _password)
    return _auth_token


class AuthTest(unittest.TestCase):
    def test_authorize(self):
        get_auth_token()
        auth = core.Auth(appname, api_key)
        auth.authorize(_username, _password)



class BucketTest(unittest.TestCase):
    def test_get(self):
        bucket = core.Bucket(appname, get_auth_token(), uuid.uuid4().hex)
        bucket.post('item1', {'x': 1})
        self.assertEqual(bucket.get('item1'), {'x': 1})

    def test_index(self):
        bucket = core.Bucket(appname, get_auth_token(), uuid.uuid4().hex)
        for i in range(3):
            bucket.post('item%s' % i, {'x': i})

        got = bucket.index(limit=2)
        want = {
            'current': got['current'],
            'mark': got['mark'],
            'index': [
                {'id': 'item2', 'v': 1},
                {'id': 'item1', 'v': 1}], }
        self.assertEqual(want, got)

        got2 = bucket.index(limit=2, mark=got['mark'])
        want2 = {
            'current': got['current'],
            'index': [
                {'id': 'item0', 'v': 1}], }
        self.assertEqual(want, got)

    def test_post(self):
        bucket = core.Bucket(appname, get_auth_token(), uuid.uuid4().hex)
        bucket.post('item1', {'a':1})
        self.assertEqual(bucket.get('item1'), {'a':1})
        bucket.post('item1', {'b':2})
        self.assertEqual(bucket.get('item1'), {'a':1, 'b':2})
        bucket.post('item1', {'c':3}, replace=True)
        self.assertEqual(bucket.get('item1'), {'c':3})


class SPUserTest(unittest.TestCase):
    def test_get(self):
        user = core.SPUser(appname, get_auth_token())
        user.post({'x': 1})
        self.assertEqual(user.get(), {'x': 1})


class ApiTest(unittest.TestCase):
    def test_getitem(self):
        api = core.Api(appname, get_auth_token())
        self.assertTrue(isinstance(api['bucket'], core.Bucket))

    def test_getattr(self):
        api = core.Api(appname, get_auth_token())
        self.assertTrue(isinstance(api.bucket, core.Bucket))

    def test_user(self):
        api = core.Api(appname, get_auth_token())
        self.assertTrue(isinstance(api.SPUser, core.SPUser))
