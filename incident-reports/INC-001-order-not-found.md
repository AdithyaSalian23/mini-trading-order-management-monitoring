# INC-001 — Order Not Found

## Incident Type
Application/API Request Issue

## Summary
A request was made for an order ID that does not exist in the database.

## Endpoint
GET /orders/{order_id}

## Test Order ID
ORD99999

## Observed Result
HTTP 404 Not Found

Response:
{
  "detail": "Order not found"
}

## Investigation
1. Reproduced the issue using Postman.
2. Checked the `orders` table in MySQL.
3. Confirmed that `ORD99999` does not exist.
4. Reviewed the API logic handling missing orders.

## Root Cause
The requested order ID does not exist in the database.

## Resolution
No application fix was required. The API correctly returned HTTP 404 with a meaningful error message.

## Validation
The request was retested and the expected 404 response was received.

## Status
Closed