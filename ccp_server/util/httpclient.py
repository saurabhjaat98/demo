import types
from typing import Any
from typing import Dict
from typing import Optional

import httpx
from fastapi import HTTPException
from fastapi import status
from httpx import codes
from httpx import Response


class HttpClient:
    """HTTP client for interacting with the API"""

    def _http_request(
            method: types.FunctionType = httpx.Client.get,  # type: ignore
            **kwargs,
    ) -> Response:
        with httpx.Client(verify=False) as client:
            try:
                response = method(
                    client,
                    **kwargs,
                )
                return response
            except Exception as ex:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

    def assert_http_request(
            method: types.FunctionType,
            expected_status: codes = codes.OK,
            **kwargs,
    ) -> Response:
        response = HttpClient._http_request(method, **kwargs)
        if response.status_code != expected_status:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )
        return response

    def get_assert(
            url: str,
            cookies: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            expected_status: Optional[codes] = codes.OK
    ) -> Response:
        return HttpClient.assert_http_request(
            method=httpx.AsyncClient.get,  # type: ignore
            expected_status=expected_status,
            url=url,
            cookies=cookies,
            headers=headers,
            params=params,
        )

    def delete_assert(
            url: str,
            cookies: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            expectedStatus: Optional[codes] = codes.NO_CONTENT
    ) -> Response:
        return HttpClient.assert_http_request(
            method=httpx.AsyncClient.delete,  # type: ignore
            expected_status=expectedStatus,
            url=url,
            cookies=cookies,
            headers=headers,
        )

    def post_assert(
            url: str,
            json: Dict[str, Any],
            cookies: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            expected_status: Optional[codes] = codes.CREATED
    ) -> Response:
        return httpx.post(
            url=url,
            json=json,
            cookies=cookies,
            headers=headers,
            verify=False,
            expected_status=expected_status,
        )

    def put_assert(
            url: str,
            json: Optional[Dict[str, Any]] = None,
            cookies: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            expected_status: Optional[codes] = codes.OK
    ) -> Response:
        return HttpClient.assert_http_request(
            method=httpx.AsyncClient.put,  # type: ignore
            expected_status=expected_status,
            url=url,
            json=json,
            cookies=cookies,
            headers=headers,
        )
