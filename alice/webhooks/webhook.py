import json
from typing import Optional


class Webhook:
    @staticmethod
    def from_dict(kdict: dict):
        return Webhook(
            webhook_id=kdict.get("webhook_id"),
            active=kdict.get("active"),
            post_url=kdict.get("post_url"),
            api_key=kdict.get("api_key"),
            secret=kdict.get("secret"),
            algorithm=kdict.get("algorithm"),
            event_name=kdict.get("event_name"),
            event_version=kdict.get("event_version"),
        )

    def to_dict(self):
        kdict = {
            "active": self.active,
            "post_url": self.post_url,
            "api_key": self.api_key,
            "secret": self.secret,
            "event_name": self.event_name,
            "event_version": self.event_version,
        }
        if self.webhook_id:
            kdict["webhook_id"] = self.webhook_id

        if self.algorithm:
            kdict["algorithm"] = self.algorithm

        return kdict

    def __init__(
        self,
        active: bool,
        post_url: str,
        api_key: str,
        secret: str,
        event_name: str,
        event_version: Optional[str] = "1",
        webhook_id: str = None,
        algorithm: str = None,
    ):
        self.webhook_id = webhook_id
        self.active = active
        self.post_url = post_url
        self.api_key = api_key
        self.secret = secret
        self.algorithm = algorithm
        self.event_name = event_name
        self.event_version = event_version
        super().__init__()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__) or issubclass(
            self.__class__, other.__class__
        ):
            return self.to_dict() == other.to_dict()
        else:
            return False
