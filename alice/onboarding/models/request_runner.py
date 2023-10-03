from dataclasses import dataclass
from typing import Any, Dict, Union

from requests import Response, Session


@dataclass
class RequestRunner:
    session: Session
    headers: Dict[str, Any]
    base_url: str
    timeout: Union[float, None] = None

    def get_with(self, url_path: str) -> Response:
        return self.session.get(
            f"{self.base_url}/{url_path}", headers=self.headers, timeout=self.timeout
        )

    def post_with(
        self,
        url_path: str,
        json: Union[Dict[str, Any], None] = None,
        data: Union[Dict[str, Any], None] = None,
    ) -> Response:
        return self.session.post(
            f"{self.base_url}/{url_path}",
            json=json,
            data=data,
            headers=self.headers,
            timeout=self.timeout,
        )

    def patch_with(
        self, url_path: str, json: Union[Dict[str, Any], None] = None
    ) -> Response:
        return self.session.patch(
            f"{self.base_url}/{url_path}",
            json=json,
            headers=self.headers,
            timeout=self.timeout,
        )

    def put_with(
        self, url_path: str, json: Union[Dict[str, Any], None] = None
    ) -> Response:
        return self.session.put(
            f"{self.base_url}/{url_path}",
            json=json,
            headers=self.headers,
            timeout=self.timeout,
        )

    def delete_with(self, url_path: str) -> Response:
        return self.session.delete(
            f"{self.base_url}/{url_path}", headers=self.headers, timeout=self.timeout
        )
