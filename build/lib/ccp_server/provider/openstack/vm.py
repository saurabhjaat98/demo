###############################################################################
# Copyright (c) 2022-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
# Modified by Pankaj Khanwnai <pankaj@coredge.io>, Feb 2023                   #
###############################################################################
from ccp_server.provider import models
from ccp_server.provider import services
from ccp_server.util.logger import log


class VM(services.VM):
    def __init__(self, connection: services.Connection):
        self.conn = connection

    @log
    async def create_vm(self, vm: models.VM):
        pass

    @log
    async def update_vm(self, resource_id: str, vm: models.VM) -> models.VM:
        pass

    @log
    async def delete_vm(self, resource_id: str):
        pass
