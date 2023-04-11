###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
from fastapi import APIRouter
from fastapi import status

from ccp_server.service.cloud_utils import CloudUtilService

router = APIRouter()

cloud_util_service: CloudUtilService = CloudUtilService()


@router.get("/azs",
            description="List all availability zones",
            status_code=status.HTTP_200_OK,
            response_description="List Availability Zones Response",
            )
async def availability_zones():
    """
    List all availability zones names of a cloud.
    :return: List of availability zones names.
    """
    return await cloud_util_service.list_availability_zones()
