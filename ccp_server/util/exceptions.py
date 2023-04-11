###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Manik Sidana <manik@coredge.io>, Feb 2023                        #
###############################################################################
# msidana: For extensability, later.
import traceback

from starlette import status

from ccp_server.util.logger import KGLogger
from ccp_server.util.messages import Message

UNAUTHENTICATED_EXCEPTION_ERR_MSG = "Access Denied: User is not authenticated to perform the operation."
NOT_FOUND_EXCEPTION_ERR_MSG = "Not Found: The requested resource could not be found."
BAD_REQUEST_EXCEPTION_ERR_MSG = "Bad Request: The request could not be understood by the server due to a client error."
UNAUTHORISED_EXCEPTION_ERR_MSG = "Unauthorized: User is not authorized to access the resource."
OPENSTACK_EXCEPTION_ERR_MSG = "OpenStack Error: Exception occurred while performing operation on OpenStack resource."
KEYCLOAK_EXCEPTION_ERR_MSG = "Keycloak Error: Exception occurred while performing operation on Keycloak resource."
CLOUD_EXCEPTION_ERR_MSG = "Cloud Error: Exception occurred while performing operation on Cloud resource."
IAM_EXCEPTION_ERR_MSG = "IAM Error: Exception occurred while performing operation on IAM resource."
CCP_EXCEPTION_ERR_MSG = "CCP Error: Exception occurred while performing operation on CCP resource."
AUTH_EXCEPTION_ERR_MSG = "Authentication Error: Exception occurred while performing operation on Authentication " \
                         "resource. "
BUSINESS_EXCEPTION_ERR_MSG = "Business Error: Exception occurred while performing operation "
CEPH_EXCEPTION_ERR_MSG = "CEPH Error: Exception occurred while performing operation on CEPH resource."
PROFILE_NOT_COMPLETED_EXCEPTION_ERR_MSG = "Profile Not Completed: Please complete your profile first."
EMAIL_NOT_SUPPORTED_ERR_MSG = "Email Not Supported: Please provide a business email address"
FILE_NOT_FOUND_ERR_MSG = "File Not Found: The requested file could not be found."
LOG = KGLogger(name=__name__)


class CCPException(Exception):
    """ Parent Exception for CCP related exceptions """

    def __init__(self, message=CCP_EXCEPTION_ERR_MSG, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.status_code = status_code
        self.message = message

    def print(self):
        traceback.print_exc()
        LOG.error(
            f'{self.__class__.__name__}: {self.status_code} {self.message}')


class InvalidTypeException(CCPException):
    """ Exception for invalid type """
    pass


class CCPBusinessException(CCPException):
    """ Parent Exception for Business related exceptions """

    def __init__(self, message=BUSINESS_EXCEPTION_ERR_MSG, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY):
        self.status_code = status_code
        self.message = message


class CCPAuthException(CCPException):
    def __init__(self, message=AUTH_EXCEPTION_ERR_MSG, status_code=status.HTTP_401_UNAUTHORIZED):
        self.message = message
        self.status_code = status_code


class CCPCloudException(CCPException):
    """ Parent Exception for Cloud related exceptions """

    def __init__(self, message=CLOUD_EXCEPTION_ERR_MSG, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code


class CCPIAMException(CCPException):
    """ Parent Exception for IAM related exceptions """

    def __init__(self, message=IAM_EXCEPTION_ERR_MSG, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code


class CCPOpenStackException(CCPCloudException):
    """ Parent Exception for OpenStack related exceptions """

    def __init__(self, message=OPENSTACK_EXCEPTION_ERR_MSG, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                 detail=None):
        self.message = message
        self.details = {
            "code": "CCP-{}".format(status_code),
            "message": detail
        }
        self.status_code = status_code


class CCPCephException(CCPCloudException):
    """ Parent Exception for Ceph related exceptions """

    def __init__(self, message=CEPH_EXCEPTION_ERR_MSG, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code


class CCPKeycloakException(CCPIAMException):
    """ Parent Exception for Keycloak related exceptions """

    def __init__(self, message=KEYCLOAK_EXCEPTION_ERR_MSG, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code


class CCPNotFoundException(CCPBusinessException):
    """ Parent Exception for Not Found related exceptions """

    def __init__(self, message=NOT_FOUND_EXCEPTION_ERR_MSG, status_code=status.HTTP_404_NOT_FOUND):
        self.message = message
        self.status_code = status_code


class CCPBadRequestException(CCPBusinessException):
    """ Parent Exception for Bad Request related exceptions """

    def __init__(self, message=BAD_REQUEST_EXCEPTION_ERR_MSG, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code


class CCPUnauthorizedException(CCPAuthException):
    """ Parent Exception for Unauthorized related exceptions """

    def __init__(self, message=UNAUTHORISED_EXCEPTION_ERR_MSG, status_code=status.HTTP_401_UNAUTHORIZED):
        self.status_code = status_code
        self.message = message


class CCPUnauthenticatedException(CCPAuthException):
    """ Parent Exception for Unauthenticated related exceptions """

    def __init__(self, message=UNAUTHENTICATED_EXCEPTION_ERR_MSG, status_code=status.HTTP_403_FORBIDDEN):
        self.status_code = status_code
        self.message = message


class CCPProfileNotCompletedException(CCPAuthException):
    """ Parent Exception for Unauthenticated related exceptions """

    def __init__(self, message=PROFILE_NOT_COMPLETED_EXCEPTION_ERR_MSG, status_code=status.HTTP_424_FAILED_DEPENDENCY):
        self.status_code = status_code
        self.message = message


class CCPEmailNotSupportedException(CCPBusinessException):
    """ Parent Exception for unsupported public email related exceptions """

    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, message=EMAIL_NOT_SUPPORTED_ERR_MSG):
        self.status_code = status_code
        self.message = message


class CCPPincodeNotFoundException(CCPBusinessException):
    """ Parent Exception for invalid pincode related exceptions """

    def __init__(self, status_code=status.HTTP_400_BAD_REQUEST, message=Message.PINCODE_NOT_FOUND_ERR_MSG):
        self.status_code = status_code
        self.message = message


class CCPFileNotFoundException(CCPException):
    """ Parent Exception for File Not Found related exceptions """

    def __init__(self, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=FILE_NOT_FOUND_ERR_MSG):
        self.status_code = status_code
        self.message = message
