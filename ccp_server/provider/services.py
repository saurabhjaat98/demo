###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from abc import ABC
from abc import abstractmethod

from ccp_server.provider import models


class Connection(ABC):

    @abstractmethod
    def connect(self):
        pass

    def botoclient(self):
        pass

    def rgw(self):
        pass


class Project(ABC):

    @abstractmethod
    def create_project(self, project: models.Project) -> models.Project:
        pass

    @abstractmethod
    def update_project(self, resource_id: str, project: models.Project) -> models.Project:
        pass

    @abstractmethod
    def delete_project(self, resource_id: str):
        pass

    @abstractmethod
    def add_member(self, resource_id, username):
        pass

    @abstractmethod
    def remove_member(self, resource_id, username):
        pass

    @abstractmethod
    def list_projects(self):
        pass


class User(ABC):

    @abstractmethod
    def create_user(self, user: models.User) -> models.User:
        pass

    @abstractmethod
    def update_user(self, resource_id: str, user: models.User) -> models.User:
        pass

    @abstractmethod
    def delete_user(self, resource_id: str):
        pass

    @abstractmethod
    def grant_role(self, resource_id: str, role_id: str) -> None:
        pass

    @abstractmethod
    def revoke_role(self, resource_id: str, role_id: str) -> None:
        pass


class Compute(ABC):
    pass


class Flavor(ABC):

    @abstractmethod
    def create_flavor(self, flavor: models.Flavor) -> models.Flavor:
        pass

    def list_flavors(self):
        pass


class CloudUtils(ABC):

    @abstractmethod
    def list_availability_zones(self):
        pass


class Aggregate(ABC):

    @abstractmethod
    def list_aggregates(self, ):
        pass

    def get_aggregates(self, aggregate_id: str) -> None:
        pass


class Network(ABC):

    @abstractmethod
    async def create_network(self, network: models.Network) -> models.Network:
        pass

    def list_all_networks(self):
        pass

    @abstractmethod
    def delete_network(self, network_id: str):
        pass


class Subnet(ABC):

    @abstractmethod
    def create_subnet(self, network_id: str, subnet: models.Subnet) -> models.Subnet:
        pass

    def list_subnets_by_network_id(self, network_id: str):
        pass

    @abstractmethod
    def delete_subnet(self, subnet_id: str):
        pass


class Image(ABC):

    @abstractmethod
    def list_images(self):
        pass

    def get_image(self, id: str):
        pass


class Hypervisor(ABC):

    @abstractmethod
    def list_hypervisors(self):
        pass


class Volume(ABC):
    @abstractmethod
    def create_volume(self, volume: models.Volume) -> models.Volume:
        pass

    @abstractmethod
    def get_volume(self, volume_id: str) -> models.Volume:
        pass

    @abstractmethod
    def delete_volume(self, volume_id: str):
        pass

    @abstractmethod
    def list_all_volumes(self):
        pass

    @abstractmethod
    def attach_volume(self, instance, volume):
        pass

    @abstractmethod
    def detach_volume(self, instance, volume):
        pass


class SecurityGroup(ABC):

    @abstractmethod
    def create_security_group(self, security_group: models.SecurityGroup) -> models.SecurityGroup:
        pass

    @abstractmethod
    def list_all_security_groups(self):
        pass

    @abstractmethod
    def delete_security_group(self, security_group_id: str):
        pass


class FloatingIP(ABC):

    @abstractmethod
    def create_floating_ip(self, network_id: str):
        pass

    @abstractmethod
    def list_all_floating_ips(self):
        pass

    @abstractmethod
    def delete_floating_ip(self, floating_ip_id: str):
        pass


class Port(ABC):

    @abstractmethod
    def create_port(self, network_id: str, port: models.Port) -> models.Port:
        pass

    @abstractmethod
    def list_ports_by_network_id(self):
        pass

    @abstractmethod
    def delete_port(self, port_id: str):
        pass


class Bucket(ABC):

    @abstractmethod
    def create_bucket(self, bucket: models.Bucket) -> models.Bucket:
        pass

    @abstractmethod
    def list_buckets(self):
        pass

    @abstractmethod
    def get_bucket(self, bucket_id: str):
        pass

    @abstractmethod
    def delete_bucket(self, bucket_id: str):
        pass

    @abstractmethod
    def upload_object(self, bucket_id: str, file_path: str):
        pass

    @abstractmethod
    def get_bucket_objects(self, bucket_id):
        pass

    @abstractmethod
    def delete_object(self, bucket_id: str, object_name: str):
        pass

    @abstractmethod
    def download_object(self, bucket_id: str, object_name: str, path: str):
        pass


class SecurityGroupRule(ABC):

    @abstractmethod
    def create_security_group_rule(self, security_group_rule: models.SecurityGroupRule) -> models.SecurityGroupRule:
        pass

    @abstractmethod
    def list_security_group_rules(self):
        pass

    @abstractmethod
    def delete_security_group_rule(self, security_group_rule_id: str):
        pass


class Router(ABC):

    @abstractmethod
    def create_router(self, network_id: str, router: models.Router) -> models.Router:
        pass

    @abstractmethod
    def list_all_routers(self):
        pass

    @abstractmethod
    def delete_router(self, router_id: str):
        pass


class VolumeSnapshot(ABC):
    @abstractmethod
    async def create_volume_snapshot(self, volume_id: str, snapshot: models.VolumeSnapshot) -> models.VolumeSnapshot:
        pass

    @abstractmethod
    async def list_volume_snapshots(self):
        pass

    @abstractmethod
    async def delete_volume_snapshot(self, snapshot_id: str):
        pass


class Keypair(ABC):

    @abstractmethod
    def create_keypair(self, keypair: models.Keypair) -> models.Keypair:
        pass

    @abstractmethod
    def delete_keypair(self, keypair_id: str):
        pass

    @abstractmethod
    def list_keypairs(self):
        pass

    @abstractmethod
    def get_keypair(self, keypair_id: str):
        pass


class StorageUser(ABC):

    @abstractmethod
    def create_storage_user(self, storageuser: models.StorageUser) -> models.StorageUser:
        pass


class ClusterTemplate(ABC):

    @abstractmethod
    def create_cluster_template(self, project_id: str, cluster_template: models.ClusterTemplate):
        pass

    @abstractmethod
    def list_all_cluster_templates(self):
        pass

    @abstractmethod
    def delete_cluster_template(self, cluster_template_id: str):
        pass


class Cluster(ABC):

    @abstractmethod
    def create_cluster(self, project_id: str, cluster: models.Cluster):
        pass

    @abstractmethod
    def list_all_clusters(self):
        pass

    @abstractmethod
    def delete_cluster(self, cluster_id: str):
        pass
