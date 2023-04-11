###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Vicky Upadhyay <vicky@coredge.io>, Feb 2023                      #
# Modified by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                   #
###############################################################################
from typing import Dict

from pydantic.types import StrictBool

from ccp_server.schema.v1.response_schemas import Pageable
from ccp_server.service.providers import Provider
from ccp_server.util.constants import Constants
from ccp_server.util.logger import log


class ImageService(Provider):

    def __init__(self):
        self.collection = Constants.MongoCollection.IMAGE

    @log
    async def list_images(self, pageable: Pageable = None,
                          use_db: StrictBool = True):

        """
        List all images.
        :param pageable: Pageable object
        :param use_db: If true it will fetch the result from Mongo, else from cloud
        :return: List of images and total count.
        """
        if use_db:
            return await self.db.get_document_list_by_ids(
                collection_name=self.collection, exclude_org=True,
                pageable=pageable)
        else:
            cloud_response = await self.connect.image.list_images()
            return cloud_response, len(cloud_response)

    @log
    async def get_image(self, image_id) -> Dict:
        """
        Get image by id.
        :param image_id: Id of the image.
        :return: Image details.
        """
        return await self.db.get_document_by_uuid(self.collection, image_id)
