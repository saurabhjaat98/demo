###############################################################################
# Copyright (c) 2022-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from ccp_server.kc.client import KeycloakClientService
from ccp_server.util.constants import Constants
from ccp_server.util.enums import InstanceRebootType
from ccp_server.util.exceptions import CCPBusinessException
from ccp_server.util.exceptions import CCPNotFoundException
from ccp_server.util.exceptions import CCPPincodeNotFoundException
from ccp_server.util.messages import Message
from ccp_server.util.utils import Utils


class Base(BaseModel):
    """Only for those object whose need tag support"""
    tags: Optional[Dict[str, str]] = Field(None, example={"type": "dev"},
                                           description="Tags for the object")

    @validator("tags")
    def tag_validator(cls, v: Dict[str, str]) -> Dict[str, str]:
        if len(v) > Constants.MAX_TAG_LENGTH:
            raise CCPBusinessException(
                Message.TAG_MAX_LENGTH_EXCEEDED.format(Constants.MAX_TAG_LENGTH))
        return v


class Project(Base):
    name: str = Field(..., description="Name of Project",
                      regex=Constants.NAME_REGEX, example='demo123')
    description: str = Field(None, example='demo is about..',
                             description="Detail description about project like:- In this project we're ...")


class User(BaseModel):
    email: str = Field(..., description="Email Name of the user",
                       regex=Constants.EMAIL_REGEX, example="test1234@test.com")
    first_name: str = Field(..., description="First Name of the user",
                            regex=Constants.FIRST_NAME_REGEX, example='xyzf')
    last_name: str = Field(..., description="Last Name of the user",
                           regex=Constants.LAST_NAME_REGEX, example='abc')
    mobile_number: Optional[str] = Field(
        description="Mobile Number of the user", regex=Constants.MOBILE_NUMBER_REGEX, example='9999999999')
    roles: List[str] = Field(..., description="List of roles of the user",
                             example=['org-admin'])
    project_id: str = Field(default=None, description="Project Id of the user", regex=Constants.UUID4_REGEX,
                            example='1f7ffd3d-ca8c-422c-9748-b5684f186351')

    @validator('roles')
    def role_validate(cls, value):
        for role in value:
            if role not in KeycloakClientService().get_client_roles_name():
                raise CCPNotFoundException(message=f"Role {role} not found")
        return value

    @validator('email')
    def email_validate(cls, value):
        return Utils.is_email_supported(value)


class Organization(BaseModel):
    name: str = Field(..., description="Name of the organization",
                      regex=Constants.NAME_REGEX, example='org_name1111')
    description: str = Field(..., description="Description of the organization",
                             regex=Constants.DESCRIPTION_REGEX, example='org_description')


class Address(BaseModel):
    address_line1: str = Field(..., description="Address of the user",
                               regex=Constants.ADDRESS_REGEX, example='pqr_nr')
    address_line2: Optional[str] = Field(description="Address of the user",
                                         regex=Constants.ADDRESS_REGEX, example='pqabcf')
    city: str = Field(..., description="city name ",
                      regex=Constants.CITY_REGEX, example='qwe')
    state: str = Field(..., description="state name ",
                       regex=Constants.CITY_REGEX, example='der')
    country: str = Field(..., description="city name ",
                         regex=Constants.CITY_REGEX, example='fgh')
    postal_code: str = Field(..., description="postal_code ",
                             regex=Constants.POSTAL_CODE_REGEX, example='123432')
    landmark: Optional[str] = Field(
        regex=Constants.ADDRESS_REGEX, example='sector-1')
    mobile_number: Optional[str] = Field(default='9999999999', regex=Constants.MOBILE_NUMBER_REGEX,
                                         description="Mobile Number of the user", example='')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.city = kwargs.get('city').title()
        self.state = kwargs.get('state').title()
        self.country = kwargs.get('country').title()
        self.postal_code = kwargs.get('postal_code')

        if self.postal_code:
            pincode_info = Utils.get_details_by_pincode(self.postal_code)
            if pincode_info['city'] != self.city or pincode_info['state'] != self.state or \
                    pincode_info['country'] != self.country:
                raise CCPPincodeNotFoundException(
                    message=Message.PINCODE_NOT_MATCH.format(self.postal_code))


