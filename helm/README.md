# Basic Service Chart

Helm chart that supports a basic, cloud-native containerized app in Kubernetes.

Chart version `0.0.1` (`helm/Chart.yaml`).

## Values

Defaults below match `helm/values.yaml`. Keys used by templates but omitted from that file are still settable and listed with empty defaults.

| Name                  | Description                                                                                    |                             Type                              | Default | Required |
| --------------------- | ---------------------------------------------------------------------------------------------- | :-----------------------------------------------------------: | :-----: | :------: |
| name                  | The service name                                                                               |                           `string`                            | `foo-service` |   yes    |
| clusterName           | Name of Kubernetes cluster to deploy to                                                        |                           `string`                            | `foo-cluster` |   yes    |
| namespace             | Namespace within Kubernetes cluster to deploy                                                  |                           `string`                            |  `foo`  |   yes    |
| createNamespace       | Whether to create the cluster namespace if it does not exist                                   |                            `bool`                             | `true`  |    no    |
| image                 | Container image of service release                                                             |                           `string`                            | `nginx:1.27` |   yes    |
| commonName            | Service common DNS name for which traffic external to the cluster should be sent to            |                 `string` (max 64 characters)                  | `foo-service.foo` |   yes    |
| command               | Container command/entrypoint override of service's base Docker image ENTRYPOINT                |                        `list(string)`                         |  `[]`   |    no    |
| args                  | Arguments to the command/entrypoint override                                                   |                        `list(string)`                         |  `[]`   |    no    |
| dockercfg             | Docker config secret name prefix (chart appends `-dockercfg`)                                  |                           `string`                            |   ``    |    no    |
| dockercfgOverride     | Docker config secret override reference (not including `-docker`/`-dockercfg` suffix)          |                           `string`                            |   ``    |    no    |
| serviceAccountName    | k8s service account/policy to associate with service                                           | `string` (use value `default` if no service account required) |   ``    |    no    |
| serviceType           | Type of k8s service object to provision (i.e. ClusterIP, NodePort, LoadBalancer, ExternalName) |                           `string`                            |   ``    |    no    |
| servicePort           | Port incoming service traffic is directed to and mapped to `serviceTargetPort`                 |                           `string`                            |   ``    |    no    |
| serviceTargetPort     | Port service is listening on inside the container                                              |                           `string`                            |   ``    |    no    |
| minReplicas           | Lower limit for the number of replicas to which the autoscaler can scale down                  |                             `int`                             |   `1`   |    no    |
| maxReplicas           | Upper limit for the number of replicas to which the autoscaler can scale up                    |                             `int`                             |   `3`   |    no    |
| env.config            | Set of environment variables to inject into the service's container runtime                    |                            `dict`                             | `{PLACEHOLDER: placeholder}` |    no    |
| secretEnv             | Sensitive environment variables rendered into a Secret and injected into the container         |                            `dict`                             |  `{}`   |    no    |
| extraEnv              | Additional env entries (raw list) merged into the container env                                |                        `list(object)`                         |  `[]`   |    no    |
| resources             | Container resource requests and limits                                                         |                            `dict`                             |  `{}`   |    no    |
| containerSecurityContext | Container-level securityContext                                                             |                            `dict`                             |  `{}`   |    no    |
| initContainers        | Container definitions to execute during service initialization                                 |                            `dict`                             |  `{}`   |    no    |
| extraContainers       | Additional container definitions to include with service deployments                           |                            `dict`                             |  `{}`   |    no    |
| configMaps            | ConfigMap definitions to include with service deployments                                      |                            `dict`                             |  `{}`   |    no    |
| extraVolumes          | Additional volume definitions to include within service deployments                            |                            `dict`                             |  `{}`   |    no    |
| extraVolumeMounts     | Additional volumeMount definitions to attach to service containers                             |                            `dict`                             |  `{}`   |    no    |
| volumesFromConfigMaps | Additional volumes to provision based on defined configMaps                                    |                            `dict`                             |  `{}`   |    no    |
| labels                | Collection of metadata labels to assign to service deployments                                 |                            `dict`                             |  `{}`   |    no    |
| annotations           | Collection of metadata annotations to assign to service deployments                            |                            `dict`                             |  `{}`   |    no    |
| serviceRoles          | RBAC policies and associated service account bindings                                          |                            `dict`                             |  `{}`   |    no    |
| deployStatefulSet     | Whether to deploy a service as a k8s StatefulSet or standard Deployment workload               |                            `bool`                             | `false` |    no    |
| podManagementPolicy   | StatefulSet pod management policy                                                              |                           `string`                            | `OrderedReady` | no |
| statefulSetOptions    | volume claim and other options associated with StatefulSet deployments                         |                            `dict`                             | `{name: data, mountPath: /data, pvcName: ebs, pvcAccessMode: ReadWriteOnce, pvcStorageClass: gp3-ext4, pvcStorageCapacity: 1Gi}` |    no    |
| deployStrategy        | The deployment strategy to use to replace existing pods with new ones                          |                            `dict`                             |  `{}`   |    no    |
| updateStrategy        | StatefulSet update strategy                                                                    |                            `dict`                             |  `{}`   |    no    |
| nodeSelector          | Pod nodeSelector                                                                               |                            `dict`                             |  `{}`   |    no    |
| affinity              | Pod affinity/anti-affinity                                                                     |                            `dict`                             |  `{}`   |    no    |
| tolerations           | Pod tolerations                                                                                |                        `list(object)`                         |  `[]`   |    no    |
| terminationGracePeriodSeconds | Pod termination grace period                                                         |                             `int`                             |  `30`   |    no    |
| persistentVolumeClaim | persistent volume claim that will be mounted to deployment                                     |                        `list(object)`                         |  `[]`   |    no    |
| persistentVolume      | persistent volume that the pvc can use                                                         |                        `list(object)`                         |  `[]`   |    no    |
| storageClass          | storage class that the pvc can use                                                             |                        `list(object)`                         |  `[]`   |    no    |
| hpa.enabled           | Enable HorizontalPodAutoscaler (also auto-enabled when `maxReplicas` > `minReplicas`)          |                            `bool`                             | `false` |    no    |
| hpa.targetCPUUtilizationPercentage | CPU utilization target for autoscaling v2                                             |                             `int`                             |  `50`   |    no    |
| hpa.targetMemoryUtilizationPercentage | Optional memory utilization target for autoscaling v2                              |                             `int`                             |         |    no    |
| hpa.metrics           | Additional HPA metric specs                                                                    |                             `list`                            |  `[]`   |    no    |
| targetCPUUtilizationPercentage | Deprecated: use `hpa.targetCPUUtilizationPercentage` instead                          |                             `int`                             |  `50`   |    no    |
| livenessProbe         | Container liveness probe definition                                                          |                            `dict`                             |  `{}`   |    no    |
| readinessProbe        | Container readiness probe definition                                                         |                            `dict`                             |  `{}`   |    no    |
| startupProbe          | Container startup probe definition                                                           |                            `dict`                             |  `{}`   |    no    |
| livenessProbeRPCDaemon | Deprecated: use `livenessProbe` instead                                                     |                            `dict`                             |  `{}`   |    no    |
| readinessProbeRPCDaemon | Deprecated: use `readinessProbe` instead                                                   |                            `dict`                             |  `{}`   |    no    |
| ingress.enabled       | Whether to create an Ingress resource                                                        |                            `bool`                             | `false` |    no    |
| serviceMonitor.enabled | Whether to create a Prometheus Operator ServiceMonitor                                      |                            `bool`                             | `false` |    no    |
| serviceMonitor.port   | Service port name scraped by ServiceMonitor                                                    |                           `string`                            | `http`  |    no    |
| serviceMonitor.path    | Metrics path scraped by ServiceMonitor                                                        |                           `string`                            | `/metrics` | no    |
| serviceMonitor.interval | Scrape interval for ServiceMonitor                                                           |                           `string`                            | `30s`  |    no    |
| podDisruptionBudget   | PodDisruptionBudget settings (`minAvailable` / `maxUnavailable`)                               |                            `dict`                             |         |    no    |
