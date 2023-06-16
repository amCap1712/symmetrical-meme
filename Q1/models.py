from typing import TypedDict


class PostOfficeT(TypedDict):
    Name: str
    Description: str | None
    BranchType: str
    DeliveryStatus: str
    Circle: str
    District: str
    Division: str
    Region: str
    Block: str
    State: str
    Country: str
    Pincode: str


class ResponseT(TypedDict):
    Message: str
    Status: str
    PostOffice: list[PostOfficeT] | None