class Onboarding(BaseModel):
    name: str = Field(..., description="Organization of the user",
                      regex=Constants.NAME_REGEX, example='org_name1234')
    description: Optional[str] = Field(None, description="Organization of the user", regex=Constants.DESCRIPTION_REGEX,
                                       example='description')
    default_cloud: Optional[str] = Field(default=None, example='noida-1',
                                         description="Default cloud for the organization where user will be landed")
    communication_address: Address
    billing_address: Address
    tan_number: str = Field(..., description='TAN number',
                            regex=Constants.TAN_NUMBER_REGEX, example='PDES03028F')
    gst_number: str = Field(..., description="GST Number of the organization", regex=Constants.GST_REGEX,
                            example='43YTREY9876A1Z0')
    users: List[User]


class Profile(BaseModel):
    description: Optional[str] = Field(None, description="Organization of the user", regex=Constants.DESCRIPTION_REGEX,
                                       example='description')
    default_cloud: Optional[str] = Field(default=None, example='noida-1',
                                         description="Default cloud for the organization where user will be landed")
    communication_address: Address
    billing_address: Address
    tan_number: str = Field(..., description='TAN number',
                            regex=Constants.TAN_NUMBER_REGEX, example='PDES03028F')
    gst_number: str = Field(..., description="GST Number of the organization", regex=Constants.GST_REGEX,
                            example='43YTREY9876A1Z0')


class Group(BaseModel):
    name: str = Field(..., description="Name of Group",
                      regex=Constants.NAME_REGEX, example='Group_name')
    description: str = Field(None, example='group_decription', description="Detail about GROUP ...",
                             regex=Constants.DESCRIPTION_REGEX)
    communication_address: Address = None
    billing_address: Address = None
    tan_number: str = None
    gst_number: str = None


class SelfOnboarding(BaseModel):
    first_name: str = Field(..., description="First Name of the user",
                            regex=Constants.FIRST_NAME_REGEX, example='xyzf')
    last_name: str = Field(..., description="Last Name of the user",
                           regex=Constants.LAST_NAME_REGEX, example='abc')
    organization_name: str = Field(..., description="Organization of the user",
                                   regex=Constants.NAME_REGEX, example='org_name1234')
    email: str = Field(..., description="Email id of the user",
                       regex=Constants.EMAIL_REGEX, example='user@email.com')

    @validator('email')
    def email_validate(cls, value):
        return Utils.is_email_supported(value)


class Flavor(BaseModel):
    name: str
    description: str
    cloud: str
    vcpus: int
    ram: int
    disk: int
    ephemeral: Optional[int] = 0
    swap: Optional[int] = 0
    rxtx_factor: Optional[int] = 1


class KeyPair(BaseModel):
    name: str = Field(..., description="Name of Key-pair",
                      regex=Constants.NAME_REGEX, example='abcd')
    public_key: Optional[str] = Field(
        description="Name of Key-pair", regex=Constants.PUBLIC_KEY_REGEX,
        example='ssh-rsa AAAAB3NzaC1ycABAAABAQC1SaD+LbNm....')


class Network(Base):
    name: str = Field(..., description="Name of Network",
                      regex=Constants.NAME_REGEX, example='public_123')
    admin_state_up: bool = Field(...,
                                 description="eg:- True or false ", example=True)
    shared: bool = Field(..., description="eg:- True or false ", example=True)
    external: Optional[bool] = Field(...,
                                     description="eg:- True or false ", example=True)
    availability_zone_hints: Optional[list] = Field(
        None, description="A list of availability zone hints")


class Subnet(BaseModel):
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
    name: Optional[str] = None
    size: int = 1


