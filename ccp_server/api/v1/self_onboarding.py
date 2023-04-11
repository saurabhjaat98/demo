###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, March 2023                    #
###############################################################################
from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from ccp_server.config import auth
from ccp_server.schema.v1 import schemas
from ccp_server.schema.v1.response_schemas import IDResponse
from ccp_server.service.oidc import UserProfile
from ccp_server.service.self_onboarding import SelfOnboardingService

router = APIRouter()

onboarding_service: SelfOnboardingService = SelfOnboardingService()


@router.post("",
             description="Self Onboarding Signup.",
             status_code=status.HTTP_201_CREATED,
             response_description="Signup Response.",
             response_model=None
             )
async def self_onboarding(
        request: schemas.SelfOnboarding
) -> IDResponse:
    """ Self Onboarding organization.

        Args:
            request (schemas.SelfOnboarding): User and Organization meta.

        """
    await onboarding_service.self_onboarding(request)


@router.post("/profile",
             description="Self Onboarding Complete-Profile.",
             status_code=status.HTTP_200_OK,
             response_description="Complete-Profile Response.",
             response_model=None,
             dependencies=[Depends(auth.authenticate)]
             )
async def complete_profile(
        request: schemas.Profile
) -> UserProfile:
    """ Self Onboarding organization.

    Args:
        request (schemas.FirstSignIn):Organization meta.

    """

    return await onboarding_service.complete_profile(request)
