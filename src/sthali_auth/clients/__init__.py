from typing import Any

from httpx import post


class ServiceClient:
    def __init__(self) -> None:
        self.url = "http://localhost:8002/authorize"

    def call(self, headers: dict[str, Any], json: dict[str, Any]) -> None:
        post(self.url, headers=headers, json=json)
