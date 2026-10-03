from crewai import Task

from agents.validation_agent import create_validation_agent


def create_validation_task():

    validation_agent = create_validation_agent()

    return Task(
        description="""
        Validate the customer order extracted by the previous
        Order Processing task.

        Use the previous task's output as the source of truth.

        Validate:

        1. All products
        2. Quantity of each product
        3. Size or variant where applicable
        4. Customer name
        5. Phone number
        6. Delivery area
        7. Delivery address
        8. Payment method

        Use the restaurant knowledge base to verify that the
        requested products and variants are available.

        Do not invent missing information.

        Return ONLY valid JSON.

        Use exactly this structure:

        {
            "order_status": "COMPLETE",
            "items": [
                {
                    "product": "BBQ Chicken Pizza",
                    "quantity": 2,
                    "size": "Large"
                }
            ],
            "customer_name": "Ahmed",
            "phone": "03001234567",
            "delivery_area": "Johar Town",
            "delivery_address": "Johar Town Lahore",
            "payment_method": "Cash on Delivery (COD)",
            "missing_information": []
        }

        The value of order_status must be either:

        "COMPLETE"

        or

        "INCOMPLETE"

        If information is missing:

        - Use null for that field.
        - Add the missing field to missing_information.

        Do not use Markdown.
        Do not add explanations outside the JSON.
        """,

        expected_output="""
        A valid JSON object containing:

        order_status
        items
        customer_name
        phone
        delivery_area
        delivery_address
        payment_method
        missing_information
        """,

        agent=validation_agent,
    )
