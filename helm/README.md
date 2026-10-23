# Basic Service Chart

Helm chart that supports a basic, cloud-native containerized app in Kubernetes.

## Values

| Name                                 | Description                                                                                     | Type               | Default | Required |
| ------------------------------------ | ----------------------------------------------------------------------------------------------- | :----------------: | :-----: | :------: |
| name                                 | The service name                                                                                | `string`           | `foo-service` | no |
| commonName                           | Service common DNS name for traffic external to the cluster                                      | `string`           | `foo-service.foo` | no |
| namespace                            | Namespace within the Kubernetes cluster to deploy                                               | `string`           | `foo` | no |
| clusterName                          | Name of Kubernetes cluster to deploy to                                                         | `string`           | `foo-cluster` | no |
| image                                | Container image of service release                                                              | `string`           | `nginx:1.27` | no |
| command                              | Container command/entrypoint override of service's base Docker image ENTRYPOINT                 | `list(string)`     | `[]` | no |
| args                                 | Arguments to the command/entrypoint override                                                    | `list(string)`     | `[]` | no |
| dockercfg                            | Enable an image pull secret named `<name>-dockercfg`                                            | `string`           | `null` | no |
| serviceAccountName                   | Kubernetes service account to associate with pods and RoleBindings                              | `string`           | `null` | no |
| serviceType                          | Type of Kubernetes Service to provision                                                         | `string`           | `null` | no |
| servicePort                          | Port incoming service traffic is directed to and mapped to `serviceTargetPort`                  | `int`              | `null` | no |
| serviceTargetPort                    | Port service is listening on inside the container                                               | `int`              | `null` | no |
| minReplicas                          | Lower limit for the number of replicas                                                          | `int`              | `1` | no |
| maxReplicas                          | Upper limit for the number of replicas                                                          | `int`              | `3` | no |
| createNamespace                      | Whether to create the cluster namespace if it does not exist                                    | `bool`             | `true` | no |
| hpa.enabled                          | Enable HorizontalPodAutoscaler (also auto-enabled when `maxReplicas` > `minReplicas`)           | `bool`             | `false` | no |
| hpa.targetCPUUtilizationPercentage   | CPU utilization target for autoscaling v2                                                       | `int`              | `50` | no |
| hpa.targetMemoryUtilizationPercentage | Optional memory utilization target for autoscaling v2                                           | `int`              | `null` | no |
| hpa.metrics                          | Additional autoscaling metrics                                                                  | `list(object)`     | `[]` | no |
| targetCPUUtilizationPercentage       | Deprecated fallback for `hpa.targetCPUUtilizationPercentage`                                    | `int`              | `50` | no |
| env.config                           | Environment variables to inject into the service container                                      | `dict`             | `{PLACEHOLDER: placeholder}` | no |
| secretEnv                            | Secret-backed environment variables; values are base64-encoded into a Secret                    | `dict`             | `{}` | no |
| extraEnv                             | Additional raw environment variable entries                                                     | `list(object)`     | `[]` | no |
| resources                            | Container resource requests and limits                                                          | `dict`             | `{}` | no |
| containerSecurityContext             | Container security context                                                                      | `dict`             | `{}` | no |
| livenessProbe                        | Container liveness probe definition                                                             | `dict`             | `{}` | no |
| readinessProbe                       | Container readiness probe definition                                                            | `dict`             | `{}` | no |
| startupProbe                         | Container startup probe definition                                                              | `dict`             | `{}` | no |
| livenessProbeRPCDaemon               | Deprecated liveness probe fallback                                                              | `dict`             | `{}` | no |
| readinessProbeRPCDaemon              | Deprecated readiness probe fallback                                                             | `dict`             | `{}` | no |
| ingress.enabled                      | Whether to create an Ingress resource                                                           | `bool`             | `false` | no |
| ingress.className                    | Ingress class name, when ingress is enabled                                                     | `string`           | `null` | no |
| ingress.annotations                  | Ingress annotations                                                                             | `dict`             | `null` | no |
| ingress.tls                          | Ingress TLS entries                                                                             | `list(object)`     | `null` | no |
| ingress.hosts                        | Ingress host and path rules                                                                     | `list(object)`     | `null` | no |
| serviceMonitor.enabled               | Whether to create a Prometheus Operator ServiceMonitor                                          | `bool`             | `false` | no |
| serviceMonitor.port                  | Service port name scraped by ServiceMonitor                                                     | `string`           | `http` | no |
| serviceMonitor.path                  | Metrics path scraped by ServiceMonitor                                                          | `string`           | `/metrics` | no |
| serviceMonitor.interval              | Scrape interval for the default ServiceMonitor endpoint                                         | `string`           | `30s` | no |
| serviceMonitor.namespace             | Namespace for the ServiceMonitor                                                                | `string`           | `.Values.namespace` | no |
| serviceMonitor.labels                | Extra labels for the ServiceMonitor                                                             | `dict`             | `null` | no |
| serviceMonitor.annotations           | Extra annotations for the ServiceMonitor                                                        | `dict`             | `null` | no |
| serviceMonitor.jobLabel              | ServiceMonitor job label                                                                        | `string`           | Helm release name | no |
| serviceMonitor.endpoints             | Custom ServiceMonitor endpoints                                                                 | `list(object)`     | `null` | no |
| serviceMonitor.scrapeTimeout         | ServiceMonitor scrape timeout                                                                   | `string`           | `null` | no |
| serviceMonitor.scheme                | ServiceMonitor scrape scheme                                                                    | `string`           | `http` | no |
| serviceMonitor.tlsConfig             | ServiceMonitor TLS configuration                                                                | `dict`             | `null` | no |
| serviceMonitor.relabelings           | ServiceMonitor relabeling rules                                                                 | `list(object)`     | `null` | no |
| initContainers                       | Container definitions to execute during service initialization                                  | `dict`             | `{}` | no |
| extraContainers                      | Additional container definitions to include with workloads                                      | `dict`             | `{}` | no |
| extraVolumes                         | Additional volume definitions to include within workloads                                       | `dict`             | `{}` | no |
| volumesFromConfigMaps                | Additional volumes to provision based on defined ConfigMaps                                     | `dict`             | `{}` | no |
| extraVolumeMounts                    | Additional volumeMount definitions to attach to service containers                              | `dict`             | `{}` | no |
| labels                               | Metadata labels to assign to resources                                                          | `dict`             | `{}` | no |
| annotations                          | Metadata annotations to assign to workloads                                                     | `dict`             | `{}` | no |
| configMaps                           | ConfigMap definitions to include with service deployments                                       | `dict`             | `{}` | no |
| serviceRoles                         | Namespaced RBAC Roles and RoleBindings                                                          | `dict`             | `{}` | no |
| clusterRoles                         | ClusterRoles and ClusterRoleBindings                                                            | `dict`             | `null` | no |
| deployStatefulSet                    | Whether to deploy a StatefulSet instead of a Deployment                                         | `bool`             | `false` | no |
| podManagementPolicy                  | StatefulSet pod management policy                                                               | `string`           | `OrderedReady` | no |
| statefulSetOptions.name              | StatefulSet volume claim template name                                                          | `string`           | `data` | no |
| statefulSetOptions.mountPath         | StatefulSet volume mount path                                                                   | `string`           | `/data` | no |
| statefulSetOptions.pvcName           | StatefulSet PVC label value                                                                     | `string`           | `ebs` | no |
| statefulSetOptions.pvcAccessMode     | StatefulSet volume claim access mode                                                            | `string`           | `ReadWriteOnce` | no |
| statefulSetOptions.pvcStorageClass   | StatefulSet volume claim storage class                                                          | `string`           | `gp3-ext4` | no |
| statefulSetOptions.pvcStorageCapacity | StatefulSet volume claim storage request                                                        | `string`           | `1Gi` | no |
| deployStrategy                       | Deployment strategy                                                                             | `dict`             | `{}` | no |
| updateStrategy                       | StatefulSet update strategy                                                                     | `dict`             | `{}` | no |
| nodeSelector                         | Pod node selector                                                                                | `dict`             | `{}` | no |
| affinity                             | Pod affinity                                                                                    | `dict`             | `{}` | no |
| tolerations                          | Pod tolerations                                                                                  | `list(object)`     | `[]` | no |
| terminationGracePeriodSeconds        | Pod termination grace period                                                                     | `int`              | `30` | no |
| storageClass                         | StorageClass resources to create                                                                | `list(object)`     | `[]` | no |
| persistentVolumeClaim                | PersistentVolumeClaim resources to create                                                       | `list(object)`     | `[]` | no |
| persistentVolume                     | PersistentVolume resources to create                                                            | `list(object)`     | `[]` | no |
| dockercfgOverride                    | Docker config secret override reference (not including `-dockercfg` suffix)                    | `string`           | `null` | no |
| imagePullSecrets                     | Explicit pod imagePullSecrets entries                                                           | `list(object)`     | `null` | no |
| nodePorts                            | NodePort Service entries for StatefulSet pod-specific ports                                     | `dict`             | `null` | no |
| extraPorts                           | Additional Service port entries                                                                 | `list(object)`     | `null` | no |
| podDisruptionBudget                  | PodDisruptionBudget settings (`minAvailable` / `maxUnavailable`)                                | `dict`             | `null` | no |
| nameOverride                         | Name override used by the chart helper                                                          | `string`           | `null` | no |
| fullnameOverride                     | Full name override used by the chart helper                                                     | `string`           | `null` | no |
