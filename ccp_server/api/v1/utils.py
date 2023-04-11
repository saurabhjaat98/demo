###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Dict
from typing import List

from fastapi import APIRouter
from fastapi import Path
from pydantic.types import StrictStr
from starlette import status

from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPPincodeNotFoundException
from ccp_server.util.messages import Message
from ccp_server.util.utils import Utils

router = APIRouter()


@router.get("/supported-clouds",
            description="Fetch the supported clouds.",
            status_code=status.HTTP_200_OK,
            response_description="Supported clouds Response.",
            )
async def get_supported_cloud() -> List[Dict[StrictStr, StrictStr]]:
    supported_clouds_details: List[Dict[StrictStr, StrictStr]] = []
    supported_clouds = Utils.load_supported_cloud_details()
    for key, value in supported_clouds.items():
        supported_clouds_details.append({
            "cloud_id": key,
            "cloud_name": value['cloud_name']
        })
    return supported_clouds_details


@router.get('/pincode/{pincode}',
            description="Fetch the pincode.",
            status_code=status.HTTP_200_OK,
            response_description="Pincode Response.",
            )
async def get_details_by_pincode(pincode: str = Path(title="Pincode",
                                                     description="Fetch the details based on Pincode",
                                                     regex=Constants.PINCODE_REGEX)):
    try:
        pincode_data = Utils.load_pincode_json()[pincode]
        return {'country': pincode_data['country'], 'district': pincode_data['city'],
                'state': pincode_data['state']}
    except KeyError:
        raise CCPPincodeNotFoundException(
            message=Message.PINCODE_NOT_FOUND_ERR_MSG.format(pincode))
