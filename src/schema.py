from pydantic import BaseModel


class PurchaseEventSchema(BaseModel):
    id: str
    price: float
    campaign: str
    source: str
    medium: str
