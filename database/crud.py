from database.connection import get_connection


def create_customer(name, phone, address=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO customers (name, phone, address)
        VALUES (?, ?, ?)
        ON CONFLICT(phone) DO UPDATE SET
            name = excluded.name,
            address = excluded.address
        """,
        (name, phone, address),
    )

    connection.commit()

    cursor.execute(
        "SELECT * FROM customers WHERE phone = ?",
        (phone,),
    )

    customer = cursor.fetchone()

    connection.close()

    return customer


def create_order(
    customer_id,
    payment_method=None,
    total_amount=0,
    status="CONFIRMED",
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO orders (
            customer_id,
            status,
            payment_method,
            total_amount
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            customer_id,
            status,
            payment_method,
            total_amount,
        ),
    )

    connection.commit()

    order_id = cursor.lastrowid

    cursor.execute(
        "SELECT * FROM orders WHERE id = ?",
        (order_id,),
    )

    order = cursor.fetchone()

    connection.close()

    return order

def add_order_item(
    order_id,
    product_name,
    quantity,
    size=None,
    unit_price=0,
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO order_items (
            order_id,
            product_name,
            quantity,
            size,
            unit_price
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            order_id,
            product_name,
            quantity,
            size,
            unit_price,
        ),
    )

    connection.commit()

    item_id = cursor.lastrowid

    cursor.execute(
        "SELECT * FROM order_items WHERE id = ?",
        (item_id,),
    )

    item = cursor.fetchone()

    connection.close()

    return item


def get_order(order_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            orders.id,
            orders.status,
            orders.payment_method,
            orders.total_amount,
            orders.created_at,
            orders.updated_at,
            customers.name,
            customers.phone,
            customers.address
        FROM orders
        JOIN customers
            ON orders.customer_id = customers.id
        WHERE orders.id = ?
        """,
        (order_id,),
    )

    order = cursor.fetchone()

    connection.close()

    return order


def get_order_items(order_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            product_name,
            quantity,
            size,
            unit_price
        FROM order_items
        WHERE order_id = ?
        """,
        (order_id,),
    )

    items = cursor.fetchall()

    connection.close()

    return items


def update_order_status(order_id, status):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (status, order_id),
    )

    connection.commit()

    connection.close()
def get_all_orders():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            orders.id,
            orders.status,
            orders.payment_method,
            orders.total_amount,
            orders.created_at,
            orders.updated_at,
            customers.name,
            customers.phone,
            customers.address
        FROM orders
        JOIN customers
            ON orders.customer_id = customers.id
        ORDER BY orders.created_at DESC
        """
    )

    orders = cursor.fetchall()

    connection.close()

    return orders


def update_order_status(order_id, status):
    allowed_statuses = {
        "NEW",
        "CONFIRMED",
        "PREPARING",
        "OUT_FOR_DELIVERY",
        "DELIVERED",
        "CANCELLED",
    }

    if status not in allowed_statuses:
        raise ValueError(
            f"Invalid order status: {status}"
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (status, order_id),
    )

    connection.commit()

    connection.close()
