import random
from time import sleep

import pytest
import strongdm
from tests.conftest import get_resource_postgres


# def test_delete_resources(client):
#     """
#     Quickly delete resources
#     """
#     resources = list(client.resources.list('healthy:false'))
#     for resource in resources:
#         client.resources.delete(resource.id)


def get_resource_gateway(hostname: str = "apple.berry.com", port: int = None) -> strongdm.Gateway:
    """
    Get a prepopulated gateway resource
    :param hostname: str
    :param port: int
    :return: strongdm.Gateway
    """
    if not port:
        port = random.randint(5000, 7000)

    gateway = strongdm.Gateway(
        name=f"gateway{port}",
        listen_address=f"{hostname}:{port}"
    )
    return gateway


def get_resource_relay(num: int = None) -> strongdm.Relay:
    """
    Get a prepopulated relay resource
    :param num: int
    :return: strongdm.Relay
    """
    if not num:
        num = random.randint(5000, 7000)

    relay = strongdm.Relay(
        name=f"relay{num}",
    )
    return relay


def get_resource_k8_cluster(num: int = None, certificate_authority: str = None) -> strongdm.AmazonEKS:
    """
    Get a prepopulated k8 cluster resource
    :param num: int
    :param certificate_authority: str
    :return: strongdm.AmazonEKS
    """
    if not num:
        num = random.randint(5000, 7000)

    if not certificate_authority:
        certificate_authority = """-----BEGIN CERTIFICATE-----
MIIEKjCCAxKgAwIBAgIEOGPe+DANBgkqhkiG9w0BAQUFADCBtDEUMBIGA1UEChMLRW50cnVzdC5u
ZXQxQDA+BgNVBAsUN3d3dy5lbnRydXN0Lm5ldC9DUFNfMjA0OCBpbmNvcnAuIGJ5IHJlZi4gKGxp
bWl0cyBsaWFiLikxJTAjBgNVBAsTHChjKSAxOTk5IEVudHJ1c3QubmV0IExpbWl0ZWQxMzAxBgNV
BAMTKkVudHJ1c3QubmV0IENlcnRpZmljYXRpb24gQXV0aG9yaXR5ICgyMDQ4KTAeFw05OTEyMjQx
NzUwNTFaFw0yOTA3MjQxNDE1MTJaMIG0MRQwEgYDVQQKEwtFbnRydXN0Lm5ldDFAMD4GA1UECxQ3
d3d3LmVudHJ1c3QubmV0L0NQU18yMDQ4IGluY29ycC4gYnkgcmVmLiAobGltaXRzIGxpYWIuKTEl
MCMGA1UECxMcKGMpIDE5OTkgRW50cnVzdC5uZXQgTGltaXRlZDEzMDEGA1UEAxMqRW50cnVzdC5u
ZXQgQ2VydGlmaWNhdGlvbiBBdXRob3JpdHkgKDIwNDgpMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A
MIIBCgKCAQEArU1LqRKGsuqjIAcVFmQqK0vRvwtKTY7tgHalZ7d4QMBzQshowNtTK91euHaYNZOL
Gp18EzoOH1u3Hs/lJBQesYGpjX24zGtLA/ECDNyrpUAkAH90lKGdCCmziAv1h3edVc3kw37XamSr
hRSGlVuXMlBvPci6Zgzj/L24ScF2iUkZ/cCovYmjZy/Gn7xxGWC4LeksyZB2ZnuU4q941mVTXTzW
nLLPKQP5L6RQstRIzgUyVYr9smRMDuSYB3Xbf9+5CFVghTAp+XtIpGmG4zU/HoZdenoVve8AjhUi
VBcAkCaTvA5JaJG/+EfTnZVCwQ5N328mz8MYIWJmQ3DW1cAH4QIDAQABo0IwQDAOBgNVHQ8BAf8E
BAMCAQYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUVeSB0RGAvtiJuQijMfmhJAkWuXAwDQYJ
KoZIhvcNAQEFBQADggEBADubj1abMOdTmXx6eadNl9cZlZD7Bh/KM3xGY4+WZiT6QBshJ8rmcnPy
T/4xmf3IDExoU8aAghOY+rat2l098c5u9hURlIIM7j+VrxGrD9cv3h8Dj1csHsm7mhpElesYT6Yf
zX1XEC+bBAlahLVu2B064dae0Wx5XnkcFMXj0EyTO2U87d89vqbllRrDtRnDvV5bu/8j72gZyxKT
J1wDLW8w0B62GqzeWvfRqqgnpv55gcR5mTNXuhKwqeBCbJPKVt7+bYQLCIt+jerXmCHG8+c8eS9e
nNFMFY3h7CI3zJpDC5fcgJCNs2ebb0gIFVbPv/ErfF6adulZkMV8gzURZVE=
-----END CERTIFICATE-----
    """

    k8_cluster = strongdm.AmazonEKS(
        name=f"K8 Cluster {num}",
        endpoint="https://A1ADBDD0AE833267869C6ED0476D6B41.gr7.us-east-2.eks.amazonaws.com",
        access_key="CLUSTERAKIAIOSFODNN7",
        secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYCLUSTERKEY",
        certificate_authority=certificate_authority,
        region="us-east-2",
        cluster_name=f"cluster_{num}",
        role_arn="arn:aws:iam::000000000000:role/RoleName",
        healthcheck_namespace="default",
    )

    return k8_cluster


