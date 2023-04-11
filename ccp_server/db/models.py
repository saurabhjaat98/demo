###############################################################################
# Copyright (c) 2022-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Shubham Kumar <shubhamkumar@coredge.io>, Feb 2023                #
###############################################################################
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import StrictStr

from ccp_server.util.enums import Status


class Base(BaseModel):
    name: Optional[str]
    description: Optional[str]
    cloud: Optional[str]
    org_id: Optional[str]
    project_id: Optional[str]
    reference_id: Optional[str]
    external_id: Optional[str]
    created_by: str = 'CCP'
    created_at: datetime = datetime.utcnow()
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    cloud_meta: Optional[Dict[StrictStr, Any]]
    active: Status = Status.ACTIVE
    tags: Optional[Dict[str, str]] = None


class Address(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    country: str
    postal_code: str
    landmark: Optional[str] = None


class Flavor(Base):
    vcpus: int
    ram: int
    disk: int
    ephemeral: Optional[int] = 0
    swap: Optional[int] = 0
    rxtx_factor: Optional[int] = 1


class Organization(Base):
    default_cloud: str = None
    org_admin: List[str] = None
    tan_number: str = None
    gst_number: str = None
    communication_address: Dict[str, Any] = None
    billing_address: Dict[str, Any] = None


class Project(Base):
    default: bool = False


class KeyPair(Base):
    pass


class Network(Base):
    name: str
    admin_state_up: Optional[bool]
    shared: Optional[bool]
    external: Optional[bool]
    availability_zone_hints: Optional[list] = list()


class Subnet(Base):
    name: str
    network_id: str
    cidr: str
    ip_version: int
    enable_dhcp: Optional[bool]
    gateway_ip: Optional[str] = None
    disable_gateway_ip: Optional[bool]
    allocation_pools: Optional[List[str]] = None
    dns_nameservers: Optional[List[str]] = None
    host_routes: Optional[List[str]] = None


class Volume(Base):
    size: int


class Instance(Base):
    pass


class SecurityGroup(Base):
    name: str
    description: str


class FloatingIP(Base):
    network_id: str


class Port(Base):
    network_id: str
    name: Optional[str] = None
    admin_state_up: Optional[bool]
    device_id: Optional[str] = None
    device_owner: Optional[str] = None
    mac_address: Optional[str] = None
    port_security_enabled: Optional[bool]
    fixed_ips: Optional[list] = list()
    binding: Optional[dict] = dict()


class SecurityGroupRule(Base):
    security_group: str
    port_range_min: Optional[int]
    port_range_max: Optional[int]
    ethertype: Optional[str] = 'IPv4'
    protocol: Optional[str]
    direction: Optional[str] = 'ingress'
    remote_ip_prefix: Optional[str] = None
    remote_group_id: Optional[str] = None
    project_id: Optional[str] = None
    description: Optional[str] = None


class Router(Base):
    name: str
    admin_state_up: Optional[bool] = True
    ext_gateway_net_id: Optional[str] = None
    enable_snat: Optional[bool] = None
    ext_fixed_ips: Optional[List[Dict]] = list()
    project_id: Optional[str] = None
    availability_zone_hints: Optional[list] = list()


class VolumeSnapshot(Base):
    volume_id: str
    name: Optional[str] = None
    description: Optional[str] = None


class Bucket(Base):
    name: str


class ClusterTemplate(Base):
    name: str
    image_id: str
    keypair_id: str
    coe: str
    public: Optional[bool] = False
    hidden: Optional[bool] = False
    registry_enabled: Optional[bool] = False
    tls_disabled: Optional[bool] = False
    flavor_id: Optional[str]
    master_flavor_id: Optional[str]
    volume_driver: str
    docker_storage_driver: str
    docker_volume_size: str
    network_driver: str
    http_proxy: str = None
    https_proxy: str = None
    no_proxy: str = None
    external_network_id: str
    fixed_network: Optional[str]
    fixed_subnet: Optional[str]
    dns_nameserver: Optional[str]
    master_lb_enabled: bool = False
    floating_ip_enabled: bool = False
    labels: Optional[str]


class Cluster(Base):
    name: str
    cluster_template_id: str
    availability_zone: Optional[str] = None
    master_count: int = 1
    master_flavor_id: Optional[str]
    node_count: int = 1
    flavor_id: Optional[str]
