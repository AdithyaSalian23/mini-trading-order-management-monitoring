import logging
import uuid

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order, User
from app.schemas import OrderCreate, OrderResponse, OrderStatusUpdate


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Mini Trading Order Management API",
    description="Practice API for trading order management and application support",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    logger.info("Health check requested")

    return {
        "status": "UP",
        "service": "Trading Order API"
    }


@app.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    logger.info(
        "Create order request received for user_id=%s, symbol=%s",
        order.user_id,
        order.symbol
    )

    # Check whether the user exists
    user = (
        db.query(User)
        .filter(User.user_id == order.user_id)
        .first()
    )

    if not user:
        logger.warning(
            "Order creation failed: user_id=%s not found",
            order.user_id
        )

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Generate a unique order ID
    order_id = f"ORD{uuid.uuid4().hex[:8].upper()}"

    new_order = Order(
        order_id=order_id,
        user_id=order.user_id,
        symbol=order.symbol.upper(),
        quantity=order.quantity,
        side=order.side,
        order_type=order.order_type,
        price=order.price,
        status="PENDING"
    )

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        logger.info(
            "Order created successfully: order_id=%s",
            order_id
        )

        return new_order

    except IntegrityError:
        db.rollback()

        logger.error(
            "Database integrity error while creating order"
        )

        raise HTTPException(
            status_code=409,
            detail="Order could not be created due to a data conflict"
        )

    except SQLAlchemyError:
        db.rollback()

        logger.exception(
            "Database error while creating order"
        )

        raise HTTPException(
            status_code=500,
            detail="Database error occurred while creating order"
        )


@app.get(
    "/orders/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    logger.info(
        "Get order request received: order_id=%s",
        order_id
    )

    order = (
        db.query(Order)
        .filter(Order.order_id == order_id)
        .first()
    )

    if not order:
        logger.warning(
            "Order not found: order_id=%s",
            order_id
        )

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    logger.info(
        "Order retrieved successfully: order_id=%s",
        order_id
    )

    return order

@app.get(
    "/users/{user_id}/orders",
    response_model=list[OrderResponse]
)
def get_user_orders(
    user_id: int,
    db: Session = Depends(get_db)
):
    logger.info(
        "Get orders request received for user_id=%s",
        user_id
    )

    # Check whether the user exists
    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if not user:
        logger.warning(
            "User not found: user_id=%s",
            user_id
        )

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    orders = (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .all()
    )

    logger.info(
        "Retrieved %s orders for user_id=%s",
        len(orders),
        user_id
    )

    return orders

@app.put("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    logger.info(
        "Update order status request received: order_id=%s, new_status=%s",
        order_id,
        status_update.status
    )

    order = (
        db.query(Order)
        .filter(Order.order_id == order_id)
        .first()
    )

    if not order:
        logger.warning(
            "Order not found for status update: order_id=%s",
            order_id
        )
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    old_status = order.status
    order.status = status_update.status

    try:
        db.commit()
        db.refresh(order)

        logger.info(
            "Order status updated: order_id=%s, old_status=%s, new_status=%s",
            order_id,
            old_status,
            order.status
        )

        return order

    except SQLAlchemyError:
        db.rollback()

        logger.exception(
            "Database error while updating order status: order_id=%s",
            order_id
        )

        raise HTTPException(
            status_code=500,
            detail="Database error occurred while updating order status"
        )