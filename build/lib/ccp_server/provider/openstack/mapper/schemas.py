###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, March 2023     #
###############################################################################
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic.types import Any

from ccp_server.util import ccp_context
from ccp_server.util.enums import Status


class Schemas(BaseModel):
    class Mixins(BaseModel):
        created_at: Optional[datetime] = datetime.utcnow()
        created_by: str = ccp_context.get_logged_in_user()
        updated_at: Optional[datetime] = None
        updated_by: str = None

    class Base(Mixins):
        name: str
        description: str = None
        cloud: str = None
        org_id: Optional[str] = None
        project_id: Optional[str] = None
        reference_id: str = None
        source: Optional[str] = None
        source_id: Optional[str] = None
        active: Status = Status.ACTIVE

    class Image(Base):
        status: str
        visibility: str
        is_protected: bool
        is_hidden: bool
        disk_format: str
        size: int
        container_format: str
        tags: list = None
        cloud_meta: dict

    class Network(Base):
        status: str
        router: str = None
        availability_zones: Optional[list] = None
        admin_state: Optional[str]
        shared: Optional[bool]
        cloud_meta: dict

    class Instance(Base):
        image: str
        flavor: str
        security_groups: list = None
        vm_state: str
        task_state: str = None
        availability_zone: str
        admin_password: str = None
        volumes: list = None
        networks: list = None
        interface: str = None
        private_v4: str = None
        private_v6: str = None
        public_v4: str = None
        public_v6: str = None
        key_name: str = None
        user_data: str = None
        host: str
        launched_at: str = None
        terminated_at: str = None
        root_device: str = None
        power_state: str
        status: str
        tags: list = None
        metadata: dict = None
        cloud_meta: dict

    class Floatingip(Base):
        cloud_meta: dict

    class Port(Base):
        network_id: str
        mac_address: Optional[str]
        admin_state: bool = True
        attached_device: Optional[str]
        cloud_meta: dict

    class Bucket(Base):
        pass

    class Router(Base):
        admin_state_up: Optional[bool] = True
        network_id: Optional[str] = None
        enable_snat: bool = None
        ext_fixed_ips: Optional[list]
        project_id: Optional[str] = None
        availability_zone_hints: Optional[list] = None
        availability_zones: Optional[list] = None
        cloud_meta: dict

    class Securitygroup(Base):
        cloud_meta: dict

    class Securitygrouprule(Base):
        name: Optional[str] = None
        description: Optional[str] = None
        security_group_id: str
        ip_protocol: Optional[str] = None
        ether_type: Optional[str] = None
        port_range_min: Optional[str] = None
        port_range_max: Optional[str] = None
        cloud_meta: dict

    class Subnet(Base):
        network_id: str
        cidr: str
        ip_version: int
        enable_dhcp: Optional[bool] = True
        gateway_ip: Optional[str] = None
        disable_gateway_ip: Optional[bool] = False
        allocation_pools: Optional[List[str]] = None
        dns_nameservers: Optional[List[str]] = None
        cloud_meta: dict

    class Project(Base):
        domain_name: Optional[str] = None
        enable: Optional[bool] = True
        cloud_meta: dict

    class Keypair(Base):
        public_key: Optional[str] = None
        private_key: Optional[str] = None
        domain_name: Optional[List[str]] = None
        cloud_meta: dict

    class Flavor(Base):
        ram: int
        vcpus: int
        disk: int
        ephemeral: int
        swap: Any = None
        disabled: bool
        vcpus: Optional[int] = None
        zone: Optional[str] = None
        rxtx_factor: float
        is_public: bool
        disabled: bool
        cloud_meta: dict

    class Volumesnapshot(Base):
        volume_id: str
        cloud_meta: dict

    class Volume(Base):
        size: Optional[int] = None
        bootable: Optional[bool] = None
        status: Optional[str] = None
        host: Optional[str] = None
        cloud_meta: dict
        attachments: Optional[List[Dict[str, Any]]] = None
        availability_zone: Optional[str] = None
        volume_type: Optional[str] = None
        is_bootable: Optional[bool] = None
        is_encrypted: Optional[bool] = None
        is_multiattach: Optional[bool] = None

    class Clustertemplate(Base):
        name: str
        image_id: str
        keypair_id: str
        coe: str
        cloud_meta: dict
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
        labels: Optional[str] = None

    class Cluster(Base):
        name: str
        cluster_template_id: str
        availability_zone: Optional[str] = None
        master_count: int = 1
        master_flavor_id: Optional[str]
        node_count: int = 1
        flavor_id: Optional[str]
        cloud_meta: dict
