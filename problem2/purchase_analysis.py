import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT"))
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

conn = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)
cursor = conn.cursor()

def merge_sort(data):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    while left and right:
        if left[0][2] > right[0][2]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left or right)
    return result


cursor.execute("""
    SELECT c.id, c.name, SUM(p.amount) AS total_spent
    FROM customers c
    JOIN purchases p ON c.id = p.customer_id
    GROUP BY c.id;
""")
customer_data = cursor.fetchall()

sorted_customers = merge_sort([ (row[0], row[1], row[2]) for row in customer_data ])

tiers = []
total_customers = len(sorted_customers)
for i in range(total_customers):
    cid, name, total = sorted_customers[i]
    if i < total_customers * 0.2:
        tier = "Gold"
    elif i < total_customers * 0.6:
        tier = "Silver"
    else:
        tier = "Bronze"
    tiers.append((name, total, tier))

gold = sum(1 for _, _, t in tiers if t == "Gold")
silver = sum(1 for _, _, t in tiers if t == "Silver")
bronze = sum(1 for _, _, t in tiers if t == "Bronze")

print(f"\nTier Summary: {gold} Gold, {silver} Silver, {bronze} Bronze customers")

print("\nCLV:")
for name, total, _ in tiers:
    print(f"{name}: ${total:.2f}")

print("\nRolling 3-Month Spend Average (first 15 rows):")
cursor.execute("""
    SELECT 
        c.name,
        p.purchase_date,
        p.amount,
        ROUND(AVG(p.amount) OVER (
            PARTITION BY p.customer_id 
            ORDER BY p.purchase_date 
            RANGE BETWEEN INTERVAL 3 MONTH PRECEDING AND CURRENT ROW
        ), 2) AS rolling_avg
    FROM purchases p
    JOIN customers c ON p.customer_id = c.id
    ORDER BY c.name, p.purchase_date;
""")
rolling_data = cursor.fetchall()

for row in rolling_data[:15]:
    print(f"{row[0]} | {row[1]} | Purchase: ${row[2]} | 3-Month Avg: ${row[3]}")

conn.close()