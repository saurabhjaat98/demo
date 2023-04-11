###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Pankaj Khanwani <pankaj@coredge.io>, Feb 2023                    #
###############################################################################
import logging
import traceback

log = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format=f'%(asctime)s %(process)d %(levelname)s Syncer %(filename)s:%(lineno)d %(message)s')
file_handler = logging.FileHandler('/var/log/stack_resources.log')
file_handler.setLevel(logging.INFO)
log.addHandler(file_handler)


class StackResources:
    """
    This class is used to extract the Stack Resources.
    """

    def __init__(self, conn, resource_collection_map={}):
        """
        Constructor for the Resources class
        :param conn: Connection object of the cloud
        :param resource_collection_map: A Resource Collection Map should have the format below:
                                        {'Flavor': ['Flavor', 'get_flavor'],
                                        'FloatingIP': ['FloatingIP', 'get_floating_ip'],
                                        'Image': ['Image', 'get_image'],
                                        'KeyPair': ['KeyPair', 'get_keypair'],
        where key is the name of the stack resource type and the value is a list
        the first element of the list is the name of the resource and
        the second element is the function to get the resource.
        """
        self.conn = conn
        self.method = None
        self.resource_id = None
        self.resource_details = {}
        self.resource_collection_map = resource_collection_map

    def fetch_detailed_cloud_resource(self, collection_name, method_name):
        """
        This method is used to get the cloud resource for each resource type
        :param collection_name: Name of the collection which you are using in Mongo DB
        :param method_name: Name of the method which you are calling for your cloud resource
        :return: Returns the cloud resource for the resource type
        Stores the cloud resource in the self.resource_details dictionary where,
        key is the collection name of the cloud and the value is another dictionary where,
        key is the resource id and the value is the cloud resource
        """
        cloud_method = getattr(self.conn, method_name)
        try:
            result = cloud_method(self.resource_id)
            if result:
                result = dict(result)
                result['source_id'] = self.stack_id
                self.resource_details[collection_name] = self.resource_details.get(
                    collection_name, {})
                self.resource_details[collection_name][self.resource_id] = result
        except Exception:
            log.error(f"Error while getting cloud resource")
            log.error(traceback.print_exc())

    def list_all_stack_resources(self):
        """
        This method is used to list all the stack resources
        :return: Returns a list of all the stack resources
        """
        try:
            total_stack_resources = []
            stacks = self.conn.list_stacks()
            for stack in stacks:
                stack_id = stack.id
                resources = self.conn.orchestration.resources(stack)
                for resource in resources:
                    resource.stack_id = stack_id
                    total_stack_resources.append(resource)
            return total_stack_resources
        except Exception:
            log.error(f"Error while getting all stack resources")
            log.error(traceback.print_exc())

    def fetch_detailed_resource_to_dict_of_dict(self, stack_resources):
        """
        This method is used to get the cloud resource for each resource type
        :param stack_resources: List of all the stack resources
        :return: None
        Stores all the resources in dictionary format inside self.resource_details
        """
        try:
            for resource in stack_resources:
                resource_type = resource.resource_type.split('::')[-1]
                self.resource_id = resource.physical_resource_id
                self.stack_id = resource.stack_id
                if resource_type in self.resource_collection_map:
                    self.fetch_detailed_cloud_resource(collection_name=self.resource_collection_map[resource_type][0],
                                                       method_name=self.resource_collection_map[resource_type][1])

            return self.resource_details
        except Exception:
            log.error(f"Error while converting list resources to dict of dict")
            log.error(traceback.print_exc())
