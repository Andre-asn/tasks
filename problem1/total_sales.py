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

def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j][1] < data[j + 1][1]:
                temp = data[j]
                data[j] = data[j + 1]
                data[j + 1] = temp
    return data

query = """
SELECT p.name, SUM(s.quantity * p.price) AS total_sales, p.category
FROM sales s
JOIN products p ON s.product_id = p.id
GROUP BY s.product_id;
"""
cursor.execute(query)
results = cursor.fetchall()

sorted_sales = bubble_sort(results)

print("Top 5 Best-Selling Products:")
for i in range(min(5, len(sorted_sales))):
    name = sorted_sales[i][0]
    total = sorted_sales[i][1]
    print(f"{name} - ${total}")

category_revenue = {}
for row in results:
    name = row[0]
    total_sales = row[1]
    category = row[2]

    if category not in category_revenue:
        category_revenue[category] = 0
    category_revenue[category] += total_sales

print("\nTotal Revenue per Category:")
for category in category_revenue:
    print(f"{category}: ${category_revenue[category]}")

conn.close()
