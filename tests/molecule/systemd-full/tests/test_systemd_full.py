def test_systemd_service_exists(host):
    """Verify that the systemd service file exists."""
    service_file = host.file("/etc/systemd/system/test-service.service")
    assert service_file.exists, "The systemd service file does not exist."
    assert service_file.is_file, "The systemd service file is not a regular file."


def test_systemd_service_properties(host):
    """Verify the systemd service properties match the role configuration."""
    service_content = host.file("/etc/systemd/system/test-service.service").content_string

    # Verify key systemd properties
    assert "ExecStart=/usr/bin/prometheus --config.file=/test/mnt/etc/prometheus/prometheus.yml" in service_content, "ExecStart is not correctly set."
    assert "User=prometheus" in service_content, "The service user is not correctly set to prometheus."
    assert "CPUQuota=50%" in service_content, "CPUQuota is not correctly set."
    assert "MemoryHigh=512M" in service_content, "MemoryHigh is not correctly set."
    assert "Restart=on-failure" in service_content, "Restart policy is not correctly set."


def test_systemd_service_status(host):
    """Verify the systemd service is active and enabled."""
    service = host.service("test-service")
    assert service.is_running, "The systemd service is not running."
    assert service.is_enabled, "The systemd service is not enabled."

def test_systemd_service_environment_variables(host):
    """Verify environment variables set in the systemd service file."""
    service_content = host.file("/etc/systemd/system/test-service.service").content_string

    # Verify environment directive
    assert "Environment=" in service_content, "Environment variables are not set in the service file."
    assert "PROMETHEUS_STORAGE_PATH=/prometheus" in service_content, "Expected environment variable is missing."

def test_systemd_service_config_files(host):
    """Verify the service configuration files exist with required settings."""
    config_file = host.file("/test/mnt/etc/prometheus/prometheus.yml")
    assert config_file.exists, "The Prometheus configuration file does not exist."

    config_content = config_file.content_string.strip()

    # Verify key settings are present in the configuration file
    assert "global:" in config_content, "The 'global' section is missing in the configuration file."
    assert "scrape_interval: 15s" in config_content, "The 'scrape_interval' setting is missing or incorrect."
    assert "evaluation_interval: 15s" in config_content, "The 'evaluation_interval' setting is missing or incorrect."
    assert "scrape_configs:" in config_content, "The 'scrape_configs' section is missing in the configuration file."
    assert "- job_name: prometheus" in config_content, "The 'prometheus' job is missing in the scrape_configs section."
    assert 'targets: ["localhost:9090"]' in config_content, "The target 'localhost:9090' is missing in the scrape_configs section."

def test_binary_file_exists_and_executable(host):
    """Verify that the service binary exists and is executable."""
    binary = host.file("/usr/bin/prometheus")
    assert binary.exists, "The service binary does not exist."
    assert binary.is_file, "The service binary is not a regular file."
    assert binary.mode & 0o111, "The service binary is not executable."


def test_data_directory_exists(host):
    """Verify the data directory exists with correct permissions."""
    data_dir = host.file("/var/tmp/prometheus")
    assert data_dir.exists, "The data directory does not exist."
    assert data_dir.is_directory, "The data directory is not a directory."
    assert data_dir.user == "prometheus", "The data directory is not owned by prometheus."
    assert data_dir.group == "prometheus", "The data directory group is not prometheus."


def test_service_logs_no_errors(host):
    """Verify that the systemd service logs contain no errors."""
    logs = host.run("journalctl -u test-service --no-pager --since '1 hour ago'")
    assert logs.rc == 0, "Failed to fetch systemd logs for the service."
    assert "error" not in logs.stdout.lower(), "Systemd logs contain errors."
    assert "failed" not in logs.stdout.lower(), "Systemd logs indicate failure."

def test_iptables_prometheus_port(host):
    """Verify that the ingress ports are allowed in iptables."""
    # Check if the iptables rule for port 9090 exists
    iptables_output = host.run("iptables -L INPUT -v -n")
    assert iptables_output.rc == 0, "Failed to list iptables rules."

    # Verify that the rule allowing TCP traffic on port 9090 exists
    assert "9090" in iptables_output.stdout, "The iptables rule for port 9090 is missing."

