import sqlite3
from sqlite3 import Error
import json
import threading


# Create a thread-local storage for the database connection
local_storage = threading.local()

# Define a function to get the database connection for the current thread
def get_db_connection(db_file):
  if not hasattr(local_storage, 'conn') or local_storage.conn is None:
    local_storage.conn = sqlite3.connect(db_file)
  return local_storage.conn



def store_analyzed_product(result, platform):
  conn = get_db_connection('cached_products.db')
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS analyzed_products
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT UNIQUE,              
                platform TEXT,
                result TEXT)''')
  conn.commit()
  product_name = result[platform]["product_data"]["product_name"]
  result_str = json.dumps(result[platform])
  try:
    c.execute('''INSERT INTO analyzed_products (product_name, platform, result)
                VALUES (?, ?, ?)''', (product_name, platform, result_str))
    conn.commit()
  except sqlite3.IntegrityError as e:
    # Handle the case where the product name already exists in the table
    print(f"Error inserting {product_name}: {str(e)}")
  close_connection()

def check_cached_product(product_name):
  conn = get_db_connection('cached_products.db')
  c = conn.cursor()
  c.execute("SELECT result FROM analyzed_products WHERE product_name=?", (product_name,))
  result = c.fetchone()
  close_connection()
  if result:
      return json.loads(result[0])
  else:
      return {}
  
# Define a function to close the database connection for the current thread
def close_connection():
  if hasattr(local_storage, 'conn') and local_storage.conn is not None:
    local_storage.conn.close()
    local_storage.conn = None
