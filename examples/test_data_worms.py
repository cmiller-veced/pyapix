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


aphia_id = {
    'good': [
        {'ID': 127160 }
    ],
    'bad': [ 
        {'id': 127160 }
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
    ],
    'bad': [ 
        {
            'stationId': 'CO100',
            'limit':   '100', 
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


test_parameters = {
    '/AphiaClassificationByAphiaID/{ID}': aphia_id,
    '/AphiaExternalIDByAphiaID/{ID}': aphia_id,
    '/AphiaRecordByAphiaID/{ID}': aphia_id,
    '/AphiaVernacularsByAphiaID/{ID}': aphia_id,
    '/AphiaRecordFullByAphiaID/{ID}': aphia_id,
} 

"""
/AphiaChildrenByAphiaID/{ID} get
/AphiaDistributionsByAphiaID/{ID} get
/AphiaIDByName/{ScientificName} get
/AphiaNameByAphiaID/{ID} get
/AphiaRecordsByAphiaIDs get
/AphiaRecordByExternalID/{ID} get
/AphiaRecordsByDate get
/AphiaRecordsByMatchNames get
/AphiaRecordsByName/{ScientificName} get
/AphiaRecordsByNames get
/AphiaRecordsByVernacular/{Vernacular} get
/AphiaSynonymsByAphiaID/{ID} get
/AphiaSourcesByAphiaID/{ID} get
/AphiaTaxonRanksByID/{ID} get
/AphiaTaxonRanksByName/{taxonRank} get
/AphiaRecordsByTaxonRankID/{ID} get
/AphiaAttributeKeysByID/{ID} get
/AphiaAttributeValuesByCategoryID/{ID} get
/AphiaIDsByAttributeKeyID/{ID} get
/AphiaAttributesByAphiaID/{ID} get
"""