class Instance(Base):
    name: str = Field(..., description="Name of Instance",
                      regex=Constants.USERNAME_REGEX, example='demo')

    description: Optional[str] = Field(example='Instance_description',
                                       description="Detail description about instance like:- working of instance ..",
                                       regex=Constants.DESCRIPTION_REGEX)
    image: Optional[str]
    flavor: str = Field(..., description="Flavour name or ID")
    network: str = Field(..., description="Network ID or name")
    instance_username: Optional[str] = Field(description="Name of user",
                                             regex=Constants.USERNAME_REGEX, example='instance')
    instance_password: Optional[str] = Field(description="password", regex=Constants.PASSWORD_REGEX,
                                             example='public@123')
    boot_volume: Optional[str]
    availability_zone: Optional[str] = Field(None, description="Enter Avaibilabity name",
                                             regex=Constants.NAME_REGEX, example='nova')
    security_groups: Optional[List[str]]
    key_name: Optional[str]
    min_count: Optional[int] = 1
    security_groups: Optional[str] = None
    scheduler_hints: Optional[Dict[str, str]]
    userdata: Optional[str] = None
    meta: Optional[Dict[str, str]]


class InstanceActions:
    class StopAction(BaseModel):
        stop: Optional[str] = Field(
            None, description="Stop Action to perform", alias="os-stop", example='')

    class StartAction(BaseModel):
        start: Optional[None] = Field(
            None, description="Start Action to perform", alias="os-start", example='')

    class RebootAction(BaseModel):
        reboot: InstanceRebootType

    class RebuildAction(BaseModel):
        image: str
        accessIPv4: Optional[str]
        accessIPv6: Optional[str]
        adminPass: Optional[str]
        metadata: Optional[dict]
        preserve_ephemeral: Optional[bool]
        key_name: Optional[str]
        user_data: Optional[str]
        trusted_image_certificates: Optional[str]
        hostname: Optional[str]

    class ResizeAction(BaseModel):
        flavorRef: str = Field(
            ..., description="Flavor ID of the Resizing Server", example='flavor ID')

    class SuspendAction(BaseModel):
        suspend: Optional[None] = Field(
            None, description="Suspend Action to perform", example='')

    class ResumeAction(BaseModel):
        resume: Optional[None] = Field(
            None, description="Resume the suspended Instance", example='')

    class PauseAction(BaseModel):
        pause: Optional[None] = Field(
            None, description="Pause the Running Instance", example='')

    class UnpauseAction(BaseModel):
        unpause: Optional[None] = Field(
            None, description="Pause the unpaused Instance", alias="os-start", example='')


class InstanceActionsSchema(BaseModel):
    REBOOT: InstanceActions.RebootAction = None
    REBUILD: InstanceActions.RebuildAction = None
    RESIZE: InstanceActions.ResizeAction = None


class SecurityGroup(BaseModel):
    name: str = Field(..., description="Enter name of Security Group",
                      regex=Constants.NAME_REGEX, example='abc')
    description: str = Field(..., example='Securitygroup_description',
                             description="In this abcd security group we're..", regex=Constants.DESCRIPTION_REGEX)


class FloatingIP(BaseModel):
    network_id: str
    pass


class PortBinding(BaseModel):
    vnic_type: Optional[str] = "normal"
    host_id: Optional[str] = Field(None, description="ID of the host where the port resides",
                                   regex=Constants.UUID4_REGEX)


class PortFixedIP(BaseModel):
    subnet_id: Optional[str] = Field(
        None, description="Subnet ID to allocate IP", regex=Constants.NAME_REGEX)
    ip_address: Optional[str] = Field(None, description="IP address to allocate to the port",
                                      regex=Constants.NAME_REGEX)


class Port(BaseModel):
    name: Optional[str] = Field(
        None, description="Enter name of Port", regex=Constants.NAME_REGEX, example='abc')
    admin_state_up: Optional[bool] = True
    device_id: Optional[str] = Field(
        ..., description="Device ID uses the port", regex=Constants.UUID4_REGEX)
    device_owner: Optional[str] = Field(
        None, description="ID of the entity that uses the port")
    mac_address: Optional[str] = Field(
        None, description="The MAC address", regex=Constants.NAME_REGEX)
    port_security_enabled: Optional[bool]
    fixed_ips: Optional[List[PortFixedIP]] = list()
    binding: Optional[PortBinding]


