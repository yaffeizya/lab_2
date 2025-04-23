import psycopg2

# Current user name
current_user = ''

# Database connection setup
conn = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="1488",
    port="5432"
)

#  Create "users" table
query_create_table_users = """
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE
    )
"""

# Create "user_scores" table
query_create_table_user_scores = """
    CREATE TABLE IF NOT EXISTS user_scores(
        id SERIAL PRIMARY KEY,
        username VARCHAR(255),
        score INTEGER,
        level INTEGER
    )
"""

# Execute a SQL query
def execute_query(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print( error)

# Input user name
def input_user():
    global current_user
    current_user = input("Enter your username: ")

# Add new user to the database
def add_user(name):
    command = "INSERT INTO users(username) VALUES(%s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (name,))
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print("add_user:", error)

# Check if a user already exists
def check_if_user_exists(name):
    command = "SELECT username FROM users WHERE username = %s"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (name,))
            result = cur.fetchall()
            return bool(result)
    except (psycopg2.DatabaseError, Exception) as error:
        print("check_if_user_exists:", error)

# Insert new score
def add_new_score(score, lvl):
    command = "INSERT INTO user_scores(username, score, level) VALUES(%s, %s, %s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (current_user, score, lvl))
            conn.commit()
            print(f"[OK] Score saved: {current_user}, Score: {score}, Level: {lvl}")
    except (psycopg2.DatabaseError, Exception) as error:
        print(" add_new_score:", error)

# Save game score
def process_score(score, lvl):
    print(f"[DEBUG] Saving: {score}, level: {lvl}, user: {current_user}")
    user_exists = check_if_user_exists(current_user)
    if not user_exists:
        print(" User not found")
        add_user(current_user)
    add_new_score(score, lvl)

# Show user's highest level
def show_highest_level():
    command = "SELECT MAX(level) FROM user_scores WHERE username = %s"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (current_user,))
            result = cur.fetchall()
            return result
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    execute_query(query_create_table_users)
    execute_query(query_create_table_user_scores)
    