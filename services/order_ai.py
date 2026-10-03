import json
import re

from crews.order_crew import create_order_crew


def build_customer_message(
    customer_name,
    phone,
    delivery_area,
    address,
    payment_method,
    cart,
):
    lines = [
        f"Customer Name: {customer_name}",
        f"Phone: {phone}",
        f"Delivery Area: {delivery_area}",
        f"Delivery Address: {address}",
        f"Payment Method: {payment_method}",
        "",
        "Customer Order:",
    ]

    for item in cart:
        item_name = item["item_name"]

        if item.get("size"):
            item_name += f" ({item['size']})"

        lines.append(
            f"- {item_name}, "
            f"Quantity: {item['quantity']}"
        )

    return "\n".join(lines)


def parse_validation_result(raw_result):

    if not raw_result:
        raise ValueError(
            "The AI validation returned an empty response."
        )

    text = str(raw_result).strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    try:
        return json.loads(text)

    except json.JSONDecodeError:

        match = re.search(
            r"\{.*\}",
            text,
            flags=re.DOTALL,
        )

        if not match:
            raise ValueError(
                "The AI validation response was not valid JSON."
            )

        try:
            return json.loads(
                match.group(0)
            )

        except json.JSONDecodeError as exc:

            raise ValueError(
                "The AI validation response could not be parsed."
            ) from exc


def validate_order_with_ai(
    customer_name,
    phone,
    delivery_area,
    address,
    payment_method,
    cart,
):

    customer_message = build_customer_message(
        customer_name=customer_name,
        phone=phone,
        delivery_area=delivery_area,
        address=address,
        payment_method=payment_method,
        cart=cart,
    )

    crew = create_order_crew(
        customer_message
    )

    result = crew.kickoff()

    raw_result = getattr(
        result,
        "raw",
        None,
    )

    validation_result = parse_validation_result(
        raw_result
    )

    order_status = validation_result.get(
        "order_status"
    )

    if order_status == "COMPLETE":

        return {
            "valid": True,
            "result": validation_result,
            "message": (
                "AI validation completed successfully."
            ),
        }

    missing_information = validation_result.get(
        "missing_information",
        [],
    )

    return {
        "valid": False,
        "result": validation_result,
        "message": (
            "The AI validation found missing information: "
            + ", ".join(
                str(item)
                for item in missing_information
            )
        ),
    }
