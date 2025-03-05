# Copyright (c) 2024-2025 Cary Miller
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.

occurrence = {
    'good': [
        {'ScientificName': 'Solea solea' }, 
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
    '/AphiaRecordsByName/{ScientificName}': occurrence,

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

