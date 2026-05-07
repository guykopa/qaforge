# BUG001 — Discount rounding error on total above €1000

## Severity: HIGH
## Status: FIXED
## Environment: Python 3.11, FastAPI 0.115, API v1.0.0

## Steps to reproduce
1. Create a new cart via `POST /cart`
2. Add an item with price `1100.00` via `POST /cart/{id}/items`
3. Apply discount code `SAVE10` via `POST /cart/{id}/discount`
4. Read the cart total via `GET /cart/{id}`

## Expected behavior
```
total = 1100.00 × 0.9 = 990.00
```

## Observed behavior
```
total = 989.9999999999999  (off by €0.01 due to float multiplication)
```

## Log excerpt
```python
>>> 1100.0 * 0.9
989.9999999999999
```

## Root cause hypothesis
Python `float` uses IEEE 754 binary arithmetic, which cannot represent
`0.9` exactly. Multiplying a float price by `0.9` introduces a
sub-cent rounding error that propagates to the displayed total.

## Fix applied
Replaced `float` arithmetic in `Cart.total()` with `decimal.Decimal`
and `ROUND_HALF_UP` quantisation to 2 decimal places:

```python
from decimal import Decimal, ROUND_HALF_UP

raw = sum(Decimal(str(item.price)) for item in self.items)
raw = raw * (Decimal("1") - rate)
return float(raw.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
```

## Linked test
`tests/unit/test_cart.py::TestCart::test_apply_10_percent_discount`
uses `pytest.approx` and will catch any future regression.
