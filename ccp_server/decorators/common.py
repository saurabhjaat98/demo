###############################################################################
# Copyright (c) 2021-present CorEdge - All Rights Reserved                    #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepakpant@coredge.io>, June 2021                   #
###############################################################################
from functools import wraps

from fastapi import HTTPException
from pydantic import BaseModel

from ccp_server.service.providers import Provider
from ccp_server.util import ccp_context
from ccp_server.util.logger import KGLogger

LOG = KGLogger(name=__name__)


def duplicate_name(collection: str):
    """Check fo the name and matches in the provided mongo collection, if found raise exception.
    This decorators can be used in case of insertion to prevent the duplicate value
    :param collection: str mongo db collection name
    """

    def outer_wrapper(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            names = [obj.name for obj in args if isinstance(
                obj, BaseModel) and hasattr(obj, 'name')]
            name = names[0] if names else None

            if name:
                """Check for the name already exist in collection"""
                await Provider().db.check_document_by_name(collection, name, raise_exception=True)
            return await func(*args, **kwargs)

        return wrapper

    return outer_wrapper


def has_role(*roles):
    """Verify if the user's roles match any of the roles in the token associated with the
    currently logged-in user for the CCP-API server client.
    :param roles: List of roles to check like 'org-admin' or 'super-admin'"""

    def decorator(func):
        async def wrapper(request, *args, **kwargs):
            if not any(role.lower() in ccp_context.get_logged_in_user_roles() for role in roles):
                LOG.error(
                    f"{roles} do not match the required roles to access the resource")
                raise HTTPException(status_code=403,
                                    detail="Access Denied: You do not have the necessary permissions "
                                           "to perform this action. "
                                           "Please contact your administrator for assistance.")
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
