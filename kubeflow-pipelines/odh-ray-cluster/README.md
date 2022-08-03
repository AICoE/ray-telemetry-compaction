# Deploying Ray Cluster on OpenShift

Integration of [Ray](https://docs.ray.io/en/latest/index.html) with Open Data Hub on OpenShift to provision a ray cluster.
The ray operator and other components are based on https://docs.ray.io/en/releases-1.12.1/cluster/kubernetes.html

#### Components  of the Ray deployment

1. [Ray operator](./operator/ray-operator-deployment.yaml): The operator would process RayCluster resources and schedule ray head and worker pods based on requirements.
2. [Ray CR](./ray-custom-resources.yaml):  RayCluster CR would describe the desired state of ray cluster.
3. [Ray Cluster Deployer](./ray-deploy-kubeflow.yaml): Apply this file to start the Ray cluster, initially just the HEAD node. Worker nodes will scale up according to the task. Also includes Ray dashboard, which can be found under Routes.

Run "oc apply -k operator" to start the the Ray operator.\
Run "oc apply -f ray-custom-resources.yaml" and "oc apply -f ray-deploy-kubeflow.yaml" to get the Ray cluster head node up and running.


#### References

1. Deploying Ray with ODH Jupyterhub: https://github.com/harshad16/odh-manifests/tree/include-ray/jupyterhub/notebook-images/overlays/odh-ray-cluster
2. Ray-Operator: https://github.com/thoth-station/ray-operator
3. Ray-ml-worker: https://github.com/thoth-station/ray-ml-worker

