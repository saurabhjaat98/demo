###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepakpant@coredge.io>, Feb 2023                    #
###############################################################################
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from ccp_server.config import auth
from ccp_server.service.oidc import OIDC
from ccp_server.service.user import UserService

router = APIRouter(tags=["Auth"])

oidc: OIDC = OIDC()
user_service: UserService = UserService()


@router.get("/oidc/sso",
            description="OIDC sso for CCP.",
            status_code=status.HTTP_200_OK,
            response_description="User Profile Response.",
            )
async def sso(token: str):
    return await oidc.web_sso(token)


@router.post("/logout",
             description="Logout user.",
             status_code=status.HTTP_204_NO_CONTENT,
             dependencies=[Depends(auth.authenticate)]
             )
async def logout() -> None:
    return await user_service.logout()


@router.post("/generate-token",
             description="Generate access token from refresh token.",
             status_code=status.HTTP_200_OK,
             )
async def generate_access_token(refresh_token: str):
    return await user_service.generate_access_token(refresh_token)
