###############################################################################
# Copyright (c) 2022-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Modified by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                  #
###############################################################################
from openstack.exceptions import BadRequestException

from ccp_server.provider import models
from ccp_server.provider import services
from ccp_server.provider.openstack.mapper.mapper import mapper
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPOpenStackException
from ccp_server.util.logger import log
from ccp_server.util.messages import Message


class Project(services.Project):

    def __init__(self, connection: services.Connection):
        self.conn = connection
        self.collection = Constants.MongoCollection.PROJECT

    @log
    async def create_project(self, project: models.Project) -> models.Project:
        try:
            cloud_res = self.conn.connect().create_project(**project.__dict__)
            return await mapper(data=cloud_res, resource_name=self.collection)
        except BadRequestException as e:
            raise CCPOpenStackException(Message.OPENSTACK_CREATE_ERR_MSG.format(
                'Project'), e.status_code, e.details)

    @log
    async def update_project(self, name_or_id, new_description) -> models.Project:
        return self.conn.connect().update_project(name_or_id=name_or_id, description=new_description)

    @log
    async def delete_project(self, project_name):
        return self.conn.connect().delete_project(name_or_id=project_name)

    @log
    async def add_member(self, cloud_project_id: str, username: str, role: str, ):
        return self.conn.connect().grant_role(project=cloud_project_id, user=username, name_or_id=role)

    @log
    async def remove_member(self, cloud_project_id: str, username: str, role: str, ):
        return self.conn.connect().revoke_role(project=cloud_project_id, user=username, name_or_id=role)

    @log
    async def list_projects(self):
        cloud_res = self.conn.connect().list_projects()
        return await mapper(data=cloud_res, resource_name=self.collection)