class Bucket(Base):
    name: str
    description: Optional[str]


class SecurityGroupRule(BaseModel):
    name: str = Field(..., description="Name of Security Group Rule")
    port_range_min: Optional[int] = Field(
        None, description="Minimum range of port", example=1)
    port_range_max: Optional[int] = Field(
        None, description="Maximum range of port", example=65530)
    ethertype: Optional[str] = Field(
        'IPv4', description="Ethertype of rule", example='IPv4')
    protocol: Optional[str] = Field(
        None, description="Type of protocol", example='tcp')
    direction: Optional[str] = Field(
        'ingress', description="Direction of the rule", example='ingress')
    remote_ip_prefix: Optional[str] = Field(
        None, description="Remote IP prefix", example='0.0.0.0/0')
    remote_group_id: Optional[str] = Field(
        None, description="Remote group ID", regex=Constants.UUID4_REGEX)
    description: Optional[str] = Field(None, description="Description about the rule",
                                       regex=Constants.DESCRIPTION_REGEX, example='This rule is used to..')


class Router(BaseModel):
    name: str = Field(..., description="Name of Router",
                      regex=Constants.NAME_REGEX, example='demo')
    admin_state_up: Optional[bool] = True
    ext_gateway_net_id: Optional[str] = Field(
        None, description="Ext gateway network ID", regex=Constants.UUID4_REGEX)
    enable_snat: Optional[bool] = Field(
        None, description="Enable Source NAT attribute")
    ext_fixed_ips: Optional[List[PortFixedIP]] = list()
    availability_zone_hints: Optional[list] = Field(
        None, description="A list of availability zone hints")


class VolumeSnapshot(BaseModel):
    name: str = Field(..., description="Name of Router",
                      regex=Constants.NAME_REGEX, example='demo')
    description: Optional[str] = Field(None, description="Description about the volume_snapshot",
                                       regex=Constants.DESCRIPTION_REGEX, example='This rule is used to..')


class ClusterTemplate(Base):
    name: str = Field(..., description="Name of Cluster Template",
                      regex=Constants.NAME_REGEX, example='template_001')
    keypair_id: str = Field(..., description="Keypair name or ID")
    coe: str = Field(..., description="Name of the COE",
                     regex=Constants.NAME_REGEX, example='mesos')
    public: Optional[bool] = False
    hidden: Optional[bool] = False
    registry_enabled: Optional[bool] = False
    tls_disabled: Optional[bool] = False
    volume_driver: str = Field(...,
                               description="Name of volume driver", example="rexray")
    docker_storage_driver: str = Field(
        ..., description="Name of device storage driver", example="devicemapper")
    network_driver: str = Field(...,
                                description="Name of network driver", example="docker")
    http_proxy: str = Field(None, description="IP address of HTTP proxy")
    https_proxy: str = Field(None, description="IP address of HTTPS proxy")
    no_proxy: str = Field(None, description="IP address of proxy server")
    external_network_id: str = Field(..., description="External Network name or ID",
                                     regex=Constants.UUID4_REGEX)
    fixed_network: Optional[str] = Field(..., description="Fixed Network name or ID",
                                         regex=Constants.UUID4_REGEX)
    fixed_subnet: Optional[str] = Field(..., description="Fixed Subnet name or ID",
                                        regex=Constants.UUID4_REGEX)
    dns_nameserver: Optional[str] = Field(
        None, description="Name of DNS name server")
    master_lb_enabled: Optional[bool] = False
    floating_ip_enabled: Optional[bool] = False
    labels: Optional[str] = Field(None, description="label details")


class Cluster(Base):
    name: str = Field(..., description="Name of Cluster",
                      regex=Constants.NAME_REGEX, example='cluster_001')
    availability_zone: Optional[str] = Field(None, description="Availability zone name",
                                             regex=Constants.NAME_REGEX, example='nova')
    master_count: int = Field(
        1, description="The number of servers that will serve as master for the cluster")
    node_count: int = Field(
        1, description="The number of servers that will serve as node in the cluster")
