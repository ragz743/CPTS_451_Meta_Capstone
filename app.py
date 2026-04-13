from flask import Flask, render_template, request, redirect, url_for, flash
from config import SECRET_KEY
from db import fetch_all, execute_query

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/customers", methods=["GET", "POST"])
def customers():
    if request.method == "POST":
        customer_id = request.form["customer_id"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        phone_num = request.form["phone_num"]
        email = request.form["email"]

        try:
            execute_query(
                """
                INSERT INTO Customers (Customer_ID, FirstName, LastName, PhoneNum, Email)
                VALUES (:customer_id, :first_name, :last_name, :phone_num, :email)
                """,
                {
                    "customer_id": customer_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone_num": phone_num,
                    "email": email if email else None,
                },
            )
            flash("Customer added successfully.", "success")
        except Exception as e:
            flash(f"Error adding customer: {str(e)}", "error")

        return redirect(url_for("customers"))

    customer_rows = []
    try:
        customer_rows = fetch_all(
            """
            SELECT Customer_ID, FirstName, LastName, PhoneNum, Email
            FROM Customers
            ORDER BY Customer_ID
            """
        )
    except Exception as e:
        flash(f"Error loading customers: {str(e)}", "error")

    return render_template("customers.html", customers=customer_rows)


@app.route("/customers/delete/<int:customer_id>", methods=["POST"])
def delete_customer(customer_id):
    try:
        execute_query(
            "DELETE FROM Customers WHERE Customer_ID = :customer_id",
            {"customer_id": customer_id},
        )
        flash("Customer deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting customer: {str(e)}", "error")

    return redirect(url_for("customers"))


@app.route("/reservations", methods=["GET", "POST"])
def reservations():
    if request.method == "POST":
        res_id = request.form["res_id"]
        customer_id = request.form["customer_id"]
        table_id = request.form["table_id"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        party_size = request.form["party_size"]
        status = request.form["status"]

        try:
            execute_query(
                """
                INSERT INTO Reservations
                (Res_ID, Customer_ID, Table_ID, Start_Time, End_Time, Party_Size, Status)
                VALUES
                (:res_id, :customer_id, :table_id,
                 TO_TIMESTAMP(:start_time, 'YYYY-MM-DD"T"HH24:MI'),
                 TO_TIMESTAMP(:end_time, 'YYYY-MM-DD"T"HH24:MI'),
                 :party_size, :status)
                """,
                {
                    "res_id": res_id,
                    "customer_id": customer_id,
                    "table_id": table_id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "party_size": party_size,
                    "status": status,
                },
            )
            flash("Reservation added successfully.", "success")
        except Exception as e:
            flash(f"Error adding reservation: {str(e)}", "error")

        return redirect(url_for("reservations"))

    reservation_rows = []
    customer_rows = []
    table_rows = []

    try:
        reservation_rows = fetch_all(
            """
            SELECT
                r.Res_ID,
                r.Customer_ID,
                c.FirstName,
                c.LastName,
                r.Table_ID,
                t.TableNum,
                r.Start_Time,
                r.End_Time,
                r.Party_Size,
                r.Status
            FROM Reservations r
            JOIN Customers c
              ON r.Customer_ID = c.Customer_ID
            JOIN Restaurant_Tables t
              ON r.Table_ID = t.Table_ID
            ORDER BY r.Res_ID
            """
        )

        customer_rows = fetch_all(
            """
            SELECT Customer_ID, FirstName, LastName
            FROM Customers
            ORDER BY Customer_ID
            """
        )

        table_rows = fetch_all(
            """
            SELECT Table_ID, TableNum, Capacity
            FROM Restaurant_Tables
            ORDER BY TableNum
            """
        )
    except Exception as e:
        flash(f"Error loading reservations: {str(e)}", "error")

    return render_template(
        "reservations.html",
        reservations=reservation_rows,
        customers=customer_rows,
        tables=table_rows
    )


@app.route("/reservations/delete/<int:res_id>", methods=["POST"])
def delete_reservation(res_id):
    try:
        execute_query(
            "DELETE FROM Reservations WHERE Res_ID = :res_id",
            {"res_id": res_id},
        )
        flash("Reservation deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting reservation: {str(e)}", "error")

    return redirect(url_for("reservations"))


@app.route("/reservations/update/<int:res_id>", methods=["GET", "POST"])
def update_reservation(res_id):
    if request.method == "POST":
        customer_id = request.form["customer_id"]
        table_id = request.form["table_id"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        party_size = request.form["party_size"]
        status = request.form["status"]

        try:
            execute_query(
                """
                UPDATE Reservations
                SET Customer_ID = :customer_id,
                    Table_ID = :table_id,
                    Start_Time = TO_TIMESTAMP(:start_time, 'YYYY-MM-DD"T"HH24:MI'),
                    End_Time = TO_TIMESTAMP(:end_time, 'YYYY-MM-DD"T"HH24:MI'),
                    Party_Size = :party_size,
                    Status = :status
                WHERE Res_ID = :res_id
                """,
                {
                    "customer_id": customer_id,
                    "table_id": table_id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "party_size": party_size,
                    "status": status,
                    "res_id": res_id,
                },
            )
            flash("Reservation updated successfully.", "success")
            return redirect(url_for("reservations"))
        except Exception as e:
            flash(f"Error updating reservation: {str(e)}", "error")

    reservation = None
    customer_rows = []
    table_rows = []

    try:
        reservation_data = fetch_all(
            """
            SELECT Res_ID, Customer_ID, Table_ID,
                   TO_CHAR(Start_Time, 'YYYY-MM-DD"T"HH24:MI') AS Start_Time_Str,
                   TO_CHAR(End_Time, 'YYYY-MM-DD"T"HH24:MI') AS End_Time_Str,
                   Party_Size, Status
            FROM Reservations
            WHERE Res_ID = :res_id
            """,
            {"res_id": res_id},
        )

        if reservation_data:
            reservation = reservation_data[0]

        customer_rows = fetch_all(
            """
            SELECT Customer_ID, FirstName, LastName
            FROM Customers
            ORDER BY Customer_ID
            """
        )

        table_rows = fetch_all(
            """
            SELECT Table_ID, TableNum, Capacity
            FROM Restaurant_Tables
            ORDER BY TableNum
            """
        )
    except Exception as e:
        flash(f"Error loading reservation for update: {str(e)}", "error")

    return render_template(
        "update_reservation.html",
        reservation=reservation,
        customers=customer_rows,
        tables=table_rows
    )


@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "POST":
        order_id = request.form["order_id"]
        customer_id = request.form["customer_id"]
        order_date = request.form["order_date"]
        total_amount = request.form["total_amount"]
        status = request.form["status"]

        try:
            execute_query(
                """
                INSERT INTO Orders
                (Order_ID, Customer_ID, Order_Date, TotalAmount, Status)
                VALUES
                (:order_id, :customer_id,
                 TO_TIMESTAMP(:order_date, 'YYYY-MM-DD"T"HH24:MI'),
                 :total_amount, :status)
                """,
                {
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "order_date": order_date,
                    "total_amount": total_amount,
                    "status": status,
                },
            )
            flash("Order added successfully.", "success")
        except Exception as e:
            flash(f"Error adding order: {str(e)}", "error")

        return redirect(url_for("orders"))

    order_rows = []
    customer_rows = []

    try:
        order_rows = fetch_all(
            """
            SELECT
                o.Order_ID,
                o.Customer_ID,
                c.FirstName,
                c.LastName,
                o.Order_Date,
                o.TotalAmount,
                o.Status
            FROM Orders o
            JOIN Customers c
              ON o.Customer_ID = c.Customer_ID
            ORDER BY o.Order_ID
            """
        )

        customer_rows = fetch_all(
            """
            SELECT Customer_ID, FirstName, LastName
            FROM Customers
            ORDER BY Customer_ID
            """
        )
    except Exception as e:
        flash(f"Error loading orders: {str(e)}", "error")

    return render_template(
        "orders.html",
        orders=order_rows,
        customers=customer_rows
    )


@app.route("/orders/delete/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    try:
        execute_query(
            "DELETE FROM Orders WHERE Order_ID = :order_id",
            {"order_id": order_id},
        )
        flash("Order deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting order: {str(e)}", "error")

    return redirect(url_for("orders"))


@app.route("/orders/update/<int:order_id>", methods=["GET", "POST"])
def update_order(order_id):
    if request.method == "POST":
        customer_id = request.form["customer_id"]
        order_date = request.form["order_date"]
        total_amount = request.form["total_amount"]
        status = request.form["status"]

        try:
            execute_query(
                """
                UPDATE Orders
                SET Customer_ID = :customer_id,
                    Order_Date = TO_TIMESTAMP(:order_date, 'YYYY-MM-DD"T"HH24:MI'),
                    TotalAmount = :total_amount,
                    Status = :status
                WHERE Order_ID = :order_id
                """,
                {
                    "customer_id": customer_id,
                    "order_date": order_date,
                    "total_amount": total_amount,
                    "status": status,
                    "order_id": order_id,
                },
            )
            flash("Order updated successfully.", "success")
            return redirect(url_for("orders"))
        except Exception as e:
            flash(f"Error updating order: {str(e)}", "error")

    order = None
    customer_rows = []

    try:
        order_data = fetch_all(
            """
            SELECT Order_ID, Customer_ID,
                   TO_CHAR(Order_Date, 'YYYY-MM-DD"T"HH24:MI') AS Order_Date_Str,
                   TotalAmount, Status
            FROM Orders
            WHERE Order_ID = :order_id
            """,
            {"order_id": order_id},
        )

        if order_data:
            order = order_data[0]

        customer_rows = fetch_all(
            """
            SELECT Customer_ID, FirstName, LastName
            FROM Customers
            ORDER BY Customer_ID
            """
        )
    except Exception as e:
        flash(f"Error loading order for update: {str(e)}", "error")

    return render_template(
        "update_order.html",
        order=order,
        customers=customer_rows
    )


@app.route("/orders/items", methods=["GET", "POST"])
def order_items():
    if request.method == "POST":
        order_item_id = request.form["order_item_id"]
        order_id = request.form["order_id"]
        menu_item_id = request.form["menu_item_id"]
        quantity = request.form["quantity"]
        item_price = request.form["item_price"]

        try:
            execute_query(
                """
                INSERT INTO Order_Items
                (Order_Item_ID, Order_ID, MenuItem_ID, Quantity, Item_Price)
                VALUES
                (:order_item_id, :order_id, :menu_item_id, :quantity, :item_price)
                """,
                {
                    "order_item_id": order_item_id,
                    "order_id": order_id,
                    "menu_item_id": menu_item_id,
                    "quantity": quantity,
                    "item_price": item_price,
                },
            )
            flash("Order item added successfully.", "success")
        except Exception as e:
            flash(f"Error adding order item: {str(e)}", "error")

        return redirect(url_for("order_items"))

    item_rows = []
    order_rows = []
    menu_rows = []

    try:
        item_rows = fetch_all(
            """
            SELECT
                oi.Order_Item_ID,
                oi.Order_ID,
                oi.MenuItem_ID,
                mi.ItemName,
                oi.Quantity,
                oi.Item_Price
            FROM Order_Items oi
            JOIN Menu_Items mi
              ON oi.MenuItem_ID = mi.MenuItem_ID
            ORDER BY oi.Order_Item_ID
            """
        )

        order_rows = fetch_all(
            """
            SELECT Order_ID
            FROM Orders
            ORDER BY Order_ID
            """
        )

        menu_rows = fetch_all(
            """
            SELECT MenuItem_ID, ItemName, Price
            FROM Menu_Items
            ORDER BY MenuItem_ID
            """
        )
    except Exception as e:
        flash(f"Error loading order items: {str(e)}", "error")

    return render_template(
        "order_items.html",
        order_items=item_rows,
        orders=order_rows,
        menu_items=menu_rows
    )


@app.route("/orders/items/delete/<int:order_item_id>", methods=["POST"])
def delete_order_item(order_item_id):
    try:
        execute_query(
            "DELETE FROM Order_Items WHERE Order_Item_ID = :order_item_id",
            {"order_item_id": order_item_id},
        )
        flash("Order item deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting order item: {str(e)}", "error")

    return redirect(url_for("order_items"))


@app.route("/payments", methods=["GET", "POST"])
def payments():
    if request.method == "POST":
        payment_id = request.form["payment_id"]
        order_id = request.form["order_id"]
        payment_method = request.form["payment_method"]
        tax_amount = request.form["tax_amount"]
        total_paid = request.form["total_paid"]
        payment_date = request.form["payment_date"]

        try:
            execute_query(
                """
                INSERT INTO Payments
                (Payment_ID, Order_ID, PaymentMethod, TaxAmount, TotalPaid, PaymentDate)
                VALUES
                (:payment_id, :order_id, :payment_method, :tax_amount, :total_paid,
                 TO_TIMESTAMP(:payment_date, 'YYYY-MM-DD"T"HH24:MI'))
                """,
                {
                    "payment_id": payment_id,
                    "order_id": order_id,
                    "payment_method": payment_method,
                    "tax_amount": tax_amount,
                    "total_paid": total_paid,
                    "payment_date": payment_date,
                },
            )
            flash("Payment added successfully.", "success")
        except Exception as e:
            flash(f"Error adding payment: {str(e)}", "error")

        return redirect(url_for("payments"))

    payment_rows = []
    unpaid_orders = []

    try:
        payment_rows = fetch_all(
            """
            SELECT
                p.Payment_ID,
                p.Order_ID,
                c.FirstName,
                c.LastName,
                p.PaymentMethod,
                p.TaxAmount,
                p.TotalPaid,
                p.PaymentDate
            FROM Payments p
            JOIN Orders o
              ON p.Order_ID = o.Order_ID
            JOIN Customers c
              ON o.Customer_ID = c.Customer_ID
            ORDER BY p.Payment_ID
            """
        )

        unpaid_orders = fetch_all(
            """
            SELECT
                o.Order_ID,
                o.TotalAmount,
                c.FirstName,
                c.LastName
            FROM Orders o
            JOIN Customers c
              ON o.Customer_ID = c.Customer_ID
            LEFT JOIN Payments p
              ON o.Order_ID = p.Order_ID
            WHERE p.Order_ID IS NULL
            ORDER BY o.Order_ID
            """
        )
    except Exception as e:
        flash(f"Error loading payments: {str(e)}", "error")

    return render_template(
        "payments.html",
        payments=payment_rows,
        unpaid_orders=unpaid_orders
    )


@app.route("/payments/delete/<int:payment_id>", methods=["POST"])
def delete_payment(payment_id):
    try:
        execute_query(
            "DELETE FROM Payments WHERE Payment_ID = :payment_id",
            {"payment_id": payment_id},
        )
        flash("Payment deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting payment: {str(e)}", "error")

    return redirect(url_for("payments"))


@app.route("/payments/update/<int:payment_id>", methods=["GET", "POST"])
def update_payment(payment_id):
    if request.method == "POST":
        order_id = request.form["order_id"]
        payment_method = request.form["payment_method"]
        tax_amount = request.form["tax_amount"]
        total_paid = request.form["total_paid"]
        payment_date = request.form["payment_date"]

        try:
            execute_query(
                """
                UPDATE Payments
                SET Order_ID = :order_id,
                    PaymentMethod = :payment_method,
                    TaxAmount = :tax_amount,
                    TotalPaid = :total_paid,
                    PaymentDate = TO_TIMESTAMP(:payment_date, 'YYYY-MM-DD"T"HH24:MI')
                WHERE Payment_ID = :payment_id
                """,
                {
                    "order_id": order_id,
                    "payment_method": payment_method,
                    "tax_amount": tax_amount,
                    "total_paid": total_paid,
                    "payment_date": payment_date,
                    "payment_id": payment_id,
                },
            )
            flash("Payment updated successfully.", "success")
            return redirect(url_for("payments"))
        except Exception as e:
            flash(f"Error updating payment: {str(e)}", "error")

    payment = None
    order_rows = []

    try:
        payment_data = fetch_all(
            """
            SELECT
                Payment_ID,
                Order_ID,
                PaymentMethod,
                TaxAmount,
                TotalPaid,
                TO_CHAR(PaymentDate, 'YYYY-MM-DD"T"HH24:MI') AS PaymentDate_Str
            FROM Payments
            WHERE Payment_ID = :payment_id
            """,
            {"payment_id": payment_id},
        )

        if payment_data:
            payment = payment_data[0]

        order_rows = fetch_all(
            """
            SELECT Order_ID
            FROM Orders
            ORDER BY Order_ID
            """
        )
    except Exception as e:
        flash(f"Error loading payment for update: {str(e)}", "error")

    return render_template(
        "update_payment.html",
        payment=payment,
        orders=order_rows
    )

@app.route("/reports")
def reports():
    sales_by_day = []
    popular_items = []
    reservations_by_status = []
    top_customers = []
    unpaid_orders = []

    try:
        sales_by_day = fetch_all(
            """
            SELECT
                TRUNC(PaymentDate) AS Sales_Day,
                COUNT(*) AS Num_Payments,
                SUM(TotalPaid) AS Total_Revenue
            FROM Payments
            GROUP BY TRUNC(PaymentDate)
            ORDER BY Sales_Day
            """
        )

        popular_items = fetch_all(
            """
            SELECT
                mi.MenuItem_ID,
                mi.ItemName,
                SUM(oi.Quantity) AS Total_Quantity_Sold,
                SUM(oi.Quantity * oi.Item_Price) AS Total_Item_Revenue
            FROM Order_Items oi
            JOIN Menu_Items mi
              ON oi.MenuItem_ID = mi.MenuItem_ID
            GROUP BY mi.MenuItem_ID, mi.ItemName
            ORDER BY Total_Quantity_Sold DESC, Total_Item_Revenue DESC
            """
        )

        reservations_by_status = fetch_all(
            """
            SELECT
                Status,
                COUNT(*) AS Reservation_Count
            FROM Reservations
            GROUP BY Status
            ORDER BY Status
            """
        )

        top_customers = fetch_all(
            """
            SELECT
                c.Customer_ID,
                c.FirstName,
                c.LastName,
                COUNT(o.Order_ID) AS Total_Orders,
                NVL(SUM(o.TotalAmount), 0) AS Total_Spent
            FROM Customers c
            LEFT JOIN Orders o
              ON c.Customer_ID = o.Customer_ID
            GROUP BY c.Customer_ID, c.FirstName, c.LastName
            ORDER BY Total_Spent DESC, Total_Orders DESC
            """
        )

        unpaid_orders = fetch_all(
            """
            SELECT
                o.Order_ID,
                c.FirstName,
                c.LastName,
                o.TotalAmount,
                o.Status
            FROM Orders o
            JOIN Customers c
              ON o.Customer_ID = c.Customer_ID
            LEFT JOIN Payments p
              ON o.Order_ID = p.Order_ID
            WHERE p.Order_ID IS NULL
            ORDER BY o.Order_ID
            """
        )
    except Exception as e:
        flash(f"Error loading reports: {str(e)}", "error")

    return render_template(
        "reports.html",
        sales_by_day=sales_by_day,
        popular_items=popular_items,
        reservations_by_status=reservations_by_status,
        top_customers=top_customers,
        unpaid_orders=unpaid_orders
    )

if __name__ == "__main__":
    app.run(debug=True)
