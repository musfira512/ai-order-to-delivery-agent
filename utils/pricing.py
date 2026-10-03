from data.menu import MENU


DELIVERY_FEES = {
    "Johar Town": 150,
    "Township": 150,
    "Model Town": 200,
    "Garden Town": 200,
    "Faisal Town": 200,
    "Gulberg": 250,
    "Wapda Town": 200,
    "DHA Lahore": 300,
    "Bahria Town Lahore": 350,
    "Valencia Town": 250,
}


FREE_DELIVERY_THRESHOLD = 3000


def get_delivery_fee(area, subtotal):
    if area == "Other":
        return None

    if subtotal >= FREE_DELIVERY_THRESHOLD:
        return 0

    return DELIVERY_FEES.get(area)


def get_item_price(category, item_name, size=None):
    item = MENU[category][item_name]

    if "sizes" in item:
        if not size:
            raise ValueError(
                f"Size is required for {item_name}."
            )

        return item["sizes"][size]

    return item["price"]


def calculate_subtotal(cart):
    subtotal = 0

    for item in cart:
        subtotal += (
            item["unit_price"] * item["quantity"]
        )

    return subtotal


def calculate_total(cart, area):
    subtotal = calculate_subtotal(cart)

    delivery_fee = get_delivery_fee(
        area,
        subtotal,
    )

    if delivery_fee is None:
        return {
            "subtotal": subtotal,
            "delivery_fee": None,
            "total": None,
        }

    total = subtotal + delivery_fee

    return {
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
    }
