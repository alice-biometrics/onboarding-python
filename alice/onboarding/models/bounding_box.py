from pydantic import Field
from pydantic.main import BaseModel


class BoundingBox(BaseModel):
    """
    A bounding box is the smallest rectangle with vertical and horizontal sides that completely surrounds an object
    """

    x: int = Field(description="Top left corner x coordinate")
    y: int = Field(description="Top left corner y coordinate")
    width: int = Field(description="Rectangle width")
    height: int = Field(description="Rectangle height")
