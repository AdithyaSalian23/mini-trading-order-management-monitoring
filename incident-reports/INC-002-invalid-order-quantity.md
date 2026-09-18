# INC-002 — Invalid Order Quantity

## Incident Type
API Validation Issue

## Summary
An order creation request was submitted with an invalid negative quantity.

## Endpoint
POST /orders

## Request
{
    "user_id": 2,
    "symbol": "INFY",
    "quantity": -5,
    "side": "BUY",
    "order_type": "LIMIT",
    "price": 1500
}

## Observed Result
HTTP 422 Unprocessable Content

## Investigation
1. Reproduced the issue using Postman.
2. Reviewed the request payload.
3. Identified that the quantity was set to -5.
4. Reviewed the API validation rules.
5. Confirmed that quantity must be greater than 0.

## Root Cause
Invalid input data was submitted. The order quantity was negative.

## Resolution
No application fix was required. The API correctly rejected the invalid request through input validation.

## Validation
The negative quantity request returned HTTP 422 as expected.

## Status
Closed