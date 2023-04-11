###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
import traceback

import yaml

from ccp_server.provider.openstack.mapper.schemas import Schemas
from ccp_server.util import ccp_context
from ccp_server.util.logger import KGLogger
from ccp_server.util.logger import log
from ccp_server.util.utils import Utils
LOG = KGLogger(__name__)


@log
def populate_cloud_type(cloud_type: str = None, cloud: str = None):
    """
    Populate the cloud type
    :param cloud_type:
    :param cloud:
    :return: cloud_type
    """
    try:
        if cloud:
            cloud_type = Utils.load_clouds_yaml()['clouds'][cloud]['type']
        else:
            cloud = ccp_context.get_cloud()
            cloud_type = Utils.load_clouds_yaml()['clouds'][cloud]['type']
        return cloud, cloud_type
    except Exception as e:
        LOG.error(e)
        raise Exception(f"{cloud_type} does not exist") from e


@log
async def mapper(resource_name: str, data, cloud: str = None, cloud_type: str = None):
    """
    This function is used to map the data to the mongo schema
    :param data: data to be mapped
    :param resource_name: name of the resource
    :param cloud: cloud name
    :param cloud_type: cloud type
    """
    try:
        if not cloud or not cloud_type:
            cloud, cloud_type = populate_cloud_type(cloud=cloud)
        mapobj = MapperClass(data, resource_name, cloud, cloud_type)
        await mapobj.create(data)
        return mapobj.data
    except Exception as e:
        LOG.error(traceback.print_exc())
        raise Exception(
            f"Unable to create Mapper for {resource_name} due to {e}")


class MapperClass:
    """
    This class is used to map the data to the mongo schema
    """
    __TYPE__ = None
    image = None
    network = None

    @log
    def __init__(self, data, resource_name: str, cloud: str = None, cloud_type: str = None):
        self.resource_name = resource_name
        self.cloud = cloud
        self.cloud_type = cloud_type
        self.data = data

    @log
    async def create(self, data):
        if isinstance(data, list):
            self.data = await self.handle_list(data)
        else:
            self.data = await self.translate(data)
        return self.data

    @log
    async def handle_list(self, data):
        obj_list = []
        for item in data:
            obj_list.append(await self.translate(item))
        return obj_list

    async def fetch_resource_map_yaml(self):
        """
        Fetch the resource map from yaml
        :return cloud_map in dictionary format:
        """
        with open(Utils.get_mapper_yaml_path(), "r") as f:
            resource_map = yaml.safe_load(f)

        if self.cloud_type in resource_map and self.resource_name.lower() in resource_map[self.cloud_type]:
            return resource_map[self.cloud_type][self.resource_name.lower()]
        else:
            error_message = f"Unable to find {self.resource_name} in {self.cloud_type}"
            LOG.error(error_message)
            raise Exception(
                f"{self.cloud_type} Mapper does not have {self.resource_name} variable: {error_message}")

    @log
    async def fetch_resource_map_from_dictmap(self):
        for sub_class in MapperClass.__subclasses__():
            if sub_class.__TYPE__ == self.cloud_type:
                return sub_class.__dict__[self.resource_name.lower()]
        LOG.error(f'Unable to find {self.resource_name} in {self.cloud_type}')
        raise Exception(
            f"{self.cloud_type} Mapper does not have {self.resource_name} variable")

    @log
    async def flatten_dict(self, obj, parent_key='', sep='.'):
        try:
            items = []

            # Check if obj is a dict, otherwise convert it to one
            try:
                obj_items = obj.items()
            except AttributeError:
                obj = dict(obj)
                obj_items = obj.items()

            for k, v in obj_items:
                new_key = f"{parent_key}{sep}{k}" if parent_key else k

                # Recursively flatten nested dictionaries
                if isinstance(v, dict):
                    new_dict = await self.flatten_dict(v, new_key, sep=sep)
                    items.extend(new_dict.items())

                # If value is a list of strings, append to items list
                elif isinstance(v, list) and all(isinstance(item, str) for item in v):
                    items.append((new_key, v))

                # Recursively flatten nested dictionaries within a list
                elif isinstance(v, list):
                    for i, item in enumerate(v):
                        if isinstance(item, dict):
                            new_sub_key = f"{new_key}{sep}{i}"
                            new_dict = await self.flatten_dict(item, new_sub_key, sep=sep)
                            items.extend(new_dict.items())
                        else:
                            items.append((f"{new_key}{sep}{i}", item))

                # If value is not a list or a dictionary, append to items list
                else:
                    items.append((new_key, v))

            # Convert items list to dictionary and return
            return dict(items)

        # If an exception is raised, log an error message
        except Exception as e:
            LOG.error(f"Unable to flatten {obj} due to {e}")

    @log
    async def translate(self, obj: dict):
        try:
            # Choosing which map to use according to the cloud_type and resource_name
            mapper = await self.fetch_resource_map_yaml()

            # Flattening the data from the cloud
            converted_obj = await self.flatten_dict(obj)

            if type(obj) != type(dict):
                obj = dict(obj)
            converted_obj['cloud_meta'] = obj
            converted_obj['cloud'] = self.cloud

            # Convert the OpenStack data to the Pydantic model data
            for key in mapper.keys():
                converted_obj[key] = converted_obj.get(mapper[key])

            # Checking if the resource_name has the Schema or not
            if hasattr(Schemas, self.resource_name.title()):
                # Returning the converted obj to the Schema according to the resource_name
                return getattr(Schemas, self.resource_name.title())(**converted_obj)
            else:
                LOG.error(
                    f'Unable to find Schema of {self.resource_name.title()} in {Schemas}')
                raise Exception(
                    f"Schema: {self.resource_name.title()} does not exist")

        except Exception as e:
            raise Exception(
                f"Unable to translate {self.resource_name} due to {e}")
