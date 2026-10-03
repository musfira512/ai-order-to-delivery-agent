import streamlit as st

from flows.order_flow import create_order_flow
from database.crud import (
    get_order,
    get_order_items,
    get_all_orders,
    update_order_status,
)


st.set_page_config(
    page_title="AI Order-to-Delivery Agent",
    page_icon="🍽️",
    layout="wide",
)


st.title("AI Order-to-Delivery Agent")
st.write("AI-powered order processing and delivery management")


tab1, tab2 = st.tabs([
    "Place Order",
    "Order Dashboard",
])


# ============================================================
# CUSTOMER ORDER
# ============================================================

with tab1:

    st.subheader("Place an Order")

    customer_message = st.text_area(
        "Enter your order",
        placeholder=(
            "Example: I want 2 large BBQ chicken pizzas. "
            "My name is Ali, phone 03001234567, "
            "address Johar Town Lahore, and I will pay by COD."
        ),
        height=150,
    )

    if st.button(
        "Process Order",
        type="primary",
        key="process_order",
    ):

        if not customer_message.strip():

            st.warning("Please enter an order first.")

        else:

            with st.spinner("Processing your order..."):

                flow = create_order_flow(
                    customer_message
                )

                flow.kickoff()

            saved = flow.state.get(
                "saved",
                False,
            )

            st.divider()

            if saved:

                order_id = flow.state.get(
                    "order_id"
                )

                status = flow.state.get(
                    "status"
                )

                st.success(
                    f"Order #{order_id} created successfully."
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Order ID",
                        f"#{order_id}",
                    )

                with col2:
                    st.metric(
                        "Status",
                        status,
                    )

                order = get_order(order_id)

                items = get_order_items(
                    order_id
                )

                st.subheader(
                    "Order Details"
                )

                if order:

                    st.write(
                        f"**Customer:** "
                        f"{order['name']}"
                    )

                    st.write(
                        f"**Phone:** "
                        f"{order['phone']}"
                    )

                    st.write(
                        f"**Address:** "
                        f"{order['address']}"
                    )

                    st.write(
                        f"**Payment:** "
                        f"{order['payment_method']}"
                    )

                st.subheader("Items")

                for item in items:

                    size_text = (
                        f" ({item['size']})"
                        if item["size"]
                        else ""
                    )

                    st.write(
                        f"• {item['quantity']} × "
                        f"{item['product_name']}"
                        f"{size_text}"
                    )

            else:

                st.error(
                    "The order could not be created."
                )

                message = flow.state.get(
                    "message",
                    "Please check the order information.",
                )

                st.info(message)


# ============================================================
# ORDER DASHBOARD
# ============================================================

with tab2:

    st.subheader("Order Dashboard")

    orders = get_all_orders()

    if not orders:

        st.info("No orders found.")

    else:

        st.write(
            f"Total orders: **{len(orders)}**"
        )

        st.divider()

        for order in orders:

            order_id = order["id"]

            with st.expander(
                f"Order #{order_id} | "
                f"{order['name']} | "
                f"{order['status']}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Customer:** "
                        f"{order['name']}"
                    )

                    st.write(
                        f"**Phone:** "
                        f"{order['phone']}"
                    )

                    st.write(
                        f"**Address:** "
                        f"{order['address']}"
                    )

                with col2:

                    st.write(
                        f"**Payment:** "
                        f"{order['payment_method']}"
                    )

                    st.write(
                        f"**Created:** "
                        f"{order['created_at']}"
                    )

                    st.write(
                        f"**Current Status:** "
                        f"{order['status']}"
                    )

                st.write("**Items:**")

                items = get_order_items(
                    order_id
                )

                for item in items:

                    size_text = (
                        f" ({item['size']})"
                        if item["size"]
                        else ""
                    )

                    st.write(
                        f"• {item['quantity']} × "
                        f"{item['product_name']}"
                        f"{size_text}"
                    )

                st.divider()

                status_options = [
                    "NEW",
                    "CONFIRMED",
                    "PREPARING",
                    "OUT_FOR_DELIVERY",
                    "DELIVERED",
                    "CANCELLED",
                ]

                current_status = order["status"]

                new_status = st.selectbox(
                    "Update Status",
                    status_options,
                    index=status_options.index(
                        current_status
                    ),
                    key=f"status_{order_id}",
                )

                if st.button(
                    "Update Order",
                    key=f"update_{order_id}",
                ):

                    update_order_status(
                        order_id,
                        new_status,
                    )

                    st.success(
                        f"Order #{order_id} updated "
                        f"to {new_status}."
                    )

                    st.rerun()
