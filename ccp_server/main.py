##############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved    #
# Unauthorized copying of this file, via any medium is strictly prohibited   #
# Proprietary and confidential                                               #
# Written by Deepak Pant <deepak.pant@coredge.io>, Feb 2023                  #
##############################################################################
from __future__ import annotations

import os
import time
import traceback

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_health import health
from git import Repo
from starlette.middleware.cors import CORSMiddleware

from ccp_server.api.v1 import api_router
from ccp_server.api.v1 import base_router
from ccp_server.api.v1 import org_admin_api_router
from ccp_server.api.v1 import org_api_router
from ccp_server.api.v1 import public_router
from ccp_server.api.v1.auth import router as oidc_router
from ccp_server.config import auth
from ccp_server.service.audit import AuditService
from ccp_server.util import ccp_context
from ccp_server.util import logger
from ccp_server.util.constants import Constants
from ccp_server.util.exceptions import CCPAuthException
from ccp_server.util.exceptions import CCPBusinessException
from ccp_server.util.exceptions import CCPCloudException
from ccp_server.util.exceptions import CCPIAMException
from ccp_server.util.logger import KGLogger
from ccp_server.util.utils import Utils

LOG = KGLogger(name=__name__)

BASE_PATH = "/api/v1"
PORT = os.environ.get('APP_PORT', 7080)
HOST = os.environ.get('APP_HOST', "0.0.0.0")
CATALOGUE = {}

g_audit_service = AuditService()


async def health_check() -> dict:
    """Function to check if the service is up and running"""
    return {"status": "OK"}


async def on_startup() -> None:
    """Function to start the service"""
    # To disable urllib3 warnings
    os.environ["PYTHONWARNINGS"] = "ignore:Unverified HTTPS request"
    LOG.info("CCP API server startup")
    global g_audit_service
    g_audit_service = AuditService()
    await g_audit_service.create_audit_collection()


async def on_shutdown() -> None:
    LOG.info("CCP API server stop")


headers = {
    "access-control-allow-methods": "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
    "access-control-max-age": "600",
    "access-control-allow-credentials": "true",
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "content-type"
}


def get_response_content(exc):
    return {
        "code": exc.status_code,
        "message": exc.message,
        "detail": exc.details
    }


async def global_exception_handler_middleware(request: Request, call_next):
    """Global exception handler middleware to handle all exceptions"""

    try:
        response = await call_next(request)
    except CCPIAMException as e:
        e.print()
        return JSONResponse(content={"detail": e.message}, headers=headers, status_code=e.status_code)
    except CCPBusinessException as e:
        e.print()
        return JSONResponse(content={"detail": e.message}, headers=headers, status_code=e.status_code)
    except CCPAuthException as e:
        e.print()
        return JSONResponse(content={"detail": e.message}, headers=headers, status_code=e.status_code)
    except CCPCloudException as e:
        e.print()
        return JSONResponse(content=get_response_content(e), headers=headers, status_code=e.status_code)
    except Exception:
        traceback.print_exc()
        content = {"detail": f"Something went wrong! Please try after sometime."}
        return JSONResponse(content=content, headers=headers, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response


app = FastAPI(
    title="CCP APIs",
    openapi_url=f'{BASE_PATH}/openapi.json',
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    debug=True)
app.include_router(api_router, prefix=BASE_PATH,
                   dependencies=[Depends(auth.authenticate)])
app.include_router(base_router, prefix=BASE_PATH,
                   dependencies=[Depends(auth.authenticate)])
app.include_router(org_admin_api_router, prefix=BASE_PATH,
                   dependencies=[Depends(auth.authenticate)])
app.add_api_route("/health", health([health_check]),
                  tags=["Actuator"], description="Health check")
app.include_router(oidc_router, prefix=BASE_PATH + '/auth')
app.include_router(org_api_router, prefix=BASE_PATH,
                   dependencies=[Depends(auth.authenticate)])
app.include_router(public_router, prefix=BASE_PATH, )

# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Global exception handler for handling 'Internal Server Errors' exception
app.middleware('http')(global_exception_handler_middleware)


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    start_time = time.time()

    project_id = Utils.extract_id_from_path(request.url.path, 'projects')

    # Set values in ccp_context
    ccp_context.set_request_data(Constants.CURRENT_REQUEST, request)
    ccp_context.set_request_data(Constants.CCPHeader.CLOUD_ID, request.headers.get(
        Constants.CCPHeader.CLOUD_ID, None))
    ccp_context.set_request_data(Constants.CCPHeader.ORG_ID, request.headers.get(
        Constants.CCPHeader.ORG_ID, None))
    ccp_context.set_request_data(Constants.CCPHeader.PROJECT_ID, project_id)
    request.state.__setattr__(Constants.CCPHeader.PROJECT_ID, project_id)

    # Configure request_id and set in ccp_context
    request_id = Utils.generate_unique_str()
    ccp_context.set_request_data(Constants.CCPHeader.AUDIT_ID, request_id)

    log = logger.configure_logger()

    log.debug(f"Entering into {request.method} {request.url}")
    response = None
    status_code = None
    process_time = 0
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Audit-ID"] = request_id
        status_code = response.status_code
    finally:
        log.debug(f"Exiting from {request.method} {request.url}")

        # Set status code to 500 if no status code if found
        status_code = status_code if status_code else status.HTTP_500_INTERNAL_SERVER_ERROR

        await g_audit_service.write_audit_log(request, status_code, request_id, start_time, process_time)

        # Clear the Context
        ccp_context.clear_context()
    return response


@app.get("/info", tags=['Actuator'], description="CCP API info")
def get_info():
    """Function to get info about the service"""
    repo = Repo(search_parent_directories=True)
    commit = repo.head.commit

    return {
        "git": {
            "branch": repo.active_branch.name,
            "commit_message": commit.message,
            "author": str(commit.author),
            "committed_date": str(commit.committed_datetime),
        }
    }
