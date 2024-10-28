occurrence = {
    'good': [
        {'scientificname': 'Solea solea' }, 
        {},
    ],
    'bad': [ 
        {'taxonid': 127160 },
        {'foo': 127160 },
    ],
}

occurrence_id = {
    'good': [
        {'id':  '00000119-203a-4605-bb25-8f850b475213'}, 
    ],
    'bad': [ 
        {'foo': 127160 },
    ],
}





checklist_newest = {
#     """
#         <Response [500 Internal Server Error]>
# >>> response.text
# '{"total":0,"results":[],"error":"[search_phase_execution_exception] "}'
# >>> 
#     """
    'good': [
        {}
    ],
    'bad': [ 
    ],
}

taxon_id = {
    'good': [
        {'id': 127160 }
    ],
    'bad': [ 
    ],
}

taxon_scientific = {
    'good': [
        {'scientificname': 'Solea solea' },   # empty list
        {}                                   # long list
    ],
    'bad': [ 
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

country = {
    'good': [
        {}, 
    ],
    'bad': [ 
        {'foo': 127160 },
    ],
}

# {'id': 233, 'country': 'Wallis Futuna Islands', 'code': 'WF'}
country_id = {
    'good': [
#        {'id': 'WF' },
    ],
    'bad': [ 
        {'id': 233 },
    ],
}


test_parameters = {
#    '/checklist/newest': checklist_newest,
    '/occurrence': occurrence,
    '/occurrence/{id}': occurrence_id,
    '/taxon/{id}': taxon_id,
    '/taxon/{scientificname}': taxon_scientific,
    '/taxon/annotations': taxon_scientific,
    '/country': country,
    '/country/{id}': country_id,
} 

#https://www.marinespecies.org/aphia.php?p=taxdetails&id=127160
#127160  (urn:lsid:marinespecies.org:taxname:127160)


# A related web service....
# https://www.marinespecies.org/rest/


