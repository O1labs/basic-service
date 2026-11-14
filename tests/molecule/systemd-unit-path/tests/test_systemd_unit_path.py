def test_unit_removed_from_configured_path(host):
    """Verify uninstall removes the unit from systemd.unit_path, not /etc."""
    unit = host.file("/run/systemd/system/probe-service.service")
    assert not unit.exists, "The unit was not removed from the configured unit_path."


def test_dropin_directory_removed_from_configured_path(host):
    """Verify uninstall removes the drop-in directory at the configured path."""
    dropin_dir = host.file("/run/systemd/system/probe-service.service.d")
    assert not dropin_dir.exists, (
        "The drop-in directory was not removed from the configured unit_path."
    )


def test_nothing_written_to_default_unit_path(host):
    """Verify a non-default unit_path is used exclusively."""
    default = host.file("/etc/systemd/system/probe-service.service")
    assert not default.exists, "The unit was written to the default /etc path."


def test_service_not_known_after_uninstall(host):
    """Verify systemd no longer knows the unit after uninstall."""
    result = host.run("systemctl show probe-service -p LoadState")
    assert result.rc == 0, f"systemctl show failed: {result.stderr}"
    assert "LoadState=not-found" in result.stdout, (
        f"Unexpected LoadState: {result.stdout}"
    )