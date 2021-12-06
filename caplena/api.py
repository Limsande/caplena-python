from enum import Enum
from typing import Any, Dict, Optional, Union

from caplena.helpers import Helpers
from caplena.http.http_client import HttpClient, HttpMethod, HttpRetry
from caplena.logging.logger import Logger


class ApiBaseUri(Enum):
    LOCAL = "http://localhost:8000/v2"
    PRODUCTION = "https://api.caplena.com/v2"

    @property
    def url(self) -> str:
        return self.value


class ApiVersion(Enum):
    DEFAULT = 0
    VER_2021_12_01 = 1

    @property
    def version(self) -> str:
        if self.name != ApiVersion.DEFAULT.name:
            return self.name.replace("VER_", "").replace("_", "-")
        else:
            raise ValueError(f"Cannot convert `{self.name}` to a valid version string.")


class ApiRequestor:
    def __init__(
        self,
        *,
        http_client: HttpClient,
        logger: Logger,
    ):
        self._http_client = http_client
        self._logger = logger

    def build_uri(
        self,
        *,
        base_uri: Union[str, ApiBaseUri],
        path: str,
        path_params: Optional[Dict[str, str]] = None,
        query_params: Optional[Dict[str, str]] = None,
    ) -> str:
        path_params = path_params if path_params is not None else {}
        query_params = query_params if query_params is not None else {}
        if isinstance(base_uri, ApiBaseUri):
            base_uri = base_uri.url

        absolute_uri = Helpers.append_path(base_uri=base_uri, path=path)
        return Helpers.build_qualified_uri(
            absolute_uri,
            path_params=path_params,
            query_params=query_params,
        )

    def build_request_headers(
        self,
        *,
        headers: Optional[Dict[str, str]] = None,
        api_version: ApiVersion = ApiVersion.DEFAULT,
        api_key: Optional[str] = None,
    ) -> Dict[str, str]:
        headers = {} if headers is None else headers.copy()
        headers.setdefault("Accept", "application/json")

        # note: we do not allow clients to overwrite user-agent, caplena-api-key or caplena-api-version
        headers["User-Agent"] = Helpers.get_user_agent(identifier=self._http_client.identifier)
        if api_key is not None:
            headers["Caplena-API-Key"] = api_key
        if api_version != ApiVersion.DEFAULT:
            headers["Caplena-API-Version"] = api_version.version

        return headers

    def request_raw(
        self,
        base_uri: Union[str, ApiBaseUri],
        path: str,
        *,
        method: HttpMethod = HttpMethod.GET,
        api_version: ApiVersion = ApiVersion.DEFAULT,
        api_key: Optional[str] = None,
        path_params: Optional[Dict[str, str]] = None,
        query_params: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        retry: Optional[HttpRetry] = None,
    ):
        absolute_uri = self.build_uri(
            base_uri=base_uri,
            path=path,
            path_params=path_params,
            query_params=query_params,
        )
        headers = self.build_request_headers(
            headers=headers,
            api_version=api_version,
            api_key=api_key,
        )

        return self._http_client.request(
            uri=absolute_uri,
            method=method,
            headers=headers,
            json=json,
            timeout=timeout,
            retry=retry,
        )

    def get(
        self,
        base_uri: Union[str, ApiBaseUri],
        path: str,
        *,
        api_version: ApiVersion = ApiVersion.DEFAULT,
        api_key: Optional[str] = None,
        path_params: Optional[Dict[str, str]] = None,
        query_params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        retry: Optional[HttpRetry] = None,
    ):
        return self.request_raw(
            base_uri=base_uri,
            path=path,
            method=HttpMethod.GET,
            api_version=api_version,
            api_key=api_key,
            path_params=path_params,
            query_params=query_params,
            json=None,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )

    def post(
        self,
        base_uri: Union[str, ApiBaseUri],
        path: str,
        *,
        api_version: ApiVersion = ApiVersion.DEFAULT,
        api_key: Optional[str] = None,
        path_params: Optional[Dict[str, str]] = None,
        query_params: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        retry: Optional[HttpRetry] = None,
    ):
        return self.request_raw(
            base_uri=base_uri,
            path=path,
            method=HttpMethod.POST,
            api_version=api_version,
            api_key=api_key,
            path_params=path_params,
            query_params=query_params,
            json=json,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )

    def put(
        self,
        base_uri: Union[str, ApiBaseUri],
        path: str,
        *,
        api_version: ApiVersion = ApiVersion.DEFAULT,
        api_key: Optional[str] = None,
        path_params: Optional[Dict[str, str]] = None,
        query_params: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        retry: Optional[HttpRetry] = None,
    ):
        return self.request_raw(
            base_uri=base_uri,
            path=path,
            method=HttpMethod.PUT,
            api_version=api_version,
            api_key=api_key,
            path_params=path_params,
            query_params=query_params,
            json=json,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )

    def patch(
        self,
        base_uri: Union[str, ApiBaseUri],
        path: str,
        *,
        api_version: ApiVersion = ApiVersion.DEFAULT,
        api_key: Optional[str] = None,
        path_params: Optional[Dict[str, str]] = None,
        query_params: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        retry: Optional[HttpRetry] = None,
    ):
        return self.request_raw(
            base_uri=base_uri,
            path=path,
            method=HttpMethod.PATCH,
            api_version=api_version,
            api_key=api_key,
            path_params=path_params,
            query_params=query_params,
            json=json,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )

    def delete(
        self,
        base_uri: Union[str, ApiBaseUri],
        path: str,
        *,
        api_version: ApiVersion = ApiVersion.DEFAULT,
        api_key: Optional[str] = None,
        path_params: Optional[Dict[str, str]] = None,
        query_params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        retry: Optional[HttpRetry] = None,
    ):
        return self.request_raw(
            base_uri=base_uri,
            path=path,
            method=HttpMethod.DELETE,
            api_version=api_version,
            api_key=api_key,
            path_params=path_params,
            query_params=query_params,
            json=None,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )
