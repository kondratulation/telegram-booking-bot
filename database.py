import sqlite3


def create_database():

    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            name TEXT,
            phone TEXT
        )
        """
    )

    connection.commit()
    connection.close()



def save_booking(user_id, name, phone):

    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO bookings (user_id, name, phone)
        VALUES (?, ?, ?)
        """,
        (user_id, name, phone)
    )

    connection.commit()
    connection.close()



def get_bookings():

    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT user_id, name, phone FROM bookings"
    )

    bookings = cursor.fetchall()

    connection.close()

    return bookings

def delete_last_booking():
    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM bookings WHERE id = (SELECT MAX(id) FROM bookings)"
    )

    connection.commit()
    connection.close()