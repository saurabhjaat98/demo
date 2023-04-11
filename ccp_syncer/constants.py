from ccp_server.service.image import ImageService
from ccp_server.util.constants import Constants


class Scheduler:
    Image = 1000
    Flavor = 500
    Heat = 1000


GENERAL_SYNCER_FUNC_MAP = {Constants.MongoCollection.IMAGE: [ImageService, 'list_images', Scheduler.Image],
                           Constants.MongoCollection.FLAVOR: [ImageService, 'list_flavors', Scheduler.Flavor]}
