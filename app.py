import os
import streamlit as st

from data.menu import MENU
from database.models import create_tables
from database.crud import (
    create_customer,
    create_order,
    add_order_item,
    get_all_orders,
    get_order_items,
    update_order_status,
)
from utils.pricing import calculate_subtotal, calculate_total
from services.order_ai import validate_order_with_ai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Urban Bites",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

create_tables()


# ============================================================
# MANAGEMENT LOGIN SETTINGS
# ============================================================

# For development/demo purposes these have fallback values.
# Before deployment, set ADMIN_USERNAME and ADMIN_PASSWORD
# as Streamlit secrets or environment variables.

ADMIN_USERNAME = os.getenv(
    "ADMIN_USERNAME",
    "admin",
)

ADMIN_PASSWORD = os.getenv(
    "ADMIN_PASSWORD",
    "urbanbites123",
)


# ============================================================
# SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "order_confirmed" not in st.session_state:
    st.session_state.order_confirmed = False

if "confirmed_order" not in st.session_state:
    st.session_state.confirmed_order = None

if "management_authenticated" not in st.session_state:
    st.session_state.management_authenticated = False

if "page" not in st.session_state:
    st.session_state.page = "Customer Ordering"


# ============================================================
# CUSTOM LIGHT THEME
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #fffaf0;
    }

    [data-testid="stSidebar"] {
        background-color: #fff3cd;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #8b3a00;
    }

    h1 {
        color: #d35400;
    }

    h2 {
        color: #c2410c;
    }

    h3 {
        color: #9a3412;
    }

    .restaurant-title {
        font-size: 38px;
        font-weight: 800;
        color: #d35400;
        margin-bottom: 4px;
    }

    .restaurant-subtitle {
        font-size: 17px;
        color: #6b4f3a;
        margin-bottom: 25px;
    }

    .price-text {
        font-size: 18px;
        font-weight: 700;
        color: #b45309;
    }

    .order-id {
        font-size: 18px;
        font-weight: 700;
        color: #9a3412;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        # 🍔 Urban Bites
        ### Restaurant Ordering System
        """
    )

    st.markdown("")

    customer_button = st.button(
        "🛒 Customer Ordering",
        use_container_width=True,
    )

    management_button = st.button(
        "🔐 Management Login",
        use_container_width=True,
    )

    if customer_button:
        st.session_state.page = "Customer Ordering"

    if management_button:
        st.session_state.page = "Management Login"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def reset_customer_order():
    """Reset the customer ordering session."""

    st.session_state.cart = []
    st.session_state.order_confirmed = False
    st.session_state.confirmed_order = None


def add_item_to_cart(
    category,
    item_name,
    size,
    quantity,
):
    """Add a selected menu item to the cart."""

    item = MENU[category][item_name]

    if "sizes" in item:
        unit_price = item["sizes"][size]
    else:
        unit_price = item["price"]

    cart_item = {
        "category": category,
        "item_name": item_name,
        "size": size,
        "quantity": quantity,
        "unit_price": unit_price,
    }

    st.session_state.cart.append(cart_item)


def get_item_display_name(item):
    """Create a readable cart item name."""

    name = item["item_name"]

    if item.get("size"):
        name += f" ({item['size']})"

    return name


def show_order_summary(
    customer_name,
    phone,
    delivery_area,
    address,
    payment_method,
):
    """Display the current order summary."""

    subtotal = calculate_subtotal(
        st.session_state.cart
    )

    if delivery_area == "Other":

        if subtotal >= 3000:
            delivery_fee = 0
        else:
            delivery_fee = 300

    else:

        pricing = calculate_total(
            st.session_state.cart,
            delivery_area,
        )

        delivery_fee = pricing.get(
            "delivery_fee"
        )

    if delivery_fee is None:
        st.error(
            "Delivery fee could not be calculated "
            "for the selected area."
        )
        return None

    total = subtotal + delivery_fee

    st.markdown("### 🧾 Order Summary")

    st.write(
        f"**Customer:** {customer_name}"
    )

    st.write(
        f"**Phone:** {phone}"
    )

    st.write(
        f"**Delivery Area:** {delivery_area}"
    )

    st.write(
        f"**Address:** {address}"
    )

    st.write(
        f"**Payment:** {payment_method}"
    )

    st.markdown("#### 🍽️ Items")

    for item in st.session_state.cart:

        item_name = get_item_display_name(
            item
        )

        item_total = (
            item["unit_price"]
            * item["quantity"]
        )

        st.write(
            f"• {item_name} × "
            f"{item['quantity']} "
            f"= Rs. {item_total:,}"
        )

    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:
        st.write(
            f"**Subtotal:** Rs. {subtotal:,}"
        )

        st.write(
            f"**Delivery Fee:** Rs. {delivery_fee:,}"
        )

    with col2:
        st.markdown(
            f"### Total: Rs. {total:,}"
        )

    return {
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
    }


# ============================================================
# CUSTOMER ORDERING PAGE
# ============================================================

def customer_ordering_page():

    if st.session_state.order_confirmed:

        order = st.session_state.confirmed_order

        st.markdown(
            '<div class="restaurant-title">'
            "🍔 Urban Bites"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="restaurant-subtitle">'
            "Fresh food. Simple ordering."
            "</div>",
            unsafe_allow_html=True,
        )

        st.success("✅ Order Confirmed")

        st.write(
            "Your order has been saved successfully."
        )

        st.markdown(
            f"""
            **Order ID:** #{order["order_id"]}  

            **Tracking ID:** {order["tracking_id"]}
            """
        )

        st.markdown("### 📦 Order Details")

        st.write(
            f"**Customer:** {order['customer_name']}"
        )

        st.write(
            f"**Phone:** {order['phone']}"
        )

        st.write(
            f"**Delivery Area:** {order['delivery_area']}"
        )

        st.write(
            f"**Address:** {order['address']}"
        )

        st.write(
            f"**Payment:** {order['payment_method']}"
        )

        st.markdown("### 🍽️ Order Summary")

        for item in order["items"]:

            item_name = item["item_name"]

            if item.get("size"):
                item_name += (
                    f" ({item['size']})"
                )

            item_total = (
                item["unit_price"]
                * item["quantity"]
            )

            st.write(
                f"• {item_name} × "
                f"{item['quantity']} "
                f"= Rs. {item_total:,}"
            )

        st.write(
            f"**Subtotal:** "
            f"Rs. {order['subtotal']:,}"
        )

        st.write(
            f"**Delivery Fee:** "
            f"Rs. {order['delivery_fee']:,}"
        )

        st.markdown(
            f"### Total: Rs. {order['total']:,}"
        )

        st.markdown("")

        if st.button(
            "🍽️ Start New Order",
            use_container_width=True,
        ):

            reset_customer_order()

            st.rerun()

        return

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="restaurant-title">'
        "🍔 Urban Bites"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="restaurant-subtitle">'
        "Fresh food. Simple ordering."
        "</div>",
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # CUSTOMER INFORMATION
    # --------------------------------------------------------

    st.markdown("### 👤 Customer Information")

    col1, col2 = st.columns(2)

    with col1:

        customer_name = st.text_input(
            "Customer Name",
            placeholder="Enter your name",
        )

    with col2:

        delivery_area = st.selectbox(
            "Delivery Area",
            [
                "Johar Town",
                "Township",
                "Model Town",
                "Garden Town",
                "Faisal Town",
                "Gulberg",
                "Wapda Town",
                "DHA Lahore",
                "Bahria Town Lahore",
                "Valencia Town",
                "Other",
            ],
        )

    col1, col2 = st.columns(2)

    with col1:

        phone = st.text_input(
            "Phone Number",
            placeholder="03XXXXXXXXX",
        )

    with col2:

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Cash on Delivery (COD)",
                "JazzCash",
                "EasyPaisa",
                "Bank Account",
            ],
        )

    address = st.text_area(
        "Complete Delivery Address",
        placeholder=(
            "House/Flat number, street, "
            "block, area, etc."
        ),
        height=100,
    )

    # --------------------------------------------------------
    # DELIVERY POLICY
    # --------------------------------------------------------

    st.markdown("### 🚚 Delivery Policy")

    st.write(
        "• Free delivery on orders of Rs. 3,000 or more "
        "within standard delivery areas."
    )

    st.write(
        "• Orders below Rs. 3,000 are charged according "
        "to the selected delivery area."
    )

    st.write(
        "• Other areas have a fixed delivery charge of "
        "Rs. 300 for orders below Rs. 3,000."
    )

    # --------------------------------------------------------
    # MENU
    # --------------------------------------------------------

    st.markdown("### 🍽️ Menu")

    categories = list(MENU.keys())

    category = st.selectbox(
        "Category",
        categories,
    )

    items = list(
        MENU[category].keys()
    )

    item_name = st.selectbox(
        "Item",
        items,
    )

    selected_item = MENU[
        category
    ][item_name]

    # --------------------------------------------------------
    # ITEM DESCRIPTION
    # --------------------------------------------------------

    description = selected_item.get(
        "description"
    )

    if description:

        st.write(
            f"_{description}_"
        )

    # --------------------------------------------------------
    # SIZE / VARIANT
    # --------------------------------------------------------

    size = None

    if "sizes" in selected_item:

        size_options = list(
            selected_item["sizes"].keys()
        )

        size = st.selectbox(
            "Size / Variant",
            size_options,
        )

        unit_price = selected_item[
            "sizes"
        ][size]

    else:

        unit_price = selected_item[
            "price"
        ]

    # --------------------------------------------------------
    # QUANTITY
    # --------------------------------------------------------

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=20,
        value=1,
        step=1,
    )

    st.write(
        f"**Price:** Rs. {unit_price:,}"
    )

    if st.button(
        "🛒 Add to Cart",
        use_container_width=True,
    ):

        add_item_to_cart(
            category=category,
            item_name=item_name,
            size=size,
            quantity=quantity,
        )

        st.success(
            f"{item_name} added to cart."
        )

    # --------------------------------------------------------
    # CART
    # --------------------------------------------------------

    if st.session_state.cart:

        st.markdown("### 🛒 Your Cart")

        for index, item in enumerate(
            st.session_state.cart
        ):

            item_name_display = (
                get_item_display_name(
                    item
                )
            )

            item_total = (
                item["unit_price"]
                * item["quantity"]
            )

            col1, col2 = st.columns(
                [5, 1]
            )

            with col1:

                st.write(
                    f"**{item_name_display}** "
                    f"× {item['quantity']} "
                    f"= Rs. {item_total:,}"
                )

            with col2:

                if st.button(
                    "Remove",
                    key=f"remove_{index}",
                ):

                    st.session_state.cart.pop(
                        index
                    )

                    st.rerun()

        # ----------------------------------------------------
        # TOTAL CALCULATION
        # ----------------------------------------------------

        subtotal = calculate_subtotal(
            st.session_state.cart
        )

        if delivery_area == "Other":

            if subtotal >= 3000:
                delivery_fee = 0
            else:
                delivery_fee = 300

        else:

            pricing = calculate_total(
                st.session_state.cart,
                delivery_area,
            )

            delivery_fee = pricing.get(
                "delivery_fee"
            )

        if delivery_fee is not None:

            total = (
                subtotal
                + delivery_fee
            )

            st.markdown("### 💰 Order Total")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(
                    f"**Subtotal**  \n"
                    f"Rs. {subtotal:,}"
                )

            with col2:
                st.write(
                    f"**Delivery**  \n"
                    f"Rs. {delivery_fee:,}"
                )

            with col3:
                st.write(
                    f"**Total**  \n"
                    f"Rs. {total:,}"
                )

            # ------------------------------------------------
            # ORDER ACTIONS
            # ------------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✏️ Edit Order",
                    use_container_width=True,
                ):

                    st.info(
                        "You can remove items from "
                        "your cart or add more items "
                        "above."
                    )

            with col2:

                confirm_order = st.button(
                    "✅ Confirm Order",
                    use_container_width=True,
                )

                if confirm_order:

                    # ----------------------------------------
                    # BASIC CHECKOUT VALIDATION
                    # ----------------------------------------

                    if not customer_name.strip():

                        st.error(
                            "Please enter your name."
                        )

                    elif not phone.strip():

                        st.error(
                            "Please enter your phone number."
                        )

                    elif not address.strip():

                        st.error(
                            "Please enter your complete "
                            "delivery address."
                        )

                    elif not st.session_state.cart:

                        st.error(
                            "Your cart is empty."
                        )

                    elif delivery_fee is None:

                        st.error(
                            "Delivery fee could not be "
                            "calculated."
                        )

                    else:

                        # ------------------------------------
                        # AI AGENT VALIDATION
                        # ------------------------------------

                        with st.spinner(
                            "🤖 AI agents are processing your order..."
                        ):

                            try:

                                ai_validation = (
                                    validate_order_with_ai(
                                        customer_name=(
                                            customer_name.strip()
                                        ),
                                        phone=phone.strip(),
                                        delivery_area=(
                                            delivery_area
                                        ),
                                        address=(
                                            address.strip()
                                        ),
                                        payment_method=(
                                            payment_method
                                        ),
                                        cart=(
                                            st.session_state.cart
                                        ),
                                    )
                                )

                            except Exception as exc:

                                st.error(
                                    "AI order processing failed. "
                                    "The order was not saved."
                                )

                                st.caption(
                                    f"AI error: {exc}"
                                )

                                ai_validation = None

                        # ------------------------------------
                        # CHECK AI RESULT
                        # ------------------------------------

                        if ai_validation is not None:

                            if not ai_validation["valid"]:

                                st.error(
                                    "❌ AI validation could not "
                                    "complete this order."
                                )

                                st.write(
                                    ai_validation["message"]
                                )

                            else:

                                st.success(
                                    "🤖 AI agents successfully "
                                    "validated the order."
                                )

                                # --------------------------------
                                # SAVE CUSTOMER
                                # --------------------------------

                                customer = create_customer(
                                    name=customer_name.strip(),
                                    phone=phone.strip(),
                                    address=address.strip(),
                                )

                                # --------------------------------
                                # SAVE ORDER
                                # --------------------------------

                                order = create_order(
                                    customer_id=customer["id"],
                                    payment_method=payment_method,
                                    total_amount=total,
                                    status="CONFIRMED",
                                )

                                order_id = order["id"]

                                # --------------------------------
                                # SAVE ORDER ITEMS
                                # --------------------------------

                                for item in (
                                    st.session_state.cart
                                ):

                                    add_order_item(
                                        order_id=order_id,
                                        product_name=item[
                                            "item_name"
                                        ],
                                        quantity=item[
                                            "quantity"
                                        ],
                                        size=item.get(
                                            "size"
                                        ),
                                        unit_price=item[
                                            "unit_price"
                                        ],
                                    )

                                # --------------------------------
                                # SAVE CONFIRMATION DATA
                                # --------------------------------

                                st.session_state.confirmed_order = {
                                    "order_id": order_id,
                                    "tracking_id": (
                                        f"UB-{order_id:04d}"
                                    ),
                                    "customer_name": (
                                        customer_name.strip()
                                    ),
                                    "phone": phone.strip(),
                                    "delivery_area": (
                                        delivery_area
                                    ),
                                    "address": (
                                        address.strip()
                                    ),
                                    "payment_method": (
                                        payment_method
                                    ),
                                    "items": (
                                        st.session_state.cart.copy()
                                    ),
                                    "subtotal": subtotal,
                                    "delivery_fee": (
                                        delivery_fee
                                    ),
                                    "total": total,
                                }

                                st.session_state.order_confirmed = True

                                st.rerun()

    else:

        st.info(
            "Your cart is empty. Add items from "
            "the menu to continue."
        )


# ============================================================
# MANAGEMENT LOGIN
# ============================================================

def management_login_page():

    st.markdown(
        '<div class="restaurant-title">'
        "🔐 Management Login"
        "</div>",
        unsafe_allow_html=True,
    )

    st.write(
        "This area is restricted to Urban Bites management."
    )

    st.markdown("")

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        username = st.text_input(
            "Username",
            key="management_username",
        )

        password = st.text_input(
            "Password",
            type="password",
            key="management_password",
        )

        login = st.button(
            "🔓 Login",
            use_container_width=True,
        )

        if login:

            if (
                username == ADMIN_USERNAME
                and password == ADMIN_PASSWORD
            ):

                st.session_state.management_authenticated = True
                st.session_state.page = "Admin Dashboard"

                st.success(
                    "Login successful."
                )

                st.rerun()

            else:

                st.error(
                    "Invalid management username or password."
                )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_dashboard_page():

    # --------------------------------------------------------
    # SECURITY CHECK
    # --------------------------------------------------------

    if not st.session_state.management_authenticated:

        st.session_state.page = "Management Login"

        st.warning(
            "Please log in as management to access this page."
        )

        if st.button(
            "🔐 Go to Management Login"
        ):

            st.rerun()

        return

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    col1, col2 = st.columns(
        [5, 1]
    )

    with col1:

        st.markdown(
            '<div class="restaurant-title">'
            "📊 Urban Bites Management"
            "</div>",
            unsafe_allow_html=True,
        )

        st.write(
            "Order management and workflow dashboard."
        )

    with col2:

        if st.button(
            "Logout",
            use_container_width=True,
        ):

            st.session_state.management_authenticated = False
            st.session_state.page = "Customer Ordering"

            st.rerun()

    # --------------------------------------------------------
    # GET ORDERS
    # --------------------------------------------------------

    orders = get_all_orders()

    if not orders:

        st.info(
            "No orders have been placed yet."
        )

        return

    # --------------------------------------------------------
    # ORDER COUNTS
    # --------------------------------------------------------

    total_orders = len(orders)

    confirmed_orders = sum(
        1
        for order in orders
        if order["status"] == "CONFIRMED"
    )

    preparing_orders = sum(
        1
        for order in orders
        if order["status"] == "PREPARING"
    )

    delivery_orders = sum(
        1
        for order in orders
        if order["status"] == "OUT_FOR_DELIVERY"
    )

    delivered_orders = sum(
        1
        for order in orders
        if order["status"] == "DELIVERED"
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total Orders",
            total_orders,
        )

    with col2:
        st.metric(
            "Confirmed",
            confirmed_orders,
        )

    with col3:
        st.metric(
            "Preparing",
            preparing_orders,
        )

    with col4:
        st.metric(
            "Out for Delivery",
            delivery_orders,
        )

    with col5:
        st.metric(
            "Delivered",
            delivered_orders,
        )

    # --------------------------------------------------------
    # ORDERS
    # --------------------------------------------------------

    st.markdown("### 📋 Orders")

    status_options = [
        "CONFIRMED",
        "PREPARING",
        "OUT_FOR_DELIVERY",
        "DELIVERED",
        "CANCELLED",
    ]

    for order in orders:

        order_title = (
            f"Order #{order['id']} | "
            f"{order['name']} | "
            f"{order['status']}"
        )

        with st.expander(
            order_title
        ):

            # -----------------------------------------------
            # CUSTOMER DETAILS
            # -----------------------------------------------

            st.markdown("#### 👤 Customer")

            st.write(
                f"**Name:** {order['name']}"
            )

            st.write(
                f"**Phone:** {order['phone']}"
            )

            st.write(
                f"**Address:** {order['address']}"
            )

            st.write(
                f"**Payment:** "
                f"{order['payment_method']}"
            )

            # -----------------------------------------------
            # ITEMS
            # -----------------------------------------------

            st.markdown("#### 🍽️ Items")

            items = get_order_items(
                order["id"]
            )

            for item in items:

                item_name = item[
                    "product_name"
                ]

                if item["size"]:

                    item_name += (
                        f" ({item['size']})"
                    )

                item_total = (
                    item["unit_price"]
                    * item["quantity"]
                )

                st.write(
                    f"• {item_name} × "
                    f"{item['quantity']} "
                    f"= Rs. {item_total:,.0f}"
                )

            # -----------------------------------------------
            # TOTAL
            # -----------------------------------------------

            st.markdown("#### 💰 Order Total")

            st.write(
                f"**Total:** "
                f"Rs. {order['total_amount']:,.0f}"
            )

            # -----------------------------------------------
            # STATUS UPDATE
            # -----------------------------------------------

            st.markdown("#### 🔄 Update Status")

            current_status = order[
                "status"
            ]

            current_index = 0

            if current_status in status_options:
                current_index = status_options.index(
                    current_status
                )

            new_status = st.selectbox(
                "Order Status",
                status_options,
                index=current_index,
                key=f"status_{order['id']}",
            )

            if st.button(
                "Update Status",
                key=f"update_{order['id']}",
                use_container_width=True,
            ):

                update_order_status(
                    order_id=order["id"],
                    status=new_status,
                )

                st.success(
                    f"Order #{order['id']} "
                    f"updated to {new_status}."
                )

                st.rerun()


# ============================================================
# PAGE ROUTING
# ============================================================

if st.session_state.page == "Customer Ordering":

    customer_ordering_page()

elif st.session_state.page == "Management Login":

    management_login_page()

elif st.session_state.page == "Admin Dashboard":

    admin_dashboard_page()
