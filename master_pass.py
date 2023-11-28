import sqlite3

# Database connection and table creation
with sqlite3.connect("SQL.db") as conn:
    print("DATABASE CONNECTION SUCCESSFUL")
    conn.execute("DROP TABLE IF EXISTS SECURITY")
    conn.execute("""
        CREATE TABLE SECURITY (
            IDENTIFIER VARCHAR(255) PRIMARY KEY,
            VALUE VARCHAR(255) NOT NULL
        )
    """)

    # Insert the master password into the SECURITY table
    master_pass = input('Enter Master Password: ')
    conn.execute("INSERT INTO SECURITY (IDENTIFIER, VALUE) VALUES (?, ?)",
                 ('master_pass', master_pass))
    print("Master Password has been set.")

# The connection is automatically closed when leaving the 'with' block
