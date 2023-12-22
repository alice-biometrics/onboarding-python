import json
from typing import Any, Dict, Union

from meiga import Error
from pydantic import BaseModel, Field
from requests import Response
from requests_toolbelt import MultipartDecoder


class BoundingBox(BaseModel):
    x: Union[int, float] = Field(ge=0)
    y: Union[int, float] = Field(ge=0)
    width: Union[int, float] = Field(gt=0)
    height: Union[int, float] = Field(gt=0)
    aspect_ratio: Union[float, None] = None
    rotation_angle: Union[float, None] = None


def liveness_response(response_encoded: bytes) -> Union[float, None]:
    if response_encoded == b"":
        return None
    pad_score = float(response_encoded.decode())
    return pad_score


def metadata_response(response_encoded: bytes) -> Union[Dict[str, Any], None]:
    if response_encoded == b"":
        return None
    return json.loads(response_encoded.decode())  # type: ignore


def bytes_response(response_encoded: bytes) -> Union[bytes, None]:
    if response_encoded == b"":
        return None
    return response_encoded


def face_bounding_box_response(response_encoded: bytes) -> BoundingBox:
    face_bounding_box = json.loads(response_encoded.decode())
    return BoundingBox(
        x=face_bounding_box["x"],
        y=face_bounding_box["y"],
        width=face_bounding_box["x2"] - face_bounding_box["x"],
        height=face_bounding_box["y2"] - face_bounding_box["y"],
    )


def number_of_faces_response(response_encoded: bytes) -> int:
    number_of_faces = int(response_encoded.decode())
    return number_of_faces


response_factory = {
    "liveness_score": liveness_response,
    "metadata": metadata_response,
    "face_avatar": bytes_response,
    "face_selfie": bytes_response,
    "face_profile": bytes_response,
    "face_bounding_box": face_bounding_box_response,
    "number_of_faces": number_of_faces_response,
}


def decode_multipart_response(response: Response) -> Dict[str, Any]:
    decoder = MultipartDecoder.from_response(response)
    response_dict = {}
    for part in decoder.parts:
        header_name = part.headers._store.get(b"content-disposition")[1].decode()
        header_name_part = header_name.split(";")[1]
        separation_idx = header_name_part.index("=")
        field_name = header_name_part[separation_idx + 2 : -1]  # noqa
        if field_name in response_factory:
            response_dict[field_name] = response_factory[field_name](part.content)

    return response_dict


class SelfieResult(BaseModel):
    face_profile: Union[bytes, None] = Field(
        None,
        description="Binary with the face profile extracted from given media.",
        examples=[b"binary data"],
    )
    liveness_score: Union[float, None] = Field(
        None,
        description="Liveness score to determine the input as a genuine attempt (>=50) or attack (<50).",
        ge=0.0,
        le=100.0,
        examples=[90],
    )
    number_of_faces: Union[int, None] = Field(
        None, description="Number of faces detected.", examples=[1]
    )
    metadata: Union[Dict[str, Any], None] = Field(
        None, description="Dictionary with some optional metadata"
    )

    def __repr__(self) -> str:
        face_profile = (
            f"face_profile(length)={len(self.face_profile)}"
            if self.face_profile
            else "face_profile=None"
        )
        return f"[SelfieResult {face_profile} liveness_score={self.liveness_score} number_of_faces={self.number_of_faces} metadata={self.metadata}]"

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def from_response(response: Response) -> "SelfieResult":
        multipart_response_dict = decode_multipart_response(response)
        face_profile = multipart_response_dict.get("face_profile")
        liveness_score = multipart_response_dict.get("liveness_score")
        number_of_faces = multipart_response_dict.get("number_of_faces")
        metadata = multipart_response_dict.get("metadata")

        return SelfieResult(
            face_profile=face_profile,
            liveness_score=liveness_score,
            number_of_faces=number_of_faces,
            metadata=metadata,
        )

    def save_face_profile(self, filename: str) -> None:
        if self.face_profile is None:
            raise FileNotFoundError("Retrieved face profile is none")
        with open(filename, "wb") as file:
            file.write(self.face_profile)


class DocumentResult(BaseModel):
    face_profile: Union[bytes, None] = Field(
        None,
        description="Binary with the face profile extracted from given image.",
        examples=[b"binary data"],
    )

    @staticmethod
    def from_response(response: Response) -> "DocumentResult":
        multipart_response_dict = decode_multipart_response(response)
        face_profile = multipart_response_dict.get("face_profile")
        # face_bounding_box = multipart_response_dict.get("face_bounding_box") # TODO REVIEW
        return DocumentResult(face_profile=face_profile)

    def save_face_profile(self, filename: str) -> None:
        if self.face_profile is None:
            raise FileNotFoundError("Retrieved face profile is none")
        with open(filename, "wb") as file:
            file.write(self.face_profile)


class MatchResult(BaseModel):
    score: Union[float, None] = Field(
        None,
        description="Matching score to determine the input as a genuine attempt (>=50) or attack (<50).",
        ge=0.0,
        le=100.0,
        examples=[90],
    )


class FaceError(Error):
    def __init__(self, message: str, status_code: int, url: str):
        self.message = message
        self.status_code = status_code
        self.url = url

    @staticmethod
    def from_response(response: Response) -> "FaceError":
        return FaceError(
            message=str(response.content),
            status_code=response.status_code,
            url=response.url,
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {self.status_code} {self.message} | {self.url}"
        )
