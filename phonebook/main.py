import psycopg2
import csv

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="1488",
    port="5432"
)
cur = conn.cursor()

# Insert from csv
def insert_from_csv(filename):
    try:
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (row[0].strip(), row[1].strip()))
        conn.commit()
        print("Data inserted successfully")
    except FileNotFoundError:
        print("File not founded")

# Insert from console
def insert_from_console():
    name = input("Enter first name: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()

# Create table
def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            phone VARCHAR(20)
        );
    """)
    conn.commit()

    # Update datas
def update_data():
    enter = input("What you want to update: 'name' or 'phone'? ").strip().lower()
    if enter == "name":
        old_name = input("Enter current name: ")
        new_name = input("Enter new name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (old_name,))
        user = cur.fetchone()
        if user:
            cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
            conn.commit()
            print("Data is updated.")
        else:
            print("No such user found.")
    elif enter == "phone":
        name = input("Enter name to change phone: ")
        new_phone = input("Enter new phone: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
        user = cur.fetchone()
        if user:
            cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", (new_phone, name))
            conn.commit()
            print("phone updated.")
        else:
            print("No such user found.")
    else:
        print("Wrong choice.")

        # Query with filters
def query_data():
    print("\nSelect request type:")
    print("1. Show all users")
    print("2. Search by name")
    print("3. Search by phone")

    choice = input("Your choise (1-3): ").strip()

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
    elif choice == "2":
        namee = input("Enter name to search: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f'%{namee}%',))
    elif choice == "3":
        phonee = input("Enter a phone number to search: ")
        cur.execute("SELECT * FROM phonebook WHERE phone ILIKE %s", (f'%{phonee}%',))
    else:
        print("Wrong choice.")
        return

    rows = cur.fetchall()
    if rows:
        print("\nResults:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No such user found.")

        # Delete data
def delete_data():
    filter = input("Delete by 'name' or 'phone'? ").strip().lower()
    value = input("Enter the value to delete: ")
    if filter == "name":
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (value,))
        user = cur.fetchone()
        if user:
            cur.execute("DELETE FROM phonebook WHERE first_name = %s", (value,))
            conn.commit()
            print("User deleted.")
        else:
            print("No such user found.")
    elif filter == "phone":
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (value,))
        user = cur.fetchone()
        if user:
            cur.execute("DELETE FROM phonebook WHERE phone = %s", (value,))
            conn.commit()
            print("User deleted.")
        else:
            print("No such user found.")
    else:
        print("Wrong choice.")

        #Starting position
if __name__ == "__main__":
    create_table()
    while True:    
        nado = int(input("\nChoose one of the variations:\n1 - insert from console\n2 - insert from csv\n3 - update values\n4 - query data\n5 - delete data\nInput number: "))

        if nado == 1:
            insert_from_console()
        if nado == 2:
            insert_from_csv("/Users/mukhametaliissayev/Desktop/python/phonebook/lab10.csv")
        if nado == 3:
            update_data()
        if nado == 4:
            query_data()
        if nado == 5:
            delete_data()


    cur.close()
    conn.close()