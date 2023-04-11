###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Deepak Pant <deepakpant@coredge.io>, Feb 2023                    #
###############################################################################
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import StrictStr

from ccp_server.util.enums import Status


class Mixins(BaseModel):
    created_by: str
    updated_by: Optional[str]


class Base(Mixins):
    name: str
    description: Optional[str]
    cloud: Optional[str]
    org_id: Optional[str]
    project_id: Optional[str]
    cloud_meta: Optional[Dict[StrictStr, Any]]
    active: Status


class Flavor(Base):
    vcpus: int
    ram: int
    disk: int
    ephemeral: Optional[int]
    swap: Optional[int]
    rxtx_factor: Optional[int]


class Instance(Base):
    pass


class Page:

    def __init__(self, page: int, size: int, total: int, data: List[Dict[str, Any]]):
        self.page: int = page
        self.size: int = size
        self.total: int = total
        self.data: List[Dict[str, Any]] = data


class IDResponse:

    def __init__(self, doc_id: str):
        self.id: str = doc_id


class Pageable:

    def __init__(self, query_str: str, page: int, size: int, sort_by: List[str],
                 sort_desc: bool, tags: List[str] = None):
        self.page: int = page
        self.size: int = size
        self.query_str: str = query_str
        self.sort_by: List[str] = sort_by
        self.sort_desc: bool = sort_desc
        self.tags: Dict[str, str] = self.populate_tags(tags)

    def populate_tags(self, tags):

        # if tag has = then only consider it a valid tag, otherwise ignore it and there should be only one '='

        if tags:
            tag_dict = {}
            for item in tags:
                if "=" in item:
                    key, value = item.split('=')
                    tag_dict[key] = value
            return tag_dict