def get_resource_ssh_server(hostname: str = "hyper.tank.com", port: int = None) -> strongdm.SSH:
    """
    Get a prepopulated ssh server resource
    :param hostname: str
    :param port: int
    :return: strongdm.SSH
    """
    if not port:
        port = random.randint(5000, 7000)

    ssh_server = strongdm.SSH(
        name=f"SSH Server for {hostname}:{port}",
        hostname=hostname,
        username=f"ssh_user_{port}",
        port=port,

    )

    return ssh_server


resources = [
    ("datasource", get_resource_postgres()),
    ("k8_cluster", get_resource_k8_cluster()),
    ("ssh_server", get_resource_ssh_server()),
]

nodes = [
    ("gateway", get_resource_gateway()),
    ("relay", get_resource_relay()),
]


def test_wait_for_healthy_datasource(client):
    """
    Adding a live datasource and waiting for a healthy state
    """
    postgres = strongdm.Postgres(
        name=f"Live Amazon Postgres Datasource",
        hostname=f"ec2-3-84-1-51.compute-1.amazonaws.com",
        port=5432,
        username="wordwasp",
        password="test123",
        database="wordwasp",
        tags={"datasource": "live"},
    )

    # Test Setup: Delete the datasource if found
    for datasource in client.resources.list(filter='tags:datasource=live'):
        client.resources.delete(datasource.id)

    # Creating a datasource
    resource_response = client.resources.create(resource=postgres)
    resource_id = resource_response.resource.id
    datasource_response = client.resources.get(resource_id)

    # Waiting for the data source to show as healthy and asserting it happened within a minute
    num = 30
    count = 0
    while not datasource_response.resource.healthy and count <= num:
        sleep(2)
        count = count + 1
        datasource_response = client.resources.get(resource_id)

    assert count <= num and datasource_response.resource.healthy, f"Live datasource not showing healthy after {num * 2} seconds."


@pytest.mark.parametrize("description, resource", resources)
def test_add_find_and_remove_resources(client, description, resource):
    """
    A parameterized test for adding, finding, and removing a datasource
    """
    resource_response = None
    delete_response = None
    try:
        # Creating the resource
        resource_response = client.resources.create(resource)
        assert hasattr(resource_response.resource, "healthy"), "Resource was not created correctly"

        # Finding the resource
        list_resource_response = list(client.resources.list("healthy:false"))
        resource_ids = [resource.id for resource in list_resource_response]
        assert resource_response.resource.id in resource_ids, "Could not find the resource when filtering"

        # Deleting and validating resource is gone
        delete_response = client.resources.delete(resource_response.resource.id)
        list_resource_response2 = list(client.resources.list("healthy:false"))
        resource_ids2 = [resource.id for resource in list_resource_response2]
        assert resource_response.resource.id not in resource_ids2, "Should not have found the resource when filtering"
    finally:
        if resource_response and not delete_response:
            client.resources.delete(resource_response.resource.id)


@pytest.mark.parametrize("description, node", nodes)
def test_add_find_and_remove_nodes(client, description, node):
    """
    A parameterized test for adding, finding, and removing nodes
    """
    node_response = None
    delete_response = None
    try:
        # Creating the node
        node_response = client.nodes.create(node)
        assert hasattr(node_response.node, "state"), "Node was not created correctly"

        # Finding the node
        list_node_response = list(client.nodes.list(f"id:{node_response.node.id}"))
        assert len(list_node_response) == 1, "Could not find the node when filtering"

        # Deleting and validating resource is gone
        delete_response = client.nodes.delete(node_response.node.id)
        get_response = client.nodes.get(node_response.node.id)
        assert get_response.node, "Should not have found the node when doing a get"
    finally:
        if node_response and not delete_response:
            client.nodes.delete(node_response.node.id)


def test_connect_to_resource_after_relay_destroyed(client):
    for datasource in client.resources.list(filter='name:wordwasp_debian'):
        client.resources.delete(datasource.id)

    ssh_server = get_resource_ssh_server(hostname="ec2-3-84-1-51.compute-1.amazonaws.com", port=2222)
    ssh_server.name = 'wordwasp_debian'
    ssh_server.key_type = 'ed25519'
    # ssh_server.public_key = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMpaI+ll54ywU+1s1WRBhrhEAsH4N9THUehgiPjEL3Eg'
    ssh_server.username = 'root'
    ssh_server.tags = {'wordwasp': ''}

    ssh_server_response = client.resources.create(ssh_server, timeout=30)

    # Unable to get this healthy or make the relay connect to it,,,
    # I can ssh to it.
    # Local box thinks it is connected but it is not really

    # <sdm.SSH allow_deprecated_key_exchanges: False  secret_store_id: '' bind_interface: '127.0.0.1' egress_filter: '' healthy: True hostname: 'ec2-3-84-1-51.compute-1.amazonaws.com' id: 'rs-633797a564a86011' key_type: 'ed25519' name: 'wordwasp_debian' port: 2222 port_forwarding: False port_override: 10002 public_key: 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMpaI+ll54ywU+1s1WRBhrhEAsH4N9THUehgiPjEL3Eg\n'
    #  subdomain: '2bf00517bd35ef8f' tags: {'wordwasp': ''} username: 'root' >
