# INC-003 — Database Connection Failure

## Incident Type
Database Connectivity / Application Support

## Summary
The application returned HTTP 500 when attempting to retrieve an order because the configured database host was temporarily set to an invalid hostname.

## Endpoint
GET /orders/{order_id}

## Observed Result
HTTP 500 Internal Server Error

## Investigation
1. Reproduced the issue using the order retrieval endpoint.
2. Reviewed the application configuration.
3. Identified that `DB_HOST` was configured with an invalid hostname.
4. Confirmed that the application could not establish a connection to MySQL.
5. Restored the database host configuration to `localhost`.
6. Restarted the FastAPI application.
7. Retested the order retrieval endpoint.

## Root Cause
An incorrect database host configuration prevented the application from connecting to MySQL.

## Resolution
Restored the database host configuration to:

DB_HOST=localhost

The FastAPI application was restarted after correcting the configuration.

## Validation
The order retrieval request was retested successfully and returned HTTP 200 OK.

## Status
Closed