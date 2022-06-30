# Ray Telemetry data compaction

### What: 
Compacting multiple `.parquet` files using Ray
### Why: 
Improving Read/write performance by reducing the overall number of files

---

## The Jupyter Notebook
Code for compaction can be found in `Ray-Only.py`.
Required packages are listed in `Requirements.txt`.

## Breaking down the code
### Initial setup
Ensure pip is upto date, and installs the dependencies in Requirements.txt.
>`pip install --upgrade pip` \
`!pip install -r Requirements.txt`

Check whether AWS credentials are correct
>`!aws configure list`

Import packages 
>`from ray.util import inspect_serializability` \
`import ray` \
`import pyarrow.fs as pq`\
`import pandas as pd`

### Ray code to read & write parquet files

Create a filesystem object which can specify the access key, secret key and a custom endpoint. Can be skipped if endpoint needn't be specified and credentials are present in awscli.
>`fs_pyarrow = pq.S3FileSystem(endpoint_override=<your-custom-endpoint>)`

Read parquet files from remote path
> `df = ray.data.read_parquet(paths=path/to/parquet, filesystem=fs_pyarrow)`

*Note: Specifying paths to multiple directories does not work with `read_parquet`. Issue and workaround: https://github.com/ray-project/ray/issues/24598*

Write back a single parquet file. `.repartition(<number-of-files>)` is where number of files can be specified. 
> `df.repartition(1).write_parquet(path=path/to/destination, filesystem=fs_pyarrow)`

## Ray Cluster Setup

### What:
Setup a Ray cluster on OpenShift, and add a JupyterHub notebook image that can connect to it.\
Refer this PR: https://github.com/opendatahub-io/odh-manifests/pull/573 \
Running the kustomize script sets up the Ray operator, and adds the `ray-ml-notebook` image to ODH JupyterHub.

## Misc

You can access the Ray dashboard via OpenShift: Networking -> Routes.










