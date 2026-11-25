# Basic Service Chart

Helm chart that supports a basic, cloud-native containerized app in Kubernetes.

Chart version `0.0.1` (`helm/Chart.yaml`).

## Values

Defaults below match `helm/values.yaml`. Keys used by templates but omitted from that file are still settable and listed with empty defaults.

| Name                  | Description                                                                                    |                             Type                              | Default | Required |
| --------------------- | ---------------------------------------------------------------------------------------------- | :-----------------------------------------------------------: | :-----: | :------: |
| name                  | The service name                                                                               |                           `string`                            | `foo-service` |   yes    |
| namespace             | Namespace within Kubernetes cluster to deploy                                                  |                           `string`                            |  `foo`  |   yes    |
| createNamespace       | Whether to create the cluster namespace if it does not exist                                   |                            `bool`                             | `true`  |    no    |
| image                 | Container image of service release                                                             |                           `string`                            | `nginx:1.27` |   yes    |
| commonName            | Service common DNS name for which traffic external to the cluster should be sent to            |                 `string` (max 64 characters)                  | `foo-service.foo` |   yes    |
| command               | Container command/entrypoint override of service's base Docker image ENTRYPOINT                |                        `list(string)`                         |  `[]`   |    no    |
| args                  | Arguments to the command/entrypoint override                                                   |                        `list(string)`                         |  `[]`   |    no    |
| dockercfg             | Docker config secret name prefix (chart appends `-dockercfg`)                                  |                           `string`                            |   ``    |    no    |
| dockercfgOverride     | Docker config secret override reference (not including `-docker`/`-dockercfg` suffix)          |                           `string`                            |   ``    |    no    |
| imagePullSecrets      | Additional image pull secrets (list of `{name: …}` entries)                                    |                        `list(object)`                         |         |    no    |
| nameOverride          | Override the chart name used in helper labels                                                  |                           `string`                            |         |    no    |
| fullnameOverride      | Override the full resource name helper                                                         |                           `string`                            |         |    no    |
| serviceAccountName    | k8s service account/policy to associate with service                                           | `string` (use value `default` if no service account required) |   ``    |    no    |
| serviceType           | Type of k8s service object to provision (i.e. ClusterIP, NodePort, LoadBalancer, ExternalName) |                           `string`                            |   ``    |    no    |
| servicePort           | Port incoming service traffic is directed to and mapped to `serviceTargetPort`                 |                           `string`                            |   ``    |    no    |
| serviceTargetPort     | Port service is listening on inside the container                                              |                           `string`                            |   ``    |    no    |
| extraPorts            | Extra service port entries appended to ClusterIP and headless Services                         |                        `list(object)`                         |         |    no    |
| nodePorts             | Map of NodePort Service definitions                                                            |                            `dict`                             |         |    no    |
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
| clusterRoles          | Cluster-scoped RBAC Role/Binding definitions                                                   |                            `dict`                             |         |    no    |
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
| targetMemoryUtilizationPercentage | Deprecated: use `hpa.targetMemoryUtilizationPercentage` instead                    |                             `int`                             |         |    no    |
| livenessProbe         | Container liveness probe definition                                                          |                            `dict`                             |  `{}`   |    no    |
| readinessProbe        | Container readiness probe definition                                                         |                            `dict`                             |  `{}`   |    no    |
| startupProbe          | Container startup probe definition                                                           |                            `dict`                             |  `{}`   |    no    |
| livenessProbeRPCDaemon | Deprecated: use `livenessProbe` instead                                                     |                            `dict`                             |  `{}`   |    no    |
| readinessProbeRPCDaemon | Deprecated: use `readinessProbe` instead                                                   |                            `dict`                             |  `{}`   |    no    |
| ingress.enabled       | Whether to create an Ingress resource                                                        |                            `bool`                             | `false` |    no    |
| ingress.className     | Ingress class name                                                                             |                           `string`                            |         |    no    |
| ingress.annotations   | Ingress annotations                                                                            |                            `dict`                             |         |    no    |
| ingress.hosts         | Ingress host/path rules                                                                        |                        `list(object)`                         |         |    no    |
| ingress.tls           | Ingress TLS configuration                                                                      |                        `list(object)`                         |         |    no    |
| serviceMonitor.enabled | Whether to create a Prometheus Operator ServiceMonitor                                      |                            `bool`                             | `false` |    no    |
| serviceMonitor.port   | Service port name scraped by ServiceMonitor                                                    |                           `string`                            | `http`  |    no    |
| serviceMonitor.path    | Metrics path scraped by ServiceMonitor                                                        |                           `string`                            | `/metrics` | no    |
| serviceMonitor.interval | Scrape interval for ServiceMonitor                                                           |                           `string`                            | `30s`  |    no    |
| serviceMonitor.namespace | Namespace for the ServiceMonitor resource                                                  |                           `string`                            |         |    no    |
| serviceMonitor.labels | Extra labels on the ServiceMonitor                                                             |                            `dict`                             |         |    no    |
| serviceMonitor.annotations | Extra annotations on the ServiceMonitor                                                   |                            `dict`                             |         |    no    |
| serviceMonitor.jobLabel | Prometheus job label for the ServiceMonitor                                                  |                           `string`                            |         |    no    |
| serviceMonitor.endpoints | Custom scrape endpoint list (overrides default port/path endpoint)                          |                        `list(object)`                         |         |    no    |
| serviceMonitor.scrapeTimeout | Scrape timeout for ServiceMonitor endpoints                                            |                           `string`                            |         |    no    |
| serviceMonitor.scheme | Scrape scheme (`http` / `https`)                                                               |                           `string`                            |         |    no    |
| serviceMonitor.tlsConfig | TLS settings for scrape endpoints                                                           |                            `dict`                             |         |    no    |
| serviceMonitor.relabelings | Relabel configs for scrape endpoints                                                       |                             `list`                            |         |    no    |
| podDisruptionBudget   | PodDisruptionBudget settings (`minAvailable` / `maxUnavailable`)                               |                            `dict`                             |         |    no    |
