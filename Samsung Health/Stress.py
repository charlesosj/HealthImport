import csv
import hashlib
import psycopg2

csv_path = "\\\\192.168.1.66\\Nas\\Health\\Samsung Health\\com.samsung.shealth.stress.20240616225180.csv"
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
# Hash function (unchanged from your original code)
# Hash Function
# Hash Function
def generate_hash(row_data):
    row_str = "".join(str(x) for x in row_data)
    return hashlib.sha256(row_str.encode()).hexdigest()

# CSV Processing and Batch Insertion
with open(csv_path, "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the first header line
    header = next(reader)  # Get the actual header row
    header.append("hash")

    rows_to_insert = []
    insert_query = """
        INSERT INTO stress (
            create_sh_ver, start_time, custom, binning_data, tag_id,
            modify_sh_ver, update_time, create_time, max, min, score,
            algorithm, time_offset, deviceuuid, comment, pkg_name,
            end_time, hash
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (hash) DO NOTHING;
    """

    for row in reader:
        # Data Cleaning and Type Conversion (with improved handling)
        row = [None if val == "" else val for val in row]

        # Robustly handle rows with missing or extra values
        while len(row) < 17:  # Pad with None if too few columns
            row.append(None)
        row = row[:17]  # Truncate if too many columns

        for i, val in enumerate(row):
            if i in [0, 4, 5, 11]:  # Integer columns
                try:
                    row[i] = int(val) if val is not None else None
                except ValueError:
                    row[i] = None  # Handle non-integer values
            elif i in [8, 9, 10]:  # Numeric columns
                try:
                    row[i] = float(val) if val is not None else None
                except ValueError:
                    row[i] = None  # Handle non-numeric values
            elif i in [1, 6, 7, 16]:  # Timestamp columns
                try:
                    row[i] = val  # Assuming ISO 8601 format
                except ValueError:
                    row[i] = None  # Handle invalid timestamps
            # Add similar conversion logic for other data types as needed

        # Calculate and Append Hash
        row_hash = generate_hash(row)
        row.append(row_hash)

        rows_to_insert.append(row)

        # Batch Insert
        if len(rows_to_insert) >= batch_size:
            cursor.executemany(insert_query, rows_to_insert)
            conn.commit()
            rows_to_insert = []

    # Insert Remaining Rows
    if rows_to_insert:
        cursor.executemany(insert_query, rows_to_insert)
        conn.commit()

# Close Connections
cursor.close()
conn.close()