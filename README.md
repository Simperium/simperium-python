simperium-python
==============
Simperium is a simple way for developers to move data as it changes, instantly and automatically. This is the Python library. You can [browse the documentation](http://simperium.com/docs/python/).

You can [sign up](http://simperium.com) for a hosted version of Simperium. There are Simperium libraries for [other languages](https://simperium.com/overview/) too.

This is not yet a full Simperium library for parsing diffs and changes. It's a wrapper for our [HTTP API](https://simperium.com/docs/http/) intended for scripting and basic backend development.

### License
The Simperium Python library is available for free and commercial use under the MIT license.

### Getting Started
To get started, first log into [https://simperium.com](https://simperium.com) and
create a new application.  Copy down the new app's name, api key and admin key.

Next install the python client:

    $ sudo pip install git+https://github.com/Simperium/simperium-python.git

Start python and import the lib:

    $ python
    >>> from simperium.core import Auth, Api

We'll need to create a user to be able to store data:

    >>> auth = Auth(yourappname, yourapikey)
    >>> token = auth.create('joe@example.com', 'secret')
    >>> token
    '25c11ad089dd4c18b84f24bc18c58fe2'

We can now store and retrieve data from simperium.  Data is stored in buckets.
For example, we could store a list of todo items in a todo bucket.  When you
store items, you need to give them a unique identifier.  Uuids are usually a
good choice.

    >>> import uuid
    >>> api = Api(yourappname, token)
    >>> todo1_id = uuid.uuid4().hex
    >>> api.todo.post(todo1_id,
                      {'text': 'Read general theory of love', 'done': False})

We can retrieve this item:

    >>> api.todo.get(todo1_id)
    {'text': 'Read general theory of love', 'done': False}

Store another todo:

    >>> api.todo.post(uuid.uuid4().hex,
                      {'text': 'Watch battle royale', 'done': False})

You can retrieve an index of all of a buckets items:

    >>> api.todo.index()
    {
        'count': 2,
        'index': [
            {'id': 'f6b680f8504c4e31a0e54a95401ffca0', 'v': 1},
            {'id': 'c0d07bb7c46e48e693653425eca93af9', 'v': 1}],
        'current': '4f8507b8faf44720dfc432b1',}

Retrieve all the docuemnts in the index:

    >>> [api.todo.get(x['id']) for x in api.todo.index()['index']]
    [
        {'text': 'Read general theory of love', 'done': False},
        {'text': 'Watch battle royale', 'done': False}]

It's also possible to get the data for each document in the index with data=True:

    >>> api.todo.index(data=True)
    {
        'count': 2,
        'index': [
            {'id': 'f6b680f8504c4e31a0e54a95401ffca0', 'v': 1,
                'd': {'text': 'Read general theory of love', 'done': False},},
            {'id': 'c0d07bb7c46e48e693653425eca93af9', 'v': 1,
                'd': {'text': 'Watch battle royale', 'done': False},}],
        'current': '4f8507b8faf44720dfc432b1'}

To update fields in an item, post the updated fields.  They'll be merged
with the current document:

    >>> api.todo.post(todo1_id, {'done': True})
    >>> api.todo.get(todo1_id)
    {'text': 'Read general theory of love', 'done': True}

Simperium items are versioned.  It's possible to go back in time and retrieve
previous versions of documents:

    >>> api.todo.get(todo1_id, version=1)
    {'text': 'Read general theory of love', 'done': False}

Of course, you can delete items:

    >>> api.todo.delete(todo1_id)
    >>> api.todo.get(todo1_id) == None
    True
    >>> api.todo.index()['count']
    1
