import json
import os
import re
import uuid
from datetime import datetime
from datetime import timezone
from typing import Any
from typing import Dict
from typing import Set

import yaml
from distutils.sysconfig import get_python_lib

from ccp_server.util import ccp_context
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPBadRequestException
from ccp_server.util.exceptions import CCPEmailNotSupportedException
from ccp_server.util.exceptions import CCPFileNotFoundException
from ccp_server.util.exceptions import CCPPincodeNotFoundException
from ccp_server.util.logger import KGLogger
from ccp_server.util.messages import Message

CLOUDS_YAML_DEFAULT_PATH = '/etc/ccp/clouds.yaml'
CLOUDS_YAML_LOCAL_PATH = 'clouds.yaml'
CLOUDS_YAML_SYNCER_PATH = '../clouds.yaml'

LOG = KGLogger(__name__)


class Utils:
    """This class contains utility methods for CCP."""

    def __init__(self):
        pass

    _CLOUD_CONFIG_DATA: Dict[str, Dict[str, Any]] = {}
    _DEFAULT_CLOUD: str = None
    _RESTRICTED_EMAIL_DATA: set = {}
    _PINCODE_DATA: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def load_clouds_yaml() -> Dict[str, Dict[str, Any]]:
        """This method loads the clouds.yaml file from the default path or local path.
        First preference is the default path and then local path.\n
        default path: /etc/ccp/clouds.yaml\n
        local path: ../../clouds.yaml\n
        :return: Dict[str, Any]
        """

        if Utils._CLOUD_CONFIG_DATA:
            return Utils._CLOUD_CONFIG_DATA
        elif Utils.is_file_exist(CLOUDS_YAML_DEFAULT_PATH):
            Utils._CLOUD_CONFIG_DATA = Utils.read_yaml(
                CLOUDS_YAML_DEFAULT_PATH)
        elif Utils.is_file_exist(CLOUDS_YAML_LOCAL_PATH):
            Utils._CLOUD_CONFIG_DATA = Utils.read_yaml(CLOUDS_YAML_LOCAL_PATH)
        elif Utils.is_file_exist(CLOUDS_YAML_SYNCER_PATH):
            Utils._CLOUD_CONFIG_DATA = Utils.read_yaml(CLOUDS_YAML_SYNCER_PATH)
        else:
            raise FileNotFoundError(
                f"{CLOUDS_YAML_DEFAULT_PATH} or {CLOUDS_YAML_LOCAL_PATH} does not exist")
        return Utils._CLOUD_CONFIG_DATA

    @staticmethod
    def load_pincode_json() -> Dict[str, Dict[str, Any]]:
        """This method loads the pincode.json file from the default path or local path.
                First preference is the default path and then local path.\n
                local path: files/pincode.json
                :return: Dict[str, Any]
                """
        if Utils._PINCODE_DATA:
            return Utils._PINCODE_DATA
        elif Utils.is_file_exist(Constants.PINCODE_JSON_FILE_DEFAULT_PATH):
            Utils._PINCODE_DATA = json.load(
                open(Constants.PINCODE_JSON_FILE_DEFAULT_PATH))
        elif Utils.is_file_exist(Constants.PINCODE_JSON_FILE_LOCAL_PATH):
            Utils._PINCODE_DATA = json.load(
                open(Constants.PINCODE_JSON_FILE_LOCAL_PATH))
        else:
            raise CCPFileNotFoundException(
                f"{Constants.PINCODE_JSON_FILE_DEFAULT_PATH} or {Constants.PINCODE_JSON_FILE_LOCAL_PATH}"
                f" does not exist")
        return Utils._PINCODE_DATA

    @staticmethod
    def get_details_by_pincode(pincode: str) -> Dict[str, Any]:
        try:
            pincode_data = Utils.load_pincode_json()[pincode]
            return {'country': pincode_data['country'], 'city': pincode_data['city'],
                    'state': pincode_data['state']}
        except KeyError:
            raise CCPPincodeNotFoundException(
                message=Message.PINCODE_NOT_FOUND_ERR_MSG.format(pincode))

    @staticmethod
    def load_restricted_email_json() -> Set:
        """
        This method loads the restricted email.json file from the default path or local path.
        default path: ccp_app/.venv/lib/python3.10/site-packages/ccp_server/files/restricted_domains.json
        local path: files/restricted_domains.json
        :return: Dict[str, Any]
        """
        if Utils._RESTRICTED_EMAIL_DATA:
            return Utils._RESTRICTED_EMAIL_DATA
        elif Utils.is_file_exist(Constants.RESTRICTED_EMAIL_FILE_DEFAULT_PATH):
            Utils._RESTRICTED_EMAIL_DATA = set(
                json.load(open(Constants.RESTRICTED_EMAIL_FILE_DEFAULT_PATH)))
        elif Utils.is_file_exist(Constants.RESTRICTED_EMAIL_FILE_LOCAL_PATH):
            Utils._RESTRICTED_EMAIL_DATA = set(
                json.load(open(Constants.RESTRICTED_EMAIL_FILE_LOCAL_PATH)))
        else:
            raise FileNotFoundError(
                f"{Constants.RESTRICTED_EMAIL_FILE_DEFAULT_PATH} or {Constants.RESTRICTED_EMAIL_FILE_LOCAL_PATH} "
                f"does not exist")
        return Utils._RESTRICTED_EMAIL_DATA

    @staticmethod
    def load_cloud_details(cloud_name: str):
        return Utils.load_clouds_yaml().get("clouds").get(cloud_name)

    @staticmethod
    def load_supported_clouds() -> Set[str]:
        return Utils.load_clouds_yaml().get("clouds").keys()

    @staticmethod
    def load_supported_cloud_details() -> Dict[str, Any]:
        return Utils.load_clouds_yaml().get("clouds")

    @staticmethod
    def default_cloud() -> str:
        if Utils._DEFAULT_CLOUD is None:
            clouds_data = Utils.load_supported_cloud_details()
            clouds = [cloud for cloud in clouds_data if clouds_data[cloud].get(
                'default', None) is True]
            if clouds:
                Utils._DEFAULT_CLOUD = clouds[0]
        return Utils._DEFAULT_CLOUD

    @staticmethod
    def get_default_cloud(cloud: str = None) -> str:
        if cloud:
            return cloud
        return Utils.default_cloud()

    @staticmethod
    def is_file_exist(file_path: str) -> bool:
        return os.path.exists(file_path)

    @staticmethod
    def read_yaml(file_path: str) -> dict:
        with open(file_path) as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as exc:
                raise Exception(exc)

    @staticmethod
    def generate_unique_str():
        """
        Generate a unique string consists of org_id, cloud_id, project_id and uuid.
        It takes first 4 alphanumeric characters of org_id and cloud_id and project_id
        :return: str: a unique string
        """
        org_prefix = Utils.alphanumeric_str(ccp_context.get_org(), 4, '-')
        cloud_prefix = Utils.alphanumeric_str(ccp_context.get_cloud(), 4, '-')
        project_prefix = Utils.alphanumeric_str(
            ccp_context.get_project_id(), 4, '-')
        uid = str(uuid.uuid4())
        return f'{org_prefix}{cloud_prefix}{project_prefix}{uid}'

    @staticmethod
    def alphanumeric_str(string: str, length: int, postfix: str = '') -> str:
        """
        Convert string to alphanumeric string.
        :param string: string to be converted.
        :param length: length of the alphanumeric string.
        :param postfix: postfix of the alphanumeric string.
        :return: alphanumeric string.
        """
        result = ''.join(filter(str.isalnum, string))[
                 :length] if string else ''
        return result + (postfix if postfix else '') if result else ''

    @staticmethod
    def generate_uuid4():
        return str(uuid.uuid4())

    @staticmethod
    def extract_id_from_path(path: str, path_id_str: str):
        """ Extract the uuid from the path. Provide the path and the id type string.
        :param path: path to be extracted like path as '/api/v1/projects/684feb89-3c7a-4cbd-a25e-caa1b96be9a8'.
        :param path_id_str: id type string like 'projects'
        :return: uuid like '684feb89-3c7a-4cbd-a25e-caa1b96be9a8'
        """
        path_id_regex = Constants.PATH_ID_REGEX.format(path_id_str)
        match = re.search(fr'{path_id_regex}', path)
        if match:
            # extract the id from the path
            id_str = match.group(0).replace(f'/{path_id_str}/', '').rstrip('/')
            if Utils.is_valid_uuid(id_str):
                return id_str
        return None

    @staticmethod
    def get_mapper_yaml_path():
        """
        Get the mapper yaml path.
        :return: Yaml Path
        """
        SITE_PKG_MAPPER_PATH = os.path.join(
            get_python_lib(), Constants.MAPPER_YAML_PATH)
        if os.path.exists(SITE_PKG_MAPPER_PATH):
            return SITE_PKG_MAPPER_PATH
        elif os.path.exists(Constants.MAPPER_YAML_PATH):
            return Constants.MAPPER_YAML_PATH
        else:
            err = f'mapper not found at {Constants.MAPPER_YAML_PATH} and {SITE_PKG_MAPPER_PATH}'
            LOG.error(err)
            raise FileNotFoundError("Mapper not found.")

    @staticmethod
    def is_email_supported(value):
        """
        This method is used to verifying email is public or not.
        """
        if not value:
            raise CCPBadRequestException()
        email_provider = value.split('@')[1]
        public_domains = Utils.load_restricted_email_json()
        if email_provider in public_domains:
            raise CCPEmailNotSupportedException()

        return value

    @staticmethod
    def get_utc_datetime():
        """
        This method is used to get the utc datetime.
        """
        return datetime.utcnow()

    @staticmethod
    def is_found(attr, attr_list):
        """
        This method is used to check if the attr is in the attr_list.
        :param attr: attribute to be checked.
        :param attr_list: list of attributes.
        """
        return any(attr for a in attr_list if a == attr)

    @staticmethod
    def to_utc_datetime(timestamp):
        """
        This method is used to convert the timestamp to utc datetime.
        :param timestamp: timestamp to be converted.
        :return: utc datetime.
        """
        dt_object = datetime.fromtimestamp(timestamp / 1000)
        return dt_object.astimezone(timezone.utc)

    @staticmethod
    def is_valid_uuid(val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False
