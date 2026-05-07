# US003 — Payment processing

## User Story
As a customer, I want to pay for my order with a credit card
so that my purchase is confirmed and I receive an order number.

## Acceptance criteria
- A valid card produces a SUCCESS payment and CONFIRMED order
- A declined card produces a DECLINED payment (order stays PENDING)
- A cancelled order cannot be paid
- A successful payment can be refunded
- A non-successful payment cannot be refunded

## Test cases

| ID    | Scenario                              | Expected result                  | Priority | Automated       |
|-------|---------------------------------------|----------------------------------|----------|-----------------|
| TC017 | Valid card → SUCCESS                  | status = SUCCESS                 | HIGH     | ✅ unit + api   |
| TC018 | Declined card → DECLINED              | status = DECLINED                | HIGH     | ✅ unit + api   |
| TC019 | Valid payment confirms order          | order.status = CONFIRMED         | HIGH     | ✅ unit         |
| TC020 | Refund SUCCESS payment → REFUNDED     | status = REFUNDED                | HIGH     | ✅ unit + api   |
| TC021 | Refund DECLINED payment → error       | PaymentError / 422               | HIGH     | ✅ unit         |
| TC022 | Pay cancelled order → error           | PaymentError / 422               | HIGH     | ✅ unit + api   |
| TC023 | GET /payment/{id} returns amount      | amount = order.total             | HIGH     | ✅ api          |
| TC024 | GET nonexistent payment → 404         | 404                              | MEDIUM   | ✅ api          |
| TC025 | E2E: successful payment shows order # | order-number element visible     | HIGH     | ✅ e2e          |
| TC026 | E2E: declined card shows error        | order-error element visible      | HIGH     | ✅ e2e          |

## Edge cases and boundary values
- Card number exactly 16 digits → accepted
- Expired card (4000000000000069) → treated as declined
- Payment amount matches discounted total when discount applied

## Out of scope
- 3-D Secure / two-factor payment authentication
- Multiple payment methods (PayPal, Apple Pay)
- Partial refunds
- Currency conversion
