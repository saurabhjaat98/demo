###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepakpant@coredge.io>, Mar 2023                    #
###############################################################################


class Message:
    """Class to hold all the exception messages at one place"""
    USER_DOESNT_HAVE_ORG = 'User does not belongs to any organisation.'
    USER_ALREADY_EXISTS = 'User {} is already exists.'
    INVALID_EMAIL_ACTION = 'Please provide the supported email action.'
    USER_DOESNT_HAVE_PROJECT = 'User does not belongs to any project.'
    EMAIL_NOT_VERIFIED = 'Please verify your email before performing any action.'
    TOKEN_EXPIRED = 'Your access token is expired or invalid.'
    CLOUD_NOT_VALID = 'Please provide a supported cloud id.'
    ORG_NOT_VALID = 'The organisation is either invalid or deleted or not belongs to you.'
    PROJECT_NOT_VALID = 'The project is either invalid or deleted or not belongs to you.'
    DOCUMENT_WITH_UUID_NOT_FOUND = 'Document with UUID {} not found in the database.'
    NAME_ALREADY_EXISTS = 'An entry already exist in the database with the same name {}.'
    UUID_ALREADY_EXISTS = 'An entry already exist in the database with the same UUID {}.'
    TOKEN_EMPTY = 'Your access token is empty.'
    USER_EXITS = 'User already exists with the same email id.'
    PROFILE_COMPLETED = 'Your Profile is already completed. Please login to perform any operation'
    DOCUMENT_LIST = 'The document should be in list.'
    VOLUME_ALREADY_ATTACHED = 'Volume ID {} is already attached to the instance ID {}'
    VOLUME_NOT_ATTACHED = 'Volume ID {} is not attached to the instance ID {}'
    TAG_MAX_LENGTH_EXCEEDED = 'Tag length cannot be more than {}'
    PINCODE_NOT_FOUND_ERR_MSG = "Pincode {} not found. Please provide a valid pincode."
    PINCODE_NOT_MATCH = "The information you provided for the city, state, and country does not match the pincode {}."
    OPENSTACK_CONNECTION_ERR_MSG = "Unable to connect to cloud {}"
    CEPH_CONNECTION_ERR_MSG = "Unable to connect with storage of {}"
    OPENSTACK_CREATE_ERR_MSG = "Failed to create {}"
