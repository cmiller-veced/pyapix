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

# valid UniProtKB accession

valid_accession = [
    { 'accession': 'A2BC19', },
    { 'accession': 'P12345', },
    { 'accession': 'A0A023GPI8', },
    { 'accession': 'P04637', },
]
bad_key = [{'x':'xxxxxxx',},]
        
#        { 'accession': 'P62988', },    # 404
proteins = {
    'good': valid_accession,
    'bad': bad_key + [ 
        {},
        { 'accession': 'xxxxxxxx', },
    ]
}

proteins_accession = {
    'good': valid_accession,
    'bad': bad_key + [{}],
}

epitope = proteins

proteome = {
    'good': [
        { 'upid': 'UP000005640', },    # but empty result
    ],
    'bad': proteins['bad'],
}

das_s4entry = {
    'good': [],
    'bad': [{'x':''}, {}],
}

uniparc_sequence = {
    'good': [
#         {'rfActive': 'true'}, 
#         """
#         <Response [500 Internal Server Error]>
#         >>> response.text
#         '{"requestedURL":"https://www.ebi.ac.uk/proteins/api/uniparc/sequence?rfActive=true","errorMessage":["Cannot invoke \\"uk.ac.ebi.uniprot.dataservice.restful.uniparc.UniparcSequenceParam.getSequence()\\" because \\"sequence\\" is null"]}'
#         """

#         {'rfActive': 'false'}, 
#        {'rfDbid': 'AAC02967,XP_006524055'},   # but returns 500 error
#         """
# '{"requestedURL":"https://www.ebi.ac.uk/proteins/api/uniparc/sequence?rfDbid=AAC02967,XP_006524055","errorMessage":["Cannot invoke \\"uk.ac.ebi.uniprot.dataservice.restful.uniparc.UniparcSequenceParam.getSequence()\\" because \\"sequence\\" is null"]}'
#         """

#        {'rfDdtype': 'EMBL,RefSeq,Ensembl'}, 
     ],
    'bad': [
        {'rfActive': True}, 
        {'rfActive': 'xxxxxxx'}, 
        {'rfTaxId': 'xxxxxx'}, 
        {'x': 'xxxxxx'}, 
    ],
}

hgvs_examples = ["NM_000551.3", "NC_000012.12"]  # bad request
hgvs_examples = ["c.88+2T>G",]  # invalid

# https://hgvs-nomenclature.org/stable/recommendations/grammar/
hgvs = {
    'good': [{'hgvs': thing} for thing in hgvs_examples],
    'bad': bad_key + [{},],
}


test_parameters = {
    '/proteins': proteins ,
    '/proteins/{accession}': proteins_accession ,
#    '/antigen/{accession}': antigen ,
    '/epitope': epitope ,
    '/proteomes': proteome ,
    '/proteomes/{upid}': proteome ,
    '/proteomics': proteome ,

   '/das/s4entry': das_s4entry ,               # patched
   '/uniparc/sequence': uniparc_sequence ,     # post
#    '/variation/hgvs/{hgvs}': hgvs ,
} 

