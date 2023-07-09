"""
--- RESOURCES ---
Add Resource - DB
Add Resource - Linux Server - SSH Server
Add Resource - K8
Add Resource - Gateway
Add Resource - Relay
List Resources - Filter - "healthy:true", "healthy:false",
List Resources - Filter - DB Specific
List Resources - Filter - Linux Server Specific
List Nodes - Filter - Gatewqy, Relay
Remove Resource - DB
Remove Resource - Linux Server - SSH Server
Remove Resource - K8
Remove Resource - Gateway
Remove Resource - Relay
"""
from time import sleep

import pytest
import strongdm
from strongdm import BadRequestError, InternalError, AlreadyExistsError, NotFoundError


# def test_delete_resources(client):
#     resources = list(client.resources.list('healthy:false'))
#     for resource in resources:
#         client.resources.delete(resource.id)


def test_add_live_datasource(client):
    resource_response = None
    postgres = strongdm.Postgres(
        name=f"Live Amazon Postgres Datasource",
        hostname=f"ec2-3-84-1-51.compute-1.amazonaws.com",
        port=5432,
        username="wordwasp",
        password="test123",
        database="wordwasp",
        tags={"datasource":"live"},
    )

    # Pre Setup
    for datasource in client.resources.list(filter='tags:datasource=live'):
        client.resources.delete(datasource.id)

    try:
        resource_response = client.resources.create(resource=postgres)
        resource_id = resource_response.resource.id
        datasource_response = client.resources.get(resource_id)

        num = 30
        count = 0
        while not datasource_response.resource.healthy and count <= num:
            sleep(2)
            count = count + 1
            datasource_response = client.resources.get(resource_id)

        assert count <= num and datasource_response.resource.healthy, f"Live datasource not showing healthy after {num * 2} seconds."
    finally:
        client.resources.delete(resource_response.resource.id)
