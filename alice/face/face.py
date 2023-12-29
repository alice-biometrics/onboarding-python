from typing import Dict, Union

from meiga import Failure, Result, Success
from requests import Response, Session

from alice.config import Config
from alice.face.face_models import DocumentResult, FaceError, MatchResult, SelfieResult


class Face:
    @staticmethod
    def from_config(config: Config) -> "Face":
        if config.session:
            session = config.session
        else:
            session = Session()
        return Face(
            api_key=config.api_key,  # type: ignore
            url=config.face_url,  # type: ignore
            timeout=config.timeout,
            send_agent=config.send_agent,
            verbose=config.verbose,
            session=session,
        )

    def __init__(
        self,
        api_key: str,
        url: str,
        session: Session,
        timeout: Union[float, None] = None,
        send_agent: bool = True,
        verbose: bool = False,
    ):
        self.api_key = api_key
        self.url = url
        self.timeout = timeout
        self.send_agent = send_agent
        self.verbose = verbose
        self.session = session

    def healthcheck(self) -> Response:
        response = self.session.get(
            url=self.url + "/healthcheck", headers={"apikey": self.api_key}
        )
        return response

    def selfie(
        self,
        media: bytes,
        extract_liveness: bool = True,
        extract_face_profile: bool = True,
        headers: Union[Dict[str, str], None] = None,
    ) -> Result[SelfieResult, FaceError]:
        if headers is None:
            headers = {}

        response = self.session.post(
            url=f"{self.url}/selfie",
            headers={"apikey": self.api_key} | headers,
            files={"media": media},
            data={
                "extract_liveness": extract_liveness,
                "extract_face_profile": extract_face_profile,
            },
        )
        if response.status_code == 200:
            return Success(SelfieResult.from_response(response))
        else:
            return Failure(FaceError.from_response(response))

    def document(
        self,
        image: bytes,
        headers: Union[Dict[str, str], None] = None,
    ) -> Result[DocumentResult, FaceError]:
        if headers is None:
            headers = {}

        response = self.session.post(
            url=f"{self.url}/document",
            headers={"apikey": self.api_key} | headers,
            files={"image": image},
        )

        if response.status_code == 200:
            return Success(DocumentResult.from_response(response))
        else:
            return Failure(FaceError.from_response(response))

    def match_profiles(
        self,
        face_profile_probe: bytes,
        face_profile_target: bytes,
    ) -> Result[MatchResult, FaceError]:
        response = self.session.post(
            url=f"{self.url}/match/profiles",
            headers={"apikey": self.api_key},
            files={
                "face_profile_probe": face_profile_probe,
                "face_profile_target": face_profile_target,
            },
        )
        if response.status_code == 200:
            return Success(MatchResult(score=response.json().get("match_score")))
        else:
            return Failure(FaceError.from_response(response))

    def match_media(
        self, selfie_media: bytes, document_media: bytes
    ) -> Result[MatchResult, FaceError]:
        response = self.session.post(
            url=f"{self.url}/match/media",
            headers={"apikey": self.api_key},
            files={"selfie_media": selfie_media, "document_media": document_media},
        )
        if response.status_code == 200:
            return Success(MatchResult(score=response.json().get("match_score")))
        else:
            return Failure(FaceError.from_response(response))
