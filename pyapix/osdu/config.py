import os

class base_path:
    dir = '~/osdu/pre-shipping/R3-M24/AWS-M24'


class path:
    base_dir = base_path.dir
    (d, f) = ('Policy', 'AWS_OSDUR3M24_Policy_Collection.postman_collection.json')
    policy = os.path.expanduser(f'{base_dir}/{d}/{f}')

    (d, f) = ('DDMS Wellbore', 'Wellbore_DDMS_v3.0.postman_collection.json')
    wellbore_ddms = os.path.expanduser(f'{base_dir}/{d}/{f}')

    (d, f) = ('Core Services', 'AWS_OSDUR3M24_CoreServices_Collection.postman_collection.json')
    core_services = os.path.expanduser(f'{base_dir}/{d}/{f}')

    (d, f) = ('Schema Upgrade', 'Schema_Upgrade_with_JOLT.postman_collection.json')
    schema_upgrade = os.path.expanduser(f'{base_dir}/{d}/{f}')

    (d, f) = ('DDMS Reservoir', 'AWS_OSDUR3M23_ReservoirDDMS_Collection.postman_collection.json')
    reservoir_ddms = os.path.expanduser(f'{base_dir}/{d}/{f}')

    (d, f) = ('DDMS Seismic', '')
# AWS_OSDUR3M24_SegyToOpenVDS_Conversion_using_Seisstore_v1.1.postman_collection.json
# AWS_OSDUR3M24_Seismic_v4_Automated.postman_collection.json
# AWS_OSDU_R3M24_OZGY_SDUtilUpload_API_Collections.postman_collection.json
# ST0202R08_PS_PSDM_RAW_PP_TIME.MIG_RAW.POST_STACK.3D.JS-017534.segy


