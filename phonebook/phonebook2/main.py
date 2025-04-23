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

# Execute a query
def execute_query(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# FILTER BY 1'st LETTER FUNCTION
create_func_filter_by_first_letter = """
    CREATE OR REPLACE FUNCTION filter_by_first_letter(letter VARCHAR(1))
    RETURNS TABLE (id INTEGER, first_name VARCHAR(50), phone VARCHAR(20))
    AS
    $$
    BEGIN
        RETURN QUERY
        SELECT * FROM phonebook22 WHERE LEFT(phonebook22.first_name, 1) = letter;
    END;
    $$
    LANGUAGE plpgsql;
"""
def call_function_w_args(function_name, args):
    try:
        with conn.cursor() as cur:
            cur.callproc(function_name, args)
            return cur.fetchall()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)




# INSERT PROCEDURE 
create_procedure_insert_new =   """
    CREATE OR REPLACE PROCEDURE add_new_user(
    new_first_name VARCHAR,
    new_phone VARCHAR(20)
    )
    AS $$
    BEGIN
        -- If user already exists, update the phone number
        IF EXISTS (SELECT 1 FROM phonebook2 WHERE first_name = new_first_name) THEN
            UPDATE phonebook2
            SET phone = new_phone
            WHERE first_name = new_first_name;
        ELSE
            -- Otherwise, insert a new user
            INSERT INTO phonebook2(first_name, phone)
            VALUES(new_first_name, new_phone);
        END IF;
    END;
    $$
    LANGUAGE plpgsql;
"""     
def insert_new(user, phone):
    user_to_insert = (user, phone)
    command = "CALL add_new_user(%s, %s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, user_to_insert)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# INSERT PROCEDURE FOR MULTIPLE USERS
create_procedure_insert_new_list=   """ 
    CREATE OR REPLACE PROCEDURE add_new_user_list(
        new_first_name varchar,
        new_phone varchar(20)
    ) 
    AS $$
    BEGIN
        -- insert into the phonebook2 table
        INSERT INTO phonebook2(first_name, phone)
        VALUES(new_first_name, new_phone);
    END;
    $$
    LANGUAGE PLPGSQL;
"""     
def insert_new_list(users_to_insert): 

    command = "CALL add_new_user(%s, %s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, users_to_insert) 
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# DELETE PROCEDURE
create_procedure_delete_user = """
    CREATE OR REPLACE PROCEDURE delete_user(user_2_del VARCHAR, phone_2_del VARCHAR(20))
    AS $$
    BEGIN
        DELETE FROM phonebook2 WHERE phonebook2.first_name = user_2_del OR phonebook2.phone = phone_2_del;
    END;
    $$
    LANGUAGE plpgsql;
"""
def delete_user(user, phone):
    user_to_delete = (user, phone)
    command = "CALL delete_user(%s, %s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, user_to_delete)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


#MENU
MENU = """
1. Insert new user
2. Insert new user from csv file
3. Delete user
4. Filter by first letter
5. Exit
"""
while True:
    print(MENU)
    choice = input("Enter your choice: ")
    if choice == '1':     # insert user
        first_name = input("Enter user name: ")
        phone = input("Enter phone number: ")
        insert_new(first_name, phone)
    elif choice == '2':   # insert from csv
        csv_file_name = input("Enter csv file name without (.csv): ")
        with open(f"{csv_file_name}.csv", 'r') as file:
            reader = csv.reader(file)
            _ = next(reader) # getting rid of the headers
            for row in reader:
                insert_new_list(row)
    elif choice == '3':   # delete user
        user_2_del = input("Enter user name (Enter if you want to delete by phone): ")
        if user_2_del == '':
            phone_2_del = input("Enter phone number: ")
            delete_user(user_2_del, phone_2_del)
        else:
            phone_2_del = ''
            delete_user(user_2_del, phone_2_del)
    elif choice == '4':   # filter by first letter
        letter = tuple((input("Enter the first letter: ")).upper())
        print(call_function_w_args('filter_by_first_letter', letter))
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please try again.")

# execute_query(create_procedure_delete_user)
# execute_query(create_procedure_insert_new_list)
# execute_query(create_procedure_insert_new)
# execute_query(create_func_filter_by_first_letter)