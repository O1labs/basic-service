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

- Launch a Wireguard client which establishes a secure peer tunnel connection:

```yaml
- name: Configure WireGuard VPN
  hosts: VPNServers
  remote_user: devops
  become: true
  roles:
    - role: basic-service
      vars:
        setup_mode: systemd
        name: wireguard
        user: wireguard
        binary_url: https://git.zx2c4.com/wireguard-tools/snapshot/wireguard-tools-1.0.20210424.tar.xz
        binary_file_name_override: wireguard
        command: >
          /usr/local/bin/wg-quick up wg0
        cpus: 50
        memory: 1G
        config:
          wg0.conf:
            destinationPath: /etc/wireguard/wg0.conf
            data: |
              [Interface]
              PrivateKey = <Your-Private-Key>
              Address = 10.0.0.1/24
              ListenPort = 51820

              [Peer]
              PublicKey = <Peer-Public-Key>
              Endpoint = <Peer-Public-IP>:51820
              AllowedIPs = 10.0.0.2/32
        ports:
          wireguard:
            ingressPort: 51820
            servicePort: 51820
        systemd:
          enable_accounting: true
          service_properties:
            ExecStop: /usr/local/bin/wg-quick down wg0
            Restart: on-failure
```

- Provision an Ethereum execution and consensus client connected to the Sepolia testnet and monitor with the XATU service

```yaml
- name: Configure Ethereum execution layer clients
  hosts: EthereumSepolia
  become: true
  roles:
    - role: basic-service
      vars:
        setup_mode: systemd
        name: reth
        user: ubuntu
        binary_url: https://github.com/paradigmxyz/reth/releases/download/v1.1.4/reth-v1.1.4-x86_64-unknown-linux-gnu.tar.gz
        binary_file_name_override: reth
        command: >
          /usr/local/bin/reth node --full --chain=sepolia --http --http.addr 0.0.0.0 --http.api "admin,debug,eth,net,txpool,web3,rpc,reth,ots,flashbots,miner" --metrics 0.0.0.0:8085
        cpus: 50
        memory: 5G
        config:
          reth.toml:
            destinationPath: /home/ubuntu/reth.toml
            data: |
              # add configuration values

- name: Configure Ethereum consensus layer clients
  hosts: EthereumSepolia
  become: true
  roles:
    - role: basic-service
      vars:
        setup_mode: systemd
        name: lighthouse
        user: ubuntu
        binary_url: https://github.com/sigp/lighthouse/releases/download/v6.0.0/lighthouse-v6.0.0-x86_64-unknown-linux-gnu.tar.gz
        binary_file_name_override: lighthouse
        command: >
          lighthouse bn --network sepolia --checkpoint-sync-url https://checkpoint-sync.sepolia.ethpandaops.io/
          --execution-endpoint http://localhost:8551 --execution-jwt /home/ahmad/.local/share/reth/sepolia/jwt.hex
          --http --http-address 0.0.0.0
          --metrics --metrics-address 0.0.0.0 --metrics-port 8086
        cpus: 50
        memory: 5G

- name: Configure XATU server for analytics
  hosts: EthereumSepolia
  become: true
  roles:
    - role: basic-service
      vars:
        setup_mode: container
        name: xatu-server
        image: ethpandaops/xatu:latest
        command: sentry --preset ethpandaops --beacon-node-url=http://localhost:5052 --output-authorization="Basic <redacted>"
        cpus: 0.5
        memory: 5g
        network_mode: host
```

- Run a downloaded binary inside a container (e.g. Prometheus from a release archive):

```yaml
- name: Configure Prometheus in a container
  hosts: Monitoring
  become: true
  roles:
    - role: basic-service
      vars:
        setup_mode: container
        name: prometheus
        image: debian:bookworm-slim
        binary_url: https://github.com/prometheus/prometheus/releases/download/v2.47.0/prometheus-2.47.0.linux-amd64.tar.gz
        binary_strip_components: 1
        binary_file_name_override: prometheus
        destination_directory: /usr/local/bin
        command: >
          /usr/local/bin/prometheus --config.file=/etc/prometheus/prometheus.yml
          --storage.tsdb.path=/prometheus --web.listen-address=0.0.0.0:9090
        ports:
          prometheus:
            ingressPort: 9090
            servicePort: 9090
        host_data_dir: /var/lib/prometheus
        config:
          prometheus.yml:
            destinationPath: /etc/prometheus/prometheus.yml
            data: |
              global:
                scrape_interval: 15s
        data_dirs:
          prometheus-data:
            hostPath: /var/lib/prometheus/data
            appPath: /prometheus
```

- Install a tool (e.g. `curl`):

```yaml
- name: Install curl tool
  hosts: all
  become: true
  roles:
    - role: basic-service
      vars:
        setup_mode: install
        name: curl
        binary_url: https://github.com/moparisthebest/static-curl/releases/download/v8.12.1/curl-amd64
        binary_strip_components: 1
        binary_file_name_override: curl
```

## License

MIT

## Author Information

This Ansible role was created in 2023 by O1.IO.

🏆 **always happy to help & donations are always welcome** 💸

- **ETH (Ethereum):** 0x652eD9d222eeA1Ad843efec01E60C29bF2CF6E4c

- **BTC (Bitcoin):** 3E8gMxwEnfAAWbvjoPVqSz6DvPfwQ1q8Jn

- **ATOM (Cosmos):** cosmos19vmcf5t68w6ug45mrwjyauh4ey99u9htrgqv09
