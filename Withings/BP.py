import csv
import hashlib
import psycopg2


# Config (fill these in)
csv_path = "\\\\192.168.1.66\\Nas\\Health\\Withings\\bp.csv"
#csv_path = "//Nas//Health//Withings//bp.csv"
db_name = "health"
db_user = "flutter"
db_password = "my_strong_password"
db_host = "192.168.1.66"
batch_size = 500  # Adjust the batch size as needed

# Connect to PostgreSQL
conn = psycopg2.connect(
    database=db_name, user=db_user, password=db_password, host=db_host, port="5432"
)
cursor = conn.cursor()

# Hash function 
def generate_hash(row_data):
    row_str = "".join(str(x) for x in row_data)  
    return hashlib.sha256(row_str.encode()).hexdigest()

# Open CSV and process in batches
with open(csv_path, "r") as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Skip header row
    header.append("hash")

    rows_to_insert = []
    insert_query = """
    INSERT INTO wbp (date, heartrate, systolic,diastolic, comments, hash)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (hash) DO NOTHING;  -- Skip duplicates
"""
    for row in reader:
        # Handle empty strings 
        row = [None if val == "" else val for val in row]  

        # Handle invalid numeric values and None
        for i, val in enumerate(row):
            if i in [1, 2,3 ]:  # Indices of numeric columns
                try:
                    if val is not None:  # Check if val is None
                        row[i] = float(val) 
                except ValueError:
                    row[i] = None  # Set to None if not numeric
        
        row_hash = generate_hash(row)
        row.append(row_hash)

        rows_to_insert.append(row)

        # insert batch if batch size is reached
        if len(rows_to_insert) >= batch_size:
            cursor.executemany(insert_query, rows_to_insert)
            conn.commit()
            rows_to_insert = [] # clear the batch

    # Insert remaining rows
    if rows_to_insert:
        cursor.executemany(insert_query, rows_to_insert)
        conn.commit()

cursor.close()
conn.close()
