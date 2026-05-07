# BUG002 — Creating an order from an empty cart returns 500

## Severity: CRITICAL
## Status: FIXED
## Environment: Python 3.11, FastAPI 0.115, API v1.0.0

## Steps to reproduce
1. Create a new cart via `POST /cart`
2. Do NOT add any items
3. Submit `POST /orders` with the empty cart id

## Expected behavior
```
HTTP 422 Unprocessable Entity
{"detail": "Cannot create an order from an empty cart."}
```

## Observed behavior
```
HTTP 500 Internal Server Error
(unhandled exception — OrderError propagated to the framework)
```

## Log excerpt
```
ERROR: Exception in ASGI application
app.domain.order.OrderError: Cannot create an order from an empty cart.
File "app/main.py", line 94, in create_order
    order = Order.from_cart(cart)
```

## Root cause hypothesis
`Order.from_cart()` raises `OrderError` for an empty cart, but the
`POST /orders` endpoint did not catch this exception, causing FastAPI
to return an unhandled 500.

## Fix applied
Added a `try/except OrderError` block in `create_order()` that
converts the domain exception to an `HTTPException(422)`:

```python
try:
    order = Order.from_cart(cart)
except OrderError as exc:
    raise HTTPException(status_code=422, detail=str(exc))
```

## Linked test
`tests/api/test_orders_api.py::TestOrdersAPI::test_create_order_with_empty_cart_returns_422`
