import threading
from typing import Dict
from typing import List

from ccp_server.util.constants import Constants

_request_local = threading.local()


def get_request_data():
    if _request_local.__dict__:
        return _request_local.data
    else:
        return None


def set_request_data(key: str, value: any):
    if not _request_local.__dict__:
        _request_local.data: Dict[str, any] = {}
    _request_local.data[key] = value


def clear_context():
    if _request_local.__dict__:
        del _request_local.data


def get_org() -> str:
    data = get_request_data()
    if data and Constants.CCPHeader.ORG_ID in data and data[Constants.CCPHeader.ORG_ID]:
        return data[Constants.CCPHeader.ORG_ID]


def get_cloud() -> str:
    data: str = get_request_data()
    if data and Constants.CCPHeader.CLOUD_ID in data and data[Constants.CCPHeader.CLOUD_ID]:
        return data[Constants.CCPHeader.CLOUD_ID].lower()


def get_logged_in_user() -> str:
    """Returns the username of the current request."""
    data = get_request_data()
    if data and data[Constants.CURRENT_REQUEST] and hasattr(data[Constants.CURRENT_REQUEST].state, Constants.USERNAME):
        # Get the user from the request scope
        return data[Constants.CURRENT_REQUEST].state.__getattr__(Constants.USERNAME)


def get_logged_in_token() -> str:
    """Returns the token of current user."""
    data = get_request_data()
    if data and data[Constants.CURRENT_REQUEST] and hasattr(data[Constants.CURRENT_REQUEST].state,
                                                            Constants.LOGGED_IN_USER_TOKEN):
        # Get the roles from the request scope
        return data[Constants.CURRENT_REQUEST].state.__getattr__(Constants.LOGGED_IN_USER_TOKEN)


# TODO: remove this and it's reference
def get_project_id() -> str:
    """Returns the project of current user."""
    data = get_request_data()
    if data and Constants.CCPHeader.PROJECT_ID in data and data[Constants.CCPHeader.PROJECT_ID]:
        return data[Constants.CCPHeader.PROJECT_ID]


def get_cloud_project_id() -> str:
    """Returns the cloud-project-id."""
    data = get_request_data()
    if data and data[Constants.CLOUD_PROJECT_ID] and hasattr(data[Constants.CLOUD_PROJECT_ID].state,
                                                             Constants.CLOUD_PROJECT_ID):
        # Get the cloud-project-id from the request scope
        return data[Constants.CLOUD_PROJECT_ID].state.__getattr__(Constants.CLOUD_PROJECT_ID)


def get_logged_in_user_roles() -> List[str]:
    """Returns the roles of the current request."""
    data = get_request_data()
    if data and data[Constants.CURRENT_REQUEST] and hasattr(data[Constants.CURRENT_REQUEST].state, Constants.CCP_ROLES):
        # Get the roles from the request scope
        return data[Constants.CURRENT_REQUEST].state.__getattr__(Constants.CCP_ROLES)
    elif data and Constants.CCP_ROLES in data and data[Constants.CCP_ROLES]:
        return data[Constants.CCP_ROLES]


def request_id():
    """Returns the request id of the current request."""
    data = get_request_data()
    if data and Constants.CCPHeader.AUDIT_ID in data and data[Constants.CCPHeader.AUDIT_ID]:
        return data[Constants.CCPHeader.AUDIT_ID]


def get_logged_in_user_ceph_details():
    """Returns the ceph details of the current request.
    :return: Tuple of (ceph access key, ceph secret key))"""
    data = get_request_data()
    if data and data[Constants.CURRENT_REQUEST] and \
            hasattr(data[Constants.CURRENT_REQUEST].state, Constants.CEPH_USER_ACCESS_KEY) and \
            hasattr(data[Constants.CURRENT_REQUEST].state, Constants.CEPH_USER_SECRET_KEY):
        return data[Constants.CURRENT_REQUEST].state.__getattr__(Constants.CEPH_USER_ACCESS_KEY),\
            data[Constants.CURRENT_REQUEST].state.__getattr__(
                Constants.CEPH_USER_SECRET_KEY)
