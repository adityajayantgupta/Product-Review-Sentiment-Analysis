import sqlite3
import threading

# Create a thread-local storage for the database connection
local_storage = threading.local()

# Define a function to get the database connection for the current thread
def get_db_connection():
  if not hasattr(local_storage, 'conn') or local_storage.conn is None:
    local_storage.conn = sqlite3.connect('product_sentiment.db')
  return local_storage.conn

# Define a function to update the brand score based on a review
def update_brand_score(brand_name, sentiment_score, platform):
  # Create a table to store the brand scores
  conn = get_db_connection()
  conn.execute('''
    CREATE TABLE IF NOT EXISTS brand_scores (
        brand_name TEXT PRIMARY KEY,
        total_score FLOAT,
        num_reviews INTEGER,
        platform TEXT
    )''')
  # Check if the brand already exists in the database
  result = conn.execute('SELECT * FROM brand_scores WHERE brand_name = ?', (brand_name,)).fetchone()
  if result is None:
    # If the brand doesn't exist, insert a new row with the initial score
    conn.execute('INSERT INTO brand_scores (brand_name, total_score, num_reviews, platform) VALUES (?, ?, 1, ?)', (brand_name, sentiment_score, platform))
  else:
    # If the brand exists, update the total score and increment the number of reviews
    total_score = result[1] + sentiment_score
    num_reviews = result[2] + 1
    conn.execute('UPDATE brand_scores SET total_score = ?, num_reviews = ? WHERE brand_name = ?', (total_score, num_reviews, brand_name))
  # Commit the changes to the database
  conn.commit()
  close_connection()

# Define a function to close the database connection for the current thread
def close_connection():
  if hasattr(local_storage, 'conn') and local_storage.conn is not None:
    local_storage.conn.close()
    local_storage.conn = None
