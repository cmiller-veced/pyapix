
sample_query_params = {
    'productId': 'ZFP',
    #        'typeId': 'TTTTTT',
    'zoneId': 'WYZ433',
    'stationId': 'CO100',
    #        'locationId': 'LLLLLL',
}


active_alerts = {
    'good': [
        { 'area': ['WY'], 'limit':   50, },
        { 'area': ['CO', 'KS', 'PK', 'PH'] },

        #        { 'xxxx':   'yyyyyyy', },    # additionalProperties permitted
        # but rejected by endpoint    400 Bad Request

        #        { 'zoneId':   'xxxxxx', },    # additionalProperties permitted
        # but rejected by endpoint    400 Bad Request

        { 'status':   ['actual', 'test'], }, 
        { 'message_type':   ['alert', 'cancel'], }, 
        { 'event':   ['Hard Freeze Warning', 'Dense Fog Advisory'], }, 
    ],
    'bad': [ 
            #        { 'limit':   '100', },
        # but accepted by endpoint
        { 'status':   ['xxxxxx'], }, 
    ],
}

# AHA!    brainwave!!!    Must take action to distinguish different error types
# in the test code.
# And distinguish validation error from endpoint error.
# for example with this ill-behaved endpoint ....
# /zones/forecast/{zoneId}/stations


#        { 'zoneId': 'WYZ433', },   # 500
"""
>>> print(response.text)
{
    "correlationId": "4388435f",
    "title": "Unexpected Problem",
    "type": "https://api.weather.gov/problems/UnexpectedProblem",
    "status": 500,
    "detail": "An unexpected problem has occurred. If this error continues, please contact support at nco.ops@noaa.gov.",
    "instance": "https://api.weather.gov/requests/4388435f"
}
"""


zones_and_limits = {
    'good': [
    ],
    'bad': [ 
        { 'limit':   '100', },
        { 'zoneId':   'xxxxxx', },
    ],
}

zones = {
    'good': [
        #        { 'zone': 'WYZ433', },
        #{ 'zoneId': 'WYZ433', },
        #{ 'xxxx':   'yyyyyyy', },    # additionalProperties permitted
    ],
    'bad': [ 
        { 'zoneId':   'xxxxxx', },
    ],
}

start_end_limit = {
    'good': [
        {
            'stationId': 'CO100',
            'start': '2024-09-17T18:39:00+00:00', 
            'end':   '2024-09-18T18:39:00+00:00',
            'limit':   50,
        },
        { 'start': '2024-09-17T18:39:00+00:00', 
            'stationId': 'CO100',
         },
        { 'end': '2024-09-17T18:39:00+00:00', 
            'stationId': 'CO100',
         },
        { 'limit':   50, 
            'stationId': 'CO100',
         },
        {  
            'stationId': 'CO100',
         },

        #        { 'start': '20240000-09-17T18:39:00+00:00', },
        # but rejected by endpoint    400 Bad Request

        #        { 'start': 'xxxxxxxx', },
        # but rejected by endpoint    400 Bad Request

        #        { 'x': 'yyyyyyy', },
        # but rejected by endpoint    400 Bad Request

    ],
    'bad': [ 
        {
            'stationId': 'CO100',
            'limit':   '100', 
        },
        {
            'stationId': 'CO100',
            'end':     '2024-09-17T18:39:00+00:00', 
            'start':   '2024-09-18T18:39:00+00:00',
            # end precedes start.  
            # Caught by local validation but not by ordinary validation.
        },

    ],
}

type_ids = {
    'good': [
        #        { 'typeId': 'ZFP', },
        #{ 'typeId': 'yyyyyyy', },
        #'ZFP', 'x', 1, {}, []      # anything goes!!!!!!!!!!!
        # but rejected by endpoint    400 Bad Request
    ],
    'bad': [ 
    ],
}

product_ids = {
    'good': [

#        { 'productId': 'BOU', },
        # but rejected by endpoint    404 Not Found
#        { 'productId': 'ZFP', },
        # but rejected by endpoint    404 Not Found

        #        { 'productId': 'xxxxxx', },
        # but rejected by endpoint    400 Bad Request

    ],
    'bad': [ 
        'ZFP', 'x', 1, {}, [] 
            # strangely, only the first one executes.
    ],
}

test_parameters = {
    '/alerts/active': active_alerts ,
    '/products/{productId}': product_ids ,
    '/products/types/{typeId}': type_ids ,
    '/stations/{stationId}/observations': start_end_limit ,
    '/zones/forecast/{zoneId}/observations' : zones,
    '/zones/forecast/{zoneId}/stations' : zones_and_limits,
} 
# https://www.postman.com/api-evangelist/national-oceanic-and-atmospheric-administration-noaa/request/9hlbjhj/products-productid
# Sadly, it has no actual data.


