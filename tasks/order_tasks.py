from crewai import Task

from agents.order_agent import create_order_agent


def create_order_task(customer_message):

    order_agent = create_order_agent()

    return Task(
        description=f"""
        Analyze the following customer checkout information.

        Customer information and order:
        {customer_message}

        Extract ALL ordered products.

        For every product identify:
        1. Product name
        2. Quantity
        3. Size or variant, if applicable

        Also identify:
        4. Customer name
        5. Phone number
        6. Delivery area
        7. Delivery address
        8. Payment method

        Use the restaurant knowledge base to understand
        the available menu and restaurant information.

        Do not invent products, prices, sizes, or policies.

        If information is missing, clearly identify it.
        """,

        expected_output="""
        Return a structured order summary containing:

        Products:
        - Product:
          Quantity:
          Size/Variant:

        Customer Name:
        Phone:
        Delivery Area:
        Delivery Address:
        Payment Method:

        Missing Information:
        """,

        agent=order_agent,
    )
