def test_service_running_and_enabled(host):
    service = host.service("test-service")
    # Check that the systemd service is running and enabled
    assert service.is_running
    assert service.is_enabled

def test_binary_exists(host):
    binary = host.file("/usr/local/bin/prometheus")
    # Check that the binary file exists and is executable
    assert binary.exists
    assert binary.mode == 0o755

def test_config_file_exists(host):
    config_file = host.file("/var/tmp/etc/prometheus/prometheus.yml")
    # Check that the configuration file exists with correct ownership
    assert config_file.exists
    assert config_file.user == "root"
    assert config_file.group == "root"
