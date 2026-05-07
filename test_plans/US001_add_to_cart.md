# US001 — Add product to cart

## User Story
As a customer, I want to add products to my cart
so that I can purchase multiple items at once.

## Acceptance criteria
- Customer can add an available product to the cart
- Quantity increases if the same product is added again
- Total recalculates automatically after each add
- Out-of-stock products cannot be added
- Cart total is zero on a new, empty cart

## Test cases

| ID    | Scenario                          | Expected result              | Priority | Automated       |
|-------|-----------------------------------|------------------------------|----------|-----------------|
| TC001 | Add 1 available product           | Cart contains 1 item, total > 0 | HIGH  | ✅ unit (test_cart.py) |
| TC002 | Add same product twice            | Total = price × 2            | HIGH     | ✅ unit (test_cart.py) |
| TC003 | Add out-of-stock product          | OutOfStockError / 409        | HIGH     | ✅ unit + api   |
| TC004 | Add item via API                  | 201, total updated           | HIGH     | ✅ api (test_cart_api.py) |
| TC005 | New empty cart total              | total = 0.0                  | MEDIUM   | ✅ unit (test_cart.py) |
| TC006 | is_empty() on new cart            | True                         | MEDIUM   | ✅ unit (test_cart.py) |
| TC007 | Add item via UI button            | Item visible, total > 0      | HIGH     | ✅ e2e (test_cart_interactions.py) |
| TC008 | GET /cart returns correct total   | total matches added items    | HIGH     | ✅ api (test_cart_api.py) |

## Edge cases and boundary values
- Stock exactly 0 → blocked
- Stock exactly 1 → allowed
- Price = 0.00 → allowed (free item)
- Very large price (> €10 000) → total must stay accurate (Decimal arithmetic)

## Out of scope
- Cart persistence across sessions (no database in this version)
- Multi-user concurrent cart access
- Item image or description validation
