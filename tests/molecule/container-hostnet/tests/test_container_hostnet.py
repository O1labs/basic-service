def test_container_runs_on_host_network(host):
    container = host.docker("hostnet-container")
    assert container.is_running
    host_config = container.inspect()["HostConfig"]
    assert host_config["NetworkMode"] == "host"
    assert not host_config.get("PortBindings")
    assert {"NET_ADMIN", "NET_RAW"} <= set(host_config.get("CapAdd") or [])


def test_container_listens_on_host_stack(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening
