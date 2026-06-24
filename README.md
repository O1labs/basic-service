<!-- @format -->

<p><img src="https://code.benco.io/icon-collection/logos/ansible.svg" alt="ansible logo" title="ansible" align="left" height="60" /></p>

# Basic-Service
[![Galaxy Role](https://img.shields.io/ansible/role/d/0x0i/basic_service)](https://galaxy.ansible.com/ui/standalone/roles/0x0i/basic_service/)
[![GitHub release (latest)](https://badgen.net/github/release/O1labs/basic-service)](https://github.com/O1labs/basic-service/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Configure and operate a basic cloud-native service: running anything from crypto blockchain clients to the immense app store of open-source ([Apache](https://projects.apache.org/projects.html), [CNCF](https://landscape.cncf.io/?group=projects-and-products&view-mode=grid) and beyond) services.

## Requirements

`Systemd`, installation of the `docker` engine or a `Kubernetes` cluster.

## Role Variables

### Common

|       var       |                        description                         |     default      |
| :-------------: | :--------------------------------------------------------: | :--------------: |
|   _setup_mode_   |  infrastructure provisioning setup mode (`container, k8s, systemd, install`)  |   `undefined`    |
|     _name_      |                 name of service to deploy                  |    **required**    |
|     _command_     |             Command and arguments to execute on startup              |    **required**    |
|     _user_     |             service user to setup              |    `<operating-user>`    |
|     _group_     |             service group to setup              |    `<operating-user>`    |
|    _config_     |  configuration files associated with the service to mount  |       `{}`       |
|   _config_env_   |  environment variables to set within the service runtime   |       `{}`       |
|     _ports_     |          listening port information for a service          |       `{}`       |
|    _data_dirs_    |  directory mappings to store service runtime/operational data |      `{}`      |
|  _host_data_dir_  |   host directory for general deployment operations    |    ``    |
|     _cpus_      |  CPU resources each deployed service can use (either percentage for systemd or cores for containers)   |      `100`       |
|    _memory_     | available memory resources each deployed service can use |       `1G`       |
| _restart_policy_ |                  service restart policy                  | `on-failure` |
|   _uninstall_   |    whether to remove installed service and artifacts    |     `false`      |

### Container

|       var       |                        description                         |     default      |
| :-------------: | :--------------------------------------------------------: | :--------------: |
|     _image_     |             service container image to deploy              |    ` `    |
|     _network_mode_     |             container network to attach ([more info](https://docs.ansible.com/ansible/latest/collections/community/docker/docker_container_module.html#parameter-network_mode))              |    `bridge `    |
|     _binary_url_     |             URL of the binary file or archive to download and bind-mount into the container              |    ` `    |
|     _binary_file_name_override_     |             Override the binary file name after moving it to the destination directory              |    ` `    |
|    _binary_strip_components_     | Strip NUMBER leading components/directories from file names on extraction | `0` |
|     _destination_directory_     |             host directory where the binary file will be placed after downloading/extracting              |    `/usr/local/bin`    |
|     _binary_app_path_     |             in-container mount path for the downloaded binary directory              |    `<destination_directory>`    |

### Systemd

|       var       |                        description                         |     default      |
| :-------------: | :--------------------------------------------------------: | :--------------: |
|     _binary_url_     |             URL of the binary file to download              |    ` `    |
|     _binary_file_name_override_     |             Override the binary file name after moving it to the destination directory              |    ` `    |
|    _binary_strip_components_     | Strip NUMBER leading components/directories from file names on extraction | `0` |
|     _destination_directory_     |             directory where the binary file will be placed after downloading/extracting              |    `/usr/local/bin`    |
|   _systemd_   |    custom service type & unit, service and install properties    |     `{}`      |
|   _systemd.enable_accounting_   |    enable systemd resource accounting (CPU, Memory, IO, Tasks, IP)    |     `true`      |

### Kubernetes (k8s)

To authorize access to the target Kubernetes cluster, set the following environment variables:
```bash
export KUBECONFIG=<path-to-the-kubeconfig-file>
export KUBE_CONTEXT=<context-within-the-kubeconfig-to-use>
```

|       var       |                        description                         |     default      |
| :-------------: | :--------------------------------------------------------: | :--------------: |
|     _helm_chart_path_     |             path to Helm chart to use for the service deployment/release              |    `helm` (resolved relative to the role)    |
|     _helm_namespace_      |  Kubernetes namespace to deploy to (also rendered into chart values)   |      `default`       |
|    _helm_values_path_     | optional Helm values overlay file merged after rendered role values |       `""`       |
| _helm_render_values_from_role_ | map common role vars (`image`, `config`, `ports`, `cpus`, `memory`, etc.) into Helm values | `true` |
| _helm_create_namespace_ | create the target namespace during Helm install | `true` |
| _helm_wait_ / _helm_atomic_ / _helm_timeout_ | Helm install safety controls | `true` / `true` / `10m` |

With `setup_mode: k8s`, the role renders Helm values from the same variables used by `container`, `systemd`, and `install` modes, then deploys the bundled chart. Set `helm_render_values_from_role: false` to use only `helm_values_path`.

## Containerized Apps
- [O1 Containers](https://github.com/O1labs/containers)
- [Dockerhub](https://hub.docker.com/search?q=)
- [Quay.io](https://quay.io/search)

## Dependencies

Install role and collection requirements:

```bash
ansible-galaxy install -r requirements.yml
```

See [requirements.yml](./requirements.yml) for the full list (includes `ansible-role-systemd` and `community.docker`).

## Example Playbook

One variable schema deploys to Docker, systemd, Kubernetes, or bare-binary install — swap `setup_mode` and keep `config`, `ports`, `data_dirs`, and resource limits. The role derives volume mounts, port mappings, iptables rules, systemd unit properties, and Helm values from those dicts so you avoid repeating `copy`, `get_url`, `docker_container`, and unit-file tasks in every playbook.

*All examples below are exercised in Molecule CI — see [tests/molecule/](./tests/molecule/).*

### Quick start — container

```yaml
- name: Serve nginx
  hosts: web
  become: true
  roles:
    - role: basic-service
      vars:
        setup_mode: container
        name: nginx
        image: nginx:latest
        command: nginx -g "daemon off;"
        cpus: 0.5
        memory: 128M
        ports:
          http:
            ingressPort: 8080
            servicePort: 80
```

### Full-featured systemd — Prometheus from a release tarball

Binary download, dedicated service user, inline config, environment, persistent data, firewall rules, and cgroup accounting — in one role block. The role auto-derives bind mounts, iptables ACCEPT rules, and a `systemd` unit with `CPUQuota`, `MemoryHigh`, and resource accounting.

```yaml
- name: Prometheus monitoring node
  hosts: monitoring
  become: true
  roles:
    - role: basic-service
      vars:
        setup_mode: systemd
        name: prometheus
        user: prometheus
        binary_url: https://github.com/prometheus/prometheus/releases/download/v2.47.0/prometheus-2.47.0.linux-amd64.tar.gz
        binary_strip_components: 1
        binary_file_name_override: prometheus
        destination_directory: /usr/local/bin
        command: >
          /usr/local/bin/prometheus
          --config.file=/var/lib/prometheus/etc/prometheus/prometheus.yml
          --storage.tsdb.path=/var/lib/prometheus/data
        cpus: 50
        memory: 512M
        host_data_dir: /var/lib/prometheus
        config:
          prometheus.yml:
            destinationPath: /etc/prometheus/prometheus.yml
            data: |
              global:
                scrape_interval: 15s
              scrape_configs:
                - job_name: prometheus
                  static_configs:
                    - targets: ["localhost:9090"]
        config_env:
          PROMETHEUS_STORAGE_PATH: /var/lib/prometheus/data
        data_dirs:
          prometheus_data:
            hostPath: /var/lib/prometheus/data
            appPath: /var/lib/prometheus/data
        ports:
          prometheus:
            ingressPort: 9090
            servicePort: 9090
        setup_iptables: true
        systemd:
          enable_accounting: true
```

### Kubernetes — same vars, different runtime

Set `KUBECONFIG` and `KUBE_CONTEXT` (see [Kubernetes variables](#kubernetes-k8s) above), then reuse the same `ports`, `cpus`, and `memory` shape. The role parses `command` into Helm `command`/`args` and converts resources into k8s requests/limits.

```yaml
- name: Prometheus on Kubernetes
  hosts: localhost
  connection: local
  roles:
    - role: basic-service
      vars:
        setup_mode: k8s
        name: prometheus
        image: prom/prometheus:v2.47.0
        helm_namespace: monitoring
        command: >
          --config.file=/etc/prometheus/prometheus.yml
          --storage.tsdb.path=/prometheus
        cpus: 0.5
        memory: 512M
        ports:
          prometheus:
            ingressPort: 9090
            servicePort: 9090
        config:
          prometheus.yml:
            destinationPath: /etc/prometheus/prometheus.yml
            data: |
              global:
                scrape_interval: 15s
        k8s_health_check_path: /-/healthy
```

To DRY a service across modes, use a YAML anchor and override only the runtime:

```yaml
vars:
  _prometheus: &prometheus
    name: prometheus
    command: --config.file=/etc/prometheus/prometheus.yml
    cpus: 0.5
    memory: 512M
    ports:
      prometheus: { ingressPort: 9090, servicePort: 9090 }
roles:
  - role: basic-service
    vars:
      <<: *prometheus
      setup_mode: container
      image: prom/prometheus:v2.47.0
  - role: basic-service
    vars:
      <<: *prometheus
      setup_mode: k8s
      helm_namespace: monitoring
```

### Ethereum Sepolia stack — execution + consensus clients

Play-level `vars` and `hostvars` wire Reth and Lighthouse on one host without hardcoded paths. `data_dirs` persists chain state; `ports` exposes RPC and metrics.

```yaml
- name: Ethereum Sepolia stack
  hosts: sepolia_nodes
  become: true
  vars:
    ethereum_network: sepolia
    ethereum_data_root: /var/lib/ethereum
    jwt_path: "{{ ethereum_data_root }}/jwt.hex"
  roles:
    - role: basic-service
      vars:
        setup_mode: systemd
        name: reth
        user: ethereum
        host_data_dir: "{{ ethereum_data_root }}/reth"
        binary_url: https://github.com/paradigmxyz/reth/releases/download/v1.1.4/reth-v1.1.4-x86_64-unknown-linux-gnu.tar.gz
        binary_file_name_override: reth
        command: >
          /usr/local/bin/reth node --chain {{ ethereum_network }}
          --datadir {{ ethereum_data_root }}/reth/data
          --authrpc.jwtsecret {{ jwt_path }}
          --http --http.addr 127.0.0.1 --http.port 8545
          --metrics 0.0.0.0:9001
        cpus: 80
        memory: 8G
        data_dirs:
          chain:
            hostPath: "{{ ethereum_data_root }}/reth/data"
            appPath: "{{ ethereum_data_root }}/reth/data"
        ports:
          metrics:
            ingressPort: 9001
            servicePort: 9001

    - role: basic-service
      vars:
        setup_mode: systemd
        name: lighthouse
        user: ethereum
        host_data_dir: "{{ ethereum_data_root }}/lighthouse"
        binary_url: https://github.com/sigp/lighthouse/releases/download/v6.0.0/lighthouse-v6.0.0-x86_64-unknown-linux-gnu.tar.gz
        binary_file_name_override: lighthouse
        command: >
          /usr/local/bin/lighthouse bn
          --network {{ ethereum_network }}
          --datadir {{ ethereum_data_root }}/lighthouse/data
          --checkpoint-sync-url https://checkpoint-sync.sepolia.ethpandaops.io
          --execution-endpoint http://127.0.0.1:8551
          --execution-jwt {{ jwt_path }}
          --http --http-address 127.0.0.1 --http-port 5052
          --metrics --metrics-address 0.0.0.0 --metrics-port 9002
        cpus: 50
        memory: 4G
        data_dirs:
          beacon:
            hostPath: "{{ ethereum_data_root }}/lighthouse/data"
            appPath: "{{ ethereum_data_root }}/lighthouse/data"
        ports:
          metrics:
            ingressPort: 9002
            servicePort: 9002
```

### Install and uninstall lifecycle

`setup_mode: install` downloads a binary without starting a service. Re-run with `uninstall: true` to tear down binaries, configs, data directories, containers, Helm releases, and iptables rules via handlers.

```yaml
- name: Install jq CLI
  hosts: all
  become: true
  roles:
    - role: basic-service
      vars:
        setup_mode: install
        name: jq
        binary_url: https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-amd64
        binary_file_name_override: jq

- name: Remove jq CLI
  hosts: all
  become: true
  roles:
    - role: basic-service
      vars:
        setup_mode: install
        name: jq
        binary_url: https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-amd64
        binary_file_name_override: jq
        uninstall: true
```

## License

MIT

## Author Information

This Ansible role was created in 2023 by O1.IO.

🏆 **always happy to help & donations are always welcome** 💸

- **ETH (Ethereum):** 0x652eD9d222eeA1Ad843efec01E60C29bF2CF6E4c

- **BTC (Bitcoin):** 3E8gMxwEnfAAWbvjoPVqSz6DvPfwQ1q8Jn

- **ATOM (Cosmos):** cosmos19vmcf5t68w6ug45mrwjyauh4ey99u9htrgqv09
