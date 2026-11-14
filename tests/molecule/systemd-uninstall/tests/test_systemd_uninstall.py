def test_service_removed(host):
    # Attempt to check if the service is enabled
    result = host.run("systemctl is-enabled sample-service")

    # Assert exit code 4 (service not found) or a valid non-enabled state
    assert result.rc in [0, 1, 4], (
        f"Unexpected exit code {result.rc} when checking service status. "
        f"stdout: {result.stdout}, stderr: {result.stderr}"
    )

    # Additional assertions based on the specific exit code
    if result.rc == 4:
        assert "not-found" in result.stdout, "Service should not exist after uninstallation"
    elif result.rc in [0, 1]:
        assert not result.stdout.strip() == "enabled", "Service should not be enabled after uninstallation"

def test_service_binary_removed(host):
    """Verify the service binary has been removed."""
    binary = host.file("/usr/bin/prometheus")
    assert not binary.exists, "The service binary still exists."


def test_systemd_service_file_removed(host):
    """Verify the systemd service file has been removed."""
    service_file = host.file("/etc/systemd/system/sample-service.service")
    assert not service_file.exists, "The systemd service file still exists."


def test_config_directory_removed(host):
    """Verify the configuration directory has been removed."""
    config_dir = host.file("/test/mnt/etc/prometheus")
    assert not config_dir.exists, "The configuration directory still exists."


def test_data_directory_removed(host):
    """Verify the data directory has been removed."""
    data_dir = host.file("/var/tmp/prometheus")
    assert not data_dir.exists, "The data directory still exists."


def test_temporary_binary_file_removed(host):
    """Verify the temporary binary file has been removed."""
    temp_binary = host.file("/tmp/prometheus-2.47.0.linux-amd64.tar.gz")
    assert not temp_binary.exists, "The temporary binary file still exists."


def test_systemd_dropin_directory_removed(host):
    """Verify uninstall removes the whole drop-in directory (O1#527)."""
    dropin_dir = host.file("/etc/systemd/system/sample-service.service.d")
    assert not dropin_dir.exists, "The systemd drop-in directory still exists."
