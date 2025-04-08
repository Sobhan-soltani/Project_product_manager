import mysql.connector
from datetime import datetime
import json
from model import Order
from model.payment import Payment


def check_payment_status(payment):
    if payment.payment_status == Payment.PAYMENT_STATUS_PAID:
        return True
    else:
        return False




def add_payment_to_db(user, order_item_list=None):

    if not check_payment_status():
        return False, "payment failed"

    #
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        #MySQL
        conn = mysql.connector.connect(
            host="localhost",       # آدرس سرور MySQL
            user="root",            # نام کاربری
            password="yourpassword",# رمز عبور
            database="yourdatabase" # نام دیتابیس
        )
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user VARCHAR(255) NOT NULL,
                date_time DATETIME NOT NULL,
                order_item_list JSON
            )
        ''')


        order_json = json.dumps(order_item_list) if order_item_list else None


        cursor.execute('''
            INSERT INTO payments (user, date_time, order_item_list)
            VALUES (%s, %s, %s)
        ''', (user, current_time, order_json))

        conn.commit()
        cursor.close()
        conn.close()
        return True, "Payment was added"

    except mysql.connector.Error as err:
        return False, f"ERROR in Data Base: {err}"