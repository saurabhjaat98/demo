###############################################################################
# Copyright (c) 2022-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Shubham Kumar <shubhamkumar@coredge.io>, Feb 2023                #
###############################################################################
from __future__ import annotations

from fastapi import APIRouter
from fastapi import status

from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import IDResponse
from ccp_server.service.onboarding import OnboardingService

router = APIRouter()

onboarding_service: OnboardingService = OnboardingService()


@router.post("",
             description="Onboarding organization.",
             status_code=status.HTTP_201_CREATED,
             response_description="Organisation Creation Response.",
             response_model=None
             )
async def onboarding(
        request: schemas.Onboarding
) -> IDResponse:
    """Onboarding organization.

    Args:
        request (schemas.Onboarding): Organization meta.

    """

    doc_id = await onboarding_service.onboarding(request)
    return IDResponse(doc_id=doc_id)
