###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header

from ccp_server.api.v1 import cloud_utils
from ccp_server.api.v1 import image
from ccp_server.api.v1 import onboarding
from ccp_server.api.v1 import org
from ccp_server.api.v1 import project
from ccp_server.api.v1 import self_onboarding
from ccp_server.api.v1 import user
from ccp_server.api.v1 import utils
from ccp_server.api.v1 import volume
from ccp_server.api.v1 import volume_snapshot
from ccp_server.api.v1.admin import aggregate
from ccp_server.api.v1.admin import flavor
from ccp_server.api.v1.admin import hypervisor
from ccp_server.api.v1.clusters import cluster
from ccp_server.api.v1.clusters import cluster_template
from ccp_server.api.v1.compute import instance
from ccp_server.api.v1.compute import keypair
from ccp_server.api.v1.networks import floating_ip
from ccp_server.api.v1.networks import network
from ccp_server.api.v1.networks import port
from ccp_server.api.v1.networks import router
from ccp_server.api.v1.networks import security_group
from ccp_server.api.v1.networks import security_group_rule
from ccp_server.api.v1.networks import subnet
from ccp_server.api.v1.storage import bucket


def ccp_headers(cloud_id: str = Header(), org_id: str = Header()):
    """Function to add cloud_id and org_id as a header"""
    pass


def cloud_ccp_headers(cloud_id: str = Header()):
    """Function to add only cloud_id as a header"""
    pass


def org_ccp_headers(org_id: str = Header()):
    """Function to add only org_id as a header"""
    pass


base_router = APIRouter()
api_router = APIRouter(dependencies=[Depends(ccp_headers)])
org_admin_api_router = APIRouter(dependencies=[Depends(cloud_ccp_headers)])
org_api_router = APIRouter(dependencies=[Depends(org_ccp_headers)])
public_router = APIRouter()

# API Routers for all the CCP APIs where cloud_id and org_id are required

api_router.include_router(keypair.router, tags=["Keypair"])
api_router.include_router(volume.router, tags=["Volume"])
api_router.include_router(instance.router, tags=["Instance"])
api_router.include_router(bucket.router, tags=["Bucket"])
api_router.include_router(volume_snapshot.router, tags=["Volume Snapshot"])
api_router.include_router(router.router, tags=["Router"])
api_router.include_router(security_group_rule.router,
                          tags=["Security Group"])
api_router.include_router(port.router, tags=["Port"])
api_router.include_router(floating_ip.router, tags=[
    "Floating IP"])  # TODO for all projects all Floating IP and for single network all Floating IP
api_router.include_router(security_group.router, tags=["Security Group"])
# TODO for all projects all Cluster template
api_router.include_router(cluster_template.router, tags=["Cluster"])
api_router.include_router(cluster.router, tags=["Cluster"])
api_router.include_router(subnet.router,
                          tags=["Subnet"])
api_router.include_router(network.router, tags=["Network"])

# this api_router should be in the end only because of similar routing issue.
api_router.include_router(project.router, tags=["Project"], prefix='/projects')

# Org API Router for all the CCP APIs where only org_id is required

org_api_router.include_router(user.router, tags=["User"], prefix="/users")

# Base router for all the CCP APIs where cloud_id and org_id are not required

base_router.include_router(onboarding.router, tags=[
    "Onboarding"], prefix="/admin/onboarding")
base_router.include_router(utils.router, tags=["Utils"], prefix="/utils")
base_router.include_router(
    org.router, tags=["Organization"], prefix="/admin/orgs")

# Org Admin API router for all the CCP APIs where only cloud_id is required

org_admin_api_router.include_router(
    aggregate.router, tags=["Aggregate"], prefix="/admin/aggregates")
org_admin_api_router.include_router(
    hypervisor.router, tags=["Hypervisor"], prefix="/admin/hypervisor")
org_admin_api_router.include_router(
    flavor.router, tags=["Flavor"], prefix="/admin/flavors")
org_admin_api_router.include_router(
    image.router, tags=["Image Service"], prefix="/admin/images")
org_admin_api_router.include_router(
    cloud_utils.router, tags=["Cloud Utils"], prefix="/clouds")

public_router.include_router(self_onboarding.router, tags=[
    "Onboarding"], prefix='/onboarding')
