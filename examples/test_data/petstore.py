
# 

petIds = {
    'good': [1234, '1234', ],
    'bad': ['x', '', '0', 0, ],
}
file = {
    'good': ['1234', 'foo'],
    'bad': ['' , 0, ],
}
status = {
    'good': ['', ''],         # fill in with real data.
    'bad': ['' , 0, 'foo'],
}
petName = {
    'good': ['fluff', 'x'],
    'bad': ['' , 0, []],
}
api_key = {
    'good': ['a?', 'string?'],
    'bad': ['' , 0, 'foo'],
}


orderId = {
    'good': ['', ''],
    'bad': ['' , 0, 'foo'],
}

username = {
    'good': ['', ''],
    'bad': ['' , 0, 'foo'],
}

x = {
    'good': ['', ''],
    'bad': ['' , 0, 'foo'],
}
photoUrls = {
    'good': [[''], []],
    'bad': ['' , 0, 'foo'],
}
category = {
    'good': [{}, {'foo': 'bar'}],
    'bad': ['' , 0, 'foo'],
}
# TODO: put together atomic parameters.    Maybe.

api_key = 'special-key'   # which actually works.

# endpoint: /pet  verb: POST
from_postman_online = {
  "name": "doggie",
  "photoUrls": [
    "adipisicing",
    "non et"
  ],
  "id": 73291872,
  "category": {
    "id": -97087948,
    "name": "incididunt cupidatat nostrud"
  },
  "tags": [
    {
      "id": -41459971,
      "name": ""
    },
    {
      "id": -75303293,
      "name": "mollit"
    }
  ],
  "status": "sold"
}

generic_bad = ['' , 0, 'foo', {}] 
generic_bad = ['' , 0, 'foo'] 

uploadImage_post = {
    'good': [
      {
       'petId': 1234,
       'additionalMetadata': 'aaaaaaa',
       'file': 'ffffff',
      }, 
      {
       'petId': 1234,
      }, 
    ],
    'bad': generic_bad,
}

Pet_post = {
    'good': [
      {
       'id': 1234,
       'category': {},
       'name': 'fluff',
       'photoUrls': [],
       'status': 'available',
       'tags': [],
      }, 
      from_postman_online,
    ],
    'bad': generic_bad
}
Pet_put = {
    'good': [
      {
       'photoUrls': [],
       'name': 'buff',
      }, 
      {
       'photoUrls': [],
       'name': 'buff',
       'status': 'pending',
      }, 

    ],
    'bad': generic_bad
}

Pet_findByStatus = {
    'good': [
      ['sold', ], 
      ['sold', 'pending'], 
    ],
    'bad': []
#    'bad': generic_bad
}
Pet_findByTags = {
    'good': [
        {'tags': ['foo', ]}, 
        {'tags': ['foo', 'bar']}, 
    ],
    'bad': []
#    'bad': generic_bad
}


petId_get = {
  'good': [
    {'petId': 1234}, 
    {'petId': 0}, 
    {'petId': 58806647}, 
  ],
  'bad': [],
}

petId_post = {
    # TODO: start here
    'good': [ {
         'petId': 1234,
         'name': 'fluff',
         'status': 'available',
        }, 
    ],
    'bad': ['' , 0, 'foo', {}],
}


petId_delete = {
    'good': [ {
         'petId': 1234,
         'api_key': api_key,
        }, 
    ],
    'bad': generic_bad,
}

store_inventory = {
    'good': [],
    'bad': [],
}

store_order_post = {
    'good': [ {
         'id': 4321,
         'petId': 1234,
        }, 
        {
         'petId': 1234,
        }, 
        {},
    ],
    'bad': generic_bad,
}
store_order_get = {
    'good': [
      {'orderId': 1},
      {'orderId': 9},
    ],
    'bad': []
#    'bad': [0, 99, 'x']
}
store_order_delete = {
    'good': [
      {'orderId': 1},
      {'orderId': 9},
    ],
    'bad': []
#    'bad': [0, 'x']
}

user_delete = {
    'good': [ {
         'username': 'user1',
        }, 
    ],
    'bad': [{}],
}

user_good = {
    'good':  
        [ {
             'username': 'user1',
#             'password': 'xxxx',
            }, 
        ],
    'bad': [] 
}

user_login_get = {
    'good': [ {
         'username': 'user1',
         'password': 'xxxx',
        }, 
    ],
    'bad': [{}],
}

user_logout_get = {
    'good': [], 
    'bad': [],
}

user_with_array_post = {
    'good': [ [{
         'id': 1234,
         'username': 'user1',
        }], 
        [{}],
    ],
    'bad': generic_bad,
}

user_get = {
    'good': [ 'user1', 'bar' ],
    'bad': [0],
}
user_put = {
    'good': [ {
         'username': 'user1',
         'body': {},
        }, 
    ],
    'bad': generic_bad,
}

user_post = {
    'good': [ {
         'id': 2314345670987,
         'username': 'user2314345670987',
        }, 
        {},
    ],
    'bad': generic_bad,
}


test_parameters = {
    '/pet/{petId}/uploadImage': {
        'post': uploadImage_post ,
    },
    '/pet': {
        'post': Pet_post ,
        'put': Pet_put,
    },
    '/pet/findByStatus': {
        'get': Pet_findByStatus,
    },
    '/pet/findByTags': {
        'get': Pet_findByTags,
    },

    '/pet/{petId}': {
        'get': petId_get,
        'post': petId_post,
        'delete': petId_delete,
    },

    '/store/inventory': {
        'get': store_inventory,
    },
    '/store/order': {
        'post': store_order_post,
    },
    '/store/order/{orderId}': {
        'get': store_order_get,
        'delete': store_order_delete,
    },

    '/user/login': {
        'get': user_login_get 
    },
    '/user/logout': {
        'get': user_logout_get 
    },
    '/user/createWithArray': {
        'post': user_with_array_post,
    },
    '/user/createWithList': {
        'post': user_with_array_post,
    },
    '/user/{username}': {
#        'get': user_get ,
        'get': user_good ,
        'put': user_put ,
#        'delete': user_get ,
        'delete': user_good ,
    },

    '/user': {
        'post': user_post ,
    },
} 


