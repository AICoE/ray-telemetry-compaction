from kfp import dsl
from kfp import components

def imports()->bool:
    # Prerequisite - Imports
    import os
    from ray.util import inspect_serializability
    import ray
    import pyarrow.fs as pq
    import pandas as pd
    return True

def initialize_ray():

    # Prerequisite - Imports
    import os
    from ray.util import inspect_serializability
    import ray
    import pyarrow.fs as pq
    import pandas as pd
    # Making use of datetime for dates, works for every day of the year (30,31,28 day problems go away)
    from datetime import date, timedelta
    from dateutil.relativedelta import relativedelta

    # Prerequisite - Connect to the Ray cluster on OpenShift
    from ray.util.client import ray as rayclient
    if rayclient.is_connected():
        ray.util.disconnect()

    ray.util.connect('{ray_head}:10001'.format(ray_head='ray-cluster-kubeflow-ray-head'))


    # Prerequisite - Specify reusable definitions

    metricName = 'cluster_version'
    #metricName = 'cluster_feature_set'
    #metricName = 'cluster_infrastructure_provider'
    #metricName = 'cluster:usage:consumption:rhods:cpu:seconds:rate5m'

    bucketName = 'DH-SECURE-THANOS-RAY-USE'
    endpoint = 'https://s3.upshift.redhat.com'

    prefixPathRead = 'raydev'
    prefixPathWrite = 'raydev-write-demo'

    year = '2021'
    month = '01'
    day = '01'

    # Read path
    read_path = f'{prefixPathRead}/metric={metricName}'

    # Write path
    write_path = f'{prefixPathWrite}/metric={metricName}'

    # Prerequisite - Create S3FileSystem in PyArrow
    # Why: Allows us to specify a custom endpoint
    AWS_ACCESS_KEY = "<Ceph S3 Creds Here>"
    AWS_SECRET_KEY = "<Ceph S3 Creds Here>"
    fs_pyarrow = pq.S3FileSystem(access_key=AWS_ACCESS_KEY, secret_key=AWS_SECRET_KEY, endpoint_override=endpoint)

    # Prerequisite - Specify day to compact 
    compactDay = date(2021, 1, 1)
    month = compactDay.month
    day = compactDay.day
    year = compactDay.year

    # (1/2) Read one days worth
    currentReadPath = f's3://{bucketName}/{read_path}/year={year}/month={month:02d}/day={day:02d}'
    print("Reading from:",currentReadPath)
    # Code here:
    # <Read dataframe>
    df = ray.data.read_parquet(paths=currentReadPath, filesystem=fs_pyarrow)

    
    # (2/2) Compact and write back to S3
    currentWritePath = f's3://{bucketName}/{write_path}/year={year}/month={month:02d}/day={day:02d}'
    print("Writing to:", currentWritePath)
    df.repartition(1).write_parquet(path=currentWritePath, filesystem=fs_pyarrow)

    return True



 
imports_op = components.create_component_from_func(
        imports, base_image='quay.io/thoth-station/s2i-ray-ml-notebook:v0.2.0')
ray_init_op = components.create_component_from_func(
        initialize_ray, base_image='quay.io/thoth-station/s2i-ray-ml-notebook:v0.2.0')

# Add secret volume
source_path: components.InputPath("k8s/ns/demo-ray/secrets/kubeflow-raydev-aws-secret/yaml")

@dsl.pipeline(
    name='test-pipeline',
    description='Sample attempt to upload a pipeline'
)


def sample_pipeline():
    importCheck = imports_op()
    with dsl.Condition(importCheck.output == True):
        ray_init_op()

if __name__ == '__main__':
    from kfp_tekton.compiler import TektonCompiler
    TektonCompiler().compile(sample_pipeline, __file__.replace('.py', '.yaml'))
