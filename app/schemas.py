from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class OrderCreate(BaseModel):
    user_id: int = Field(gt=0)
    symbol: str = Field(min_length=1, max_length=20)
    quantity: int = Field(gt=0)
    side: str
    order_type: str
    price: Decimal = Field(gt=0)

    @field_validator("side")
    @classmethod
    def validate_side(cls, value):
        value = value.upper()

        if value not in {"BUY", "SELL"}:
            raise ValueError("side must be BUY or SELL")

        return value

    @field_validator("order_type")
    @classmethod
    def validate_order_type(cls, value):
        value = value.upper()

        if value not in {"MARKET", "LIMIT"}:
            raise ValueError(
                "order_type must be MARKET or LIMIT"
            )

        return value


class OrderResponse(BaseModel):
    order_id: str
    user_id: int
    symbol: str
    quantity: int
    side: str
    order_type: str
    price: Decimal
    status: str

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        value = value.upper()

        if value not in {"PENDING", "EXECUTED", "CANCELLED"}:
            raise ValueError(
                "status must be PENDING, EXECUTED, or CANCELLED"
            )

        return value