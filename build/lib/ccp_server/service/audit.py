###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved    #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Vicky Upadhyay <vicky@coredge.io>, Mar 2023                      #
###############################################################################
import datetime

from ccp_server.db.mongo import MongoAPI
from ccp_server.util import ccp_context
from ccp_server.util import env_variables
from ccp_server.util.constants import Constants


class AuditService(object):
    UNAUDITED_API_URLS = ['/docs']

    def __init__(self):
        self.db: MongoAPI = MongoAPI(
            conn_str=env_variables.AUDIT_DB_URL,
            db_name=Constants.CCP_AUDIT_DB_NAME
        )

    async def create_audit_collection(self):
        await self.db.create_capped_collection(Constants.MongoCollection.AUDIT_COLLECTION_NAME,
                                               max_size_bytes=Constants.
                                               CAPPED_COLLECTION_MAX_SIZE_BYTES,
                                               max_count=Constants.CAPPED_COLLECTION_MAX_NUM_ENTRIES)

    async def write_audit_log(self, request, status_code, request_id, start_time, process_time):
        """
        Write audit log to database
        :param request: HTTPRequest: Request object
        :param status_code: int: Response code
        :param request_id: str: Request ID
        :param start_time: str:  Start time
        :param process_time: long: Process time
        """
        # Check if the request URL contains any of the un-audited APIs
        if request.url.path in self.UNAUDITED_API_URLS:
            return

        # Convert the str time into datetime object
        start_time = datetime.datetime.utcfromtimestamp(start_time)

        # Openstack CADF audit log model
        audit_log = {
            "audit_id": request_id,
            "event": {
                "time": start_time,
                "action": request.url.path,
                "type": request.method,
                "outcome": {"reason": status_code},
                "duration": process_time,
            },
            "target": {
                "id": request.url.path,
                "type": request.method,
            },
            "initiator": {
                "id": ccp_context.get_logged_in_user(),
                "type": ccp_context.get_logged_in_user_roles(),
                "host": {
                    "agent": request.headers.get("Referer", "unknown"),
                    "address": request.headers.get("X-Forwarded-For", request.client.host),
                }
            },
            "observer": {
                "id": "CCP_APP"
            },
            "tag": [
                {
                    "name": "org_id",
                    "value": ccp_context.get_org()
                },
                {
                    "name": "cloud_id",
                    "value": ccp_context.get_cloud()
                },
                {
                    "name": "project_id",
                    "value": ccp_context.get_project_id()
                }
            ]
        }

        await self.db.write_document(Constants.MongoCollection.AUDIT_COLLECTION_NAME, audit_log)
