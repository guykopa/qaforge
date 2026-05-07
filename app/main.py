from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.domain.cart import Cart, DiscountError, Item, ItemNotFoundError, OutOfStockError
from app.domain.order import Order, OrderError
from app.domain.payment import Payment, PaymentError

app = FastAPI(title="qaforge e-commerce API")
templates = Jinja2Templates(directory="app/templates")

# In-memory stores (stateless per test client instance)
_carts: dict[str, Cart] = {}
_orders: dict[str, Order] = {}
_payments: dict[str, Payment] = {}


# ── Request / Response schemas ────────────────────────────────────────────────

class ItemIn(BaseModel):
    """Request body for adding an item to a cart."""

    id: str
    name: str
    price: float
    stock: int


class DiscountIn(BaseModel):
    """Request body for applying a discount code."""

    code: str


class OrderIn(BaseModel):
    """Request body for creating an order."""

    cart_id: str


class PaymentIn(BaseModel):
    """Request body for processing a payment."""

    order_id: str
    card_number: str


# ── Cart endpoints ────────────────────────────────────────────────────────────

@app.post("/cart", status_code=201)
def create_cart() -> dict:
    """Create a new empty cart and return its id."""
    cart = Cart()
    _carts[cart.id] = cart
    return {"id": cart.id}


@app.get("/cart/{cart_id}")
def get_cart(cart_id: str) -> dict:
    """Return cart contents and current total."""
    cart = _get_cart(cart_id)
    return {
        "id": cart.id,
        "items": [
            {"id": i.id, "name": i.name, "price": i.price, "stock": i.stock}
            for i in cart.items
        ],
        "discount_code": cart.discount_code,
        "total": cart.total(),
    }


@app.post("/cart/{cart_id}/items", status_code=201)
def add_item(cart_id: str, body: ItemIn) -> dict:
    """Add an item to the cart."""
    cart = _get_cart(cart_id)
    item = Item(id=body.id, name=body.name, price=body.price, stock=body.stock)
    try:
        cart.add_item(item)
    except OutOfStockError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return {"id": cart.id, "total": cart.total()}


@app.delete("/cart/{cart_id}/items/{item_id}", status_code=200)
def remove_item(cart_id: str, item_id: str) -> dict:
    """Remove an item from the cart."""
    cart = _get_cart(cart_id)
    try:
        cart.remove_item(item_id)
    except ItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"id": cart.id, "total": cart.total()}


@app.post("/cart/{cart_id}/discount", status_code=200)
def apply_discount(cart_id: str, body: DiscountIn) -> dict:
    """Apply a discount code to the cart."""
    cart = _get_cart(cart_id)
    try:
        cart.apply_discount(body.code)
    except DiscountError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"id": cart.id, "discount_code": cart.discount_code, "total": cart.total()}


# ── Order endpoints ───────────────────────────────────────────────────────────

@app.post("/orders", status_code=201)
def create_order(body: OrderIn) -> dict:
    """Create an order from a cart."""
    cart = _get_cart(body.cart_id)
    try:
        order = Order.from_cart(cart)
    except OrderError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    _orders[order.id] = order
    return _order_dict(order)


@app.get("/orders/{order_id}")
def get_order(order_id: str) -> dict:
    """Return order details."""
    order = _get_order(order_id)
    return _order_dict(order)


@app.delete("/orders/{order_id}", status_code=200)
def cancel_order(order_id: str) -> dict:
    """Cancel an order."""
    order = _get_order(order_id)
    try:
        order.cancel()
    except OrderError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return _order_dict(order)


# ── Payment endpoints ─────────────────────────────────────────────────────────

@app.post("/payment", status_code=201)
def process_payment(body: PaymentIn) -> dict:
    """Process a payment for an order."""
    order = _get_order(body.order_id)
    try:
        payment = Payment.process(order, body.card_number)
    except PaymentError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    _payments[payment.id] = payment
    return _payment_dict(payment)


@app.get("/payment/{payment_id}")
def get_payment(payment_id: str) -> dict:
    """Return payment details."""
    payment = _get_payment(payment_id)
    return _payment_dict(payment)


@app.post("/payment/{payment_id}/refund", status_code=200)
def refund_payment(payment_id: str) -> dict:
    """Refund a successful payment."""
    payment = _get_payment(payment_id)
    try:
        payment.refund()
    except PaymentError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return _payment_dict(payment)


# ── HTML pages ───────────────────────────────────────────────────────────────

@app.get("/products", response_class=HTMLResponse)
def products_page(request: Request) -> HTMLResponse:
    """Products listing page."""
    return templates.TemplateResponse("products.html", {"request": request})


@app.get("/cart-page/{cart_id}", response_class=HTMLResponse)
def cart_page(request: Request, cart_id: str) -> HTMLResponse:
    """Shopping cart page."""
    cart = _carts.get(cart_id)
    if cart is None:
        from fastapi.responses import RedirectResponse
        return RedirectResponse("/products")
    return templates.TemplateResponse("cart_page.html", {
        "request": request,
        "cart": cart,
        "cart_total": cart.total(),
    })


@app.get("/checkout-page/{cart_id}", response_class=HTMLResponse)
def checkout_page(request: Request, cart_id: str) -> HTMLResponse:
    """Checkout page."""
    return templates.TemplateResponse("checkout_page.html", {
        "request": request,
        "cart_id": cart_id,
    })


@app.get("/confirmation-page", response_class=HTMLResponse)
def confirmation_page(
    request: Request,
    success: str = "true",
    order_id: str = "",
    payment_id: str = "",
) -> HTMLResponse:
    """Order confirmation page."""
    return templates.TemplateResponse("confirmation_page.html", {
        "request": request,
        "success": success == "true",
        "order_id": order_id,
        "payment_id": payment_id,
    })


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_cart(cart_id: str) -> Cart:
    """Retrieve a cart or raise 404."""
    cart = _carts.get(cart_id)
    if cart is None:
        raise HTTPException(status_code=404, detail=f"Cart '{cart_id}' not found.")
    return cart


def _get_order(order_id: str) -> Order:
    """Retrieve an order or raise 404."""
    order = _orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")
    return order


def _get_payment(payment_id: str) -> Payment:
    """Retrieve a payment or raise 404."""
    payment = _payments.get(payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail=f"Payment '{payment_id}' not found.")
    return payment


def _order_dict(order: Order) -> dict:
    """Serialize an Order to a dict."""
    return {
        "id": order.id,
        "cart_id": order.cart_id,
        "status": order.status.value,
        "total": order.total,
        "created_at": order.created_at.isoformat(),
    }


def _payment_dict(payment: Payment) -> dict:
    """Serialize a Payment to a dict."""
    return {
        "id": payment.id,
        "order_id": payment.order_id,
        "amount": payment.amount,
        "status": payment.status.value,
        "card_last4": payment.card_last4,
    }
