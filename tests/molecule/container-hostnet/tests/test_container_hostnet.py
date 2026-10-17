def test_container_running(host):
    container = host.docker("hostnet-container")
    assert container.is_running


def test_container_uses_host_network(host):
    host_config = host.docker("hostnet-container").inspect()["HostConfig"]
    assert host_config["NetworkMode"] == "host"


def test_container_publishes_no_ports(host):
    host_config = host.docker("hostnet-container").inspect()["HostConfig"]
    assert not host_config.get("PortBindings")


def test_container_adds_capabilities(host):
    host_config = host.docker("hostnet-container").inspect()["HostConfig"]
    cap_add = host_config.get("CapAdd") or []
    assert {"NET_ADMIN", "NET_RAW"} <= set(cap_add)


def test_container_listens_on_host_stack(host):
    # nginx binds :80 directly on the host network namespace.
    assert host.socket("tcp://0.0.0.0:80").is_listening
