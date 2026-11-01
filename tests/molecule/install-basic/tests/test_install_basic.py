def test_binary_exists(host):
    binary = host.file("/usr/local/bin/jq-tool")
    assert binary.exists
    assert binary.mode == 0o755


def test_empty_override_falls_back_to_the_url_basename(host):
    binary = host.file("/usr/local/bin/jq-linux-amd64")
    assert binary.exists
    assert binary.mode == 0o755
    assert host.run("/usr/local/bin/jq-linux-amd64 --version").rc == 0


def test_staging_file_is_not_left_behind(host):
    assert not host.file("/tmp/jq-linux-amd64").exists


def test_service_not_exists(host):
    unit_file = host.file("/etc/systemd/system/test-tool.service")
    assert not unit_file.exists

    # systemctl is-enabled exits 4 when the unit is missing
    status = host.run("systemctl is-enabled test-tool")
    assert status.rc != 0
    assert "not-found" in status.stdout or status.rc == 4
