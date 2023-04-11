###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Dict

from pydantic.types import StrictStr

from ccp_server.db.mongo import MongoAPI
from ccp_server.provider.aws.aws import AWS
from ccp_server.provider.cloud_provider import CloudProvider
from ccp_server.provider.gcp.gcp import GCP
from ccp_server.provider.openstack.openstack import Openstack
from ccp_server.util import ccp_context
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPNotFoundException
from ccp_server.util.utils import Utils


class Provider:
    # Store all the cloud provider data at the time of startup
    cloud_connections: Dict[StrictStr, CloudProvider] = {}
    mongo: MongoAPI = None

    def __init__(self):
        Provider.cloud_connections[Constants.CLOUD_TYPE_OPENSTACK] = Openstack(
        )
        Provider.cloud_connections[Constants.CLOUD_TYPE_AWS] = AWS()
        Provider.cloud_connections[Constants.CLOUD_TYPE_GCP] = GCP()

        # Initialize the mongo connection
        Provider.mongo = MongoAPI()

    @property
    def connect(self) -> CloudProvider:
        cloud: str = ccp_context.get_cloud()

        if cloud in Utils.load_supported_clouds():
            cloud_type: str = Utils.load_cloud_details(cloud).get("type")
            return Provider().cloud_connections[cloud_type]
        else:
            raise CCPNotFoundException(
                message=f"'{cloud}' is not a valid cloud or not supported.")

    @property
    def db(self) -> MongoAPI:
        return Provider.mongo