def test_systemd_ip_accounting(host):
    """Verify that IP accounting is enabled and working."""
    service_content = host.file("/etc/systemd/system/test-service.service").content_string
    assert "IPAccounting=yes" in service_content, "IPAccounting directive is missing from the service file."

    # Verify systemd tracks network data
    accounting_output = host.run("systemctl show test-service --property=IPIngressBytes,IPEgressBytes")
    assert accounting_output.rc == 0, "Failed to get IP accounting data from systemd."
    assert "IPIngressBytes=" in accounting_output.stdout and "IPEgressBytes=" in accounting_output.stdout, "IP accounting data is not available."

def test_service_group_exists(host):
    """Verify that the prometheus service group was created."""
    group = host.group("prometheus")
    assert group.exists, "The prometheus group does not exist."
    # System groups typically have GID < 1000
    assert group.gid < 1000, f"The prometheus group is not a system group (GID: {group.gid})."

def test_service_user_exists(host):
    """Verify that the prometheus service user was created."""
    user = host.user("prometheus")
    assert user.exists, "The prometheus user does not exist."
    assert user.shell == "/usr/sbin/nologin", "The prometheus user shell is not set to /usr/sbin/nologin."
    assert user.group == "prometheus", "The prometheus user is not in the prometheus group."
    # System users typically have UID < 1000
    assert user.uid < 1000, f"The prometheus user is not a system user (UID: {user.uid})."

def test_config_file_ownership(host):
    """Verify that config files are owned by the prometheus user."""
    config_file = host.file("/test/mnt/etc/prometheus/prometheus.yml")
    assert config_file.exists, "The Prometheus configuration file does not exist."
    assert config_file.user == "prometheus", "The config file is not owned by prometheus."
    assert config_file.group == "prometheus", "The config file group is not prometheus."

def test_stale_dropin_removed(host):
    """Verify O1#527: a redeploy prunes drop-ins the role did not write."""
    stale = host.file("/etc/systemd/system/test-service.service.d/cpu.conf")
    assert not stale.exists, "The stale drop-in was not pruned on redeploy."


def test_symlinked_dropin_removed(host):
    """Verify a symlinked stale drop-in is pruned; systemd follows these."""
    linked = host.file("/etc/systemd/system/test-service.service.d/linked.conf")
    assert not linked.exists, "The symlinked stale drop-in was not pruned."


def test_keep_listed_dropin_preserved(host):
    """Verify a drop-in named in systemd.keep_dropins survives a redeploy."""
    operator = host.file("/etc/systemd/system/test-service.service.d/operator.conf")
    assert operator.exists, "The keep-listed drop-in was removed."


def test_pruned_dropin_does_not_override_catalog_values(host):
    """Verify the effective unit matches the catalog, not the seeded drop-in.

    The seeded drop-in set CPUQuota=400% and Restart=always; the role asks for
    50% and on-failure, so these would fail if the drop-in survived.
    """
    quota = host.run("systemctl show test-service -p CPUQuotaPerSecUSec --value")
    assert quota.rc == 0, f"Could not read CPUQuota: {quota.stderr}"
    assert quota.stdout.strip() == "500ms", (
        f"Effective CPUQuota is {quota.stdout.strip()!r}, expected 500ms (50%); "
        "a stale drop-in is still overriding the unit."
    )

    restart = host.run("systemctl show test-service -p Restart --value")
    assert restart.rc == 0, f"Could not read Restart: {restart.stderr}"
    assert restart.stdout.strip() == "on-failure", (
        f"Effective Restart is {restart.stdout.strip()!r}, expected on-failure."
    )

    # The symlinked drop-in set MemoryMax=9G; the role renders no MemoryMax.
    mem_max = host.run("systemctl show test-service -p MemoryMax --value")
    assert mem_max.rc == 0, f"Could not read MemoryMax: {mem_max.stderr}"
    assert mem_max.stdout.strip() == "infinity", (
        f"Effective MemoryMax is {mem_max.stdout.strip()!r}; the symlinked "
        "drop-in is still overriding the unit."
    )


def test_keep_listed_dropin_still_applies(host):
    """Verify the preserved drop-in is actually loaded by systemd."""
    nice = host.run("systemctl show test-service -p Nice --value")
    assert nice.rc == 0, f"Could not read Nice: {nice.stderr}"
    assert nice.stdout.strip() == "5", (
        f"Effective Nice is {nice.stdout.strip()!r}, expected 5 from operator.conf."
    )
