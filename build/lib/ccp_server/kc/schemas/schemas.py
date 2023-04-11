###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                   #
###############################################################################
from typing import List


class Group:
    def __init__(self, name: str):
        self.name: str = name


class User:

    def __init__(self, first_name: str, last_name: str, email: str, mobile_number: str = None,
                 groups: List[str] = None, roles: List[str] = None):
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.mobile_number: str = mobile_number
        self.groups: List[str] = groups
        self.roles: List[str] = roles
