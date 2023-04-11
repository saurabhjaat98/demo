###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel


class Base(BaseModel):
    name: str
    description: Optional[str] = None


class Project(Base):
    domain_id: Optional[str] = 'default'


class User(Base):
    email: str
    default_project: Optional[str] = None
    domain_id: Optional[str] = 'default'
    role: Optional[str] = 'member'


class Flavor(Base):
    vcpus: int
    ram: int
    disk: int
    ephemeral: Optional[int] = 0
    swap: Optional[int] = 0
    rxtx_factor: Optional[int] = 1


class Network(BaseModel):
    name: str
    admin_state_up: Optional[bool]
    shared: Optional[bool]
    external: Optional[bool]
    availability_zone_hints: Optional[list] = list()


class Subnet(Base):
    name: str
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


class Instance(BaseModel):
    name: str
    flavor: Optional[Flavor]
    image: Optional[str]
    networks: Optional[List[Network]]
    user: Optional[User]
    project: Optional[Project]
    availability_zone: Optional[str]
    security_groups: Optional[List[str]]


class SecurityGroup(Base):
    name: str
    description: str


class Port(Base):
    name: Optional[str] = None
    admin_state_up: Optional[bool]
    device_id: Optional[str] = None
    device_owner: Optional[str] = None
    mac_address: Optional[str] = None
    port_security_enabled: Optional[bool]
    fixed_ips: Optional[list] = list()
    binding: Optional[dict] = dict()


class Bucket(Base):
    name: str


class SecurityGroupRule(BaseModel):
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


class Router(BaseModel):
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


class Keypair(BaseModel):
    name: str
    public_key: Optional[str] = None
    private_key: Optional[str] = None


class StorageUser(User):
    name: str
    email: str


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
    dns_nameserver: Optional[str] = None
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
