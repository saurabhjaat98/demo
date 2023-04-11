###############################################################################
# Copyright (c) 2022-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Modified by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                  #
###############################################################################
from openstack.exceptions import BadRequestException

from ccp_server.provider import models
from ccp_server.provider import services
from ccp_server.util.exceptions import CCPBadRequestException
from ccp_server.util.exceptions import CCPOpenStackException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message


class User(services.User):

    def __init__(self, connection: services.Connection):
        self.conn = connection

    @log
    def create_user(self, user: models.User, exist_ok: bool = False) -> models.User:
        """This method is used to create user in cloud.
        :param user: User object.
        :param exist_ok: If True, return None if user already exists.
        :return: dict: User access key and secret key if user is created else None."""

        payload = user.__dict__
        role = user.role
        payload.pop('role')

        try:
            # Create the user in OpenStack and adds it to the Project
            response = self.conn.connect().create_user(**payload)
        except BadRequestException as e:
            raise CCPOpenStackException(
                Message.OPENSTACK_CREATE_ERR_MSG.format('User'), e.status_code, e.details)
        except Exception:
            if not exist_ok:
                raise CCPBadRequestException(message="User is already exists")
            return None

        # Provide the Member role to the user to the project
        if user.default_project:
            self.conn.connect().grant_role(name_or_id=role, user=user.email,
                                           project=user.default_project, domain=user.domain_id)

        return response

    @log
    def get_user(self, username: str) -> models.User:
        # Fetch the user from Cloud
        return self.conn.connect().get_user(username)

    @log
    def update_user(self, resource_id: str, user: models.User) -> models.User:
        pass

    @log
    def delete_user(self, resource_id: str):
        self.conn.connect().delete_user(resource_id)

    @log
    def grant_role(self, resource_id: str, role_id: str) -> None:
        pass

    @log
    def revoke_role(self, resource_id: str, role_id: str) -> None:
        pass
