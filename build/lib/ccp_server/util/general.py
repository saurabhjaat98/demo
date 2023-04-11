###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Manik Sidana <manik@coredge.io>, Feb 2023                        #
# Modified by Saurabh Choudhary <saurabhchoudhary@coredge.io>, March 2023     #
###############################################################################
from ccp_server.util.exceptions import InvalidTypeException
from ccp_server.util.logger import log


@log
def remove_key_from_dict(key, val_dict):
    """Method to remove all occurrences of a key in dictionary.
    Modifies the dict in place

    Args:
        key (str): key to be removed
        val_dict (dict): Dict from which the key is to be removed

    Raises:
        InvalidTypeException: If key is not of str type.
    """
    if not isinstance(key, str):
        raise InvalidTypeException(f'Expected string but received {type(key)}')

    for k, v in list(val_dict.items()):
        if k == key:
            del val_dict[k]
        elif isinstance(v, dict):
            remove_key_from_dict(key, v)
        elif isinstance(v, list):
            for _ in v:
                remove_key_from_dict(key, _)
    return val_dict


@log
def flatten_dict(obj, parent_key='', sep='.'):
    items = []
    for k, v in obj.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k

        # Recursively flatten nested dictionaries
        if isinstance(v, dict):
            new_dict = flatten_dict(v, new_key)
            items.extend(new_dict.items())

        # If value is a list of strings, append to items list
        elif isinstance(v, list) and all(isinstance(item, str) for item in v):
            items.append((new_key, v))

        # Recursively flatten nested dictionaries within a list
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    new_sub_key = f"{new_key}{sep}{i}"
                    new_dict = flatten_dict(item, new_sub_key)
                    items.extend(new_dict.items())
                else:
                    items.append((f"{new_key}{sep}{i}", item))

        # If value is not a list or a dictionary, append to items list
        else:
            items.append((new_key, v))

    # Convert items list to dictionary and return
    return dict(items)
