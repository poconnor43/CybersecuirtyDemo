import sqlite3
from passwordMake import generate_password
from lookUp import whois_lookup


def create_table():
    # Connect to the SQLite database (creates a new database if it doesn't exist)
    conn = sqlite3.connect('credentials.db')
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    # Create a table to store website credentials
    cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (
                        id INTEGER PRIMARY KEY,
                        website_name TEXT NOT NULL,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')

    # Create a table to store user accounts
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    )''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def insert_credentials(website_name, username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    # Insert new credentials into the table
    cursor.execute('INSERT INTO credentials (website_name, username, password) VALUES (?, ?, ?)', (website_name, username, password))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def print_table():
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()

    # Retrieve all records from the table
    cursor.execute('SELECT * FROM credentials')
    records = cursor.fetchall()

    # Print the table
    print("Website Name\tUsername\tPassword")
    for record in records:
        print(f"{record[1]}\t{record[2]}\t{record[3]}")

    # Close the connection
    conn.close()

def delete_credentials(website_name):
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()

    # Delete credentials from the table based on website name
    cursor.execute('DELETE FROM credentials WHERE website_name = ?', (website_name,))
    conn.commit()
    conn.close()

def delete_account(username):
    # Connect to the SQLite database
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()

    # Delete user account from the accounts table
    cursor.execute('DELETE FROM accounts WHERE username = ?', (username,))

    # Delete all credentials associated with the user
    cursor.execute('DELETE FROM credentials WHERE username = ?', (username,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def update_credentials(website_name, new_username=None, new_password=None):
    # Connect to the SQLite database
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()

    # Update username and/or password for the specified website
    if new_username is not None:
        cursor.execute('UPDATE credentials SET username = ? WHERE website_name = ?', (new_username, website_name))
    if new_password is not None:
        cursor.execute('UPDATE credentials SET password = ? WHERE website_name = ?', (new_password, website_name))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def main():
    # the way we created our table this will allow the same information to be stored
    create_table()

    # Check if there are any accounts in the database
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM accounts')
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        # If no accounts exist, prompt the user to create one
        print("No accounts found. We created you an account")
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        # Insert the new account into the accounts table
        conn = sqlite3.connect('credentials.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO accounts (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        print("Account created successfully!")

    while True:
        choice = input("Enter:\n 'add' to add new credentials,\n 'delete' to delete credentials,\n 'update' to update credentials,\n 'print' to print the table,\n 'delete account' to delete the account and all associated credentials,\n 'create password' to create a secure password,\n 'website info' to see websites information,\n or 'quit' to exit: ")
        
        if choice.lower() == 'add':
            website_name = input("Enter website name: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            insert_credentials(website_name, username, password)
        
        elif choice.lower() == 'delete':
            website_name = input("Enter website name to delete credentials: ")
            delete_credentials(website_name)
        
        elif choice.lower() == 'update':
            website_name = input("Enter website name to update credentials: ")
            new_username = input("Enter new username (leave blank to keep current): ")
            new_password = input("Enter new password (leave blank to keep current): ")
            update_credentials(website_name, new_username=new_username, new_password=new_password)
        
        elif choice.lower() == 'print':
            print("\nCredentials stored in the database:")
            print_table()
        
        elif choice.lower() == 'delete account':
            username = input("Enter username to delete the account and all associated credentials: ")
            delete_account(username)
            print(f"Account '{username}' and associated credentials deleted successfully!")
        
        elif choice.lower() == 'create password':
            generate_password()

        elif choice.lower() == 'website info':
            websiteName = input("please enter the websites name including the .com/.org/etc portions\n")
            info= whois_lookup(websiteName)
            print(info)

        elif choice.lower() == 'quit':
            break

if __name__ == "__main__":
    main()