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

def initialize_Ray():

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
    return True
 
imports_op = components.create_component_from_func(
        imports, base_image='quay.io/thoth-station/s2i-ray-ml-notebook:v0.2.0')
ray_init_op = components.create_component_from_func(
        initialize_Ray, base_image='quay.io/thoth-station/s2i-ray-ml-notebook:v0.2.0')


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
