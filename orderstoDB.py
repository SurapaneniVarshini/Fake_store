import sqlite3
import pandas as pd

def create_orders_table(headers):
    conn = sqlite3.connect('Store.db')
    c = conn.cursor()

    # Drop the table if it exists
    c.execute("DROP TABLE IF EXISTS orders")

    # Create the orders table
    table_columns = ', '.join(headers)
    create_table_query = f"CREATE TABLE orders ({table_columns})"
    c.execute(create_table_query)

    conn.commit()
    conn.close()

def insert_data_into_orders(data):
    conn = sqlite3.connect('Store.db')

    # Insert the data into the orders table
    data.to_sql('orders', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()

def excel_to_database():
    # Read the Excel file
    df = pd.read_excel('orders.xlsx', engine='openpyxl')

    # Modify the column names
    df.rename(columns={'Product Name': 'ProductName', 'Total Price': 'TotalPrice'}, inplace=True)

    # Get the headers from the DataFrame
    headers = df.columns.tolist()

    # Create the orders table
    create_orders_table(headers)

    # Insert the data into the orders table
    insert_data_into_orders(df)

    print("Data inserted into the orders table successfully!")

# Call the function to transfer the Excel data to the database
excel_to_database()
