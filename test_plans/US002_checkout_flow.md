# US002 — Checkout flow

## User Story
As a customer, I want to go through the checkout process
so that I can provide my delivery address and confirm my order.

## Acceptance criteria
- Customer can proceed to checkout from a non-empty cart
- Customer must fill in street, city, and zip code
- Guest checkout must be available (no account required)
- Order is created with PENDING status on submission
- Empty cart cannot be checked out

## Test cases

| ID    | Scenario                          | Expected result              | Priority | Automated       |
|-------|-----------------------------------|------------------------------|----------|-----------------|
| TC009 | Create order from valid cart      | 201, status = PENDING        | HIGH     | ✅ unit + api   |
| TC010 | Create order from empty cart      | OrderError / 422             | HIGH     | ✅ unit + api   |
| TC011 | Order total matches cart total    | order.total == cart.total()  | HIGH     | ✅ unit + api   |
| TC012 | Cancel order changes status       | status = CANCELLED           | HIGH     | ✅ unit + api   |
| TC013 | GET /orders/{id} returns details  | 200, correct total           | HIGH     | ✅ api (test_orders_api.py) |
| TC014 | GET nonexistent order → 404       | 404                          | MEDIUM   | ✅ api          |
| TC015 | Complete checkout journey (E2E)   | Confirmation page visible    | HIGH     | ✅ e2e (test_checkout_flow.py) |
| TC016 | Guest checkout option visible     | Element present on page      | HIGH     | ✅ e2e          |

## Edge cases and boundary values
- Order from cart with only one item → valid
- Double cancellation → second cancel raises OrderError
- Confirm already-confirmed order → raises OrderError

## Out of scope
- Address validation (postal code format, country)
- Delivery date estimation
- Multi-address / split shipping
