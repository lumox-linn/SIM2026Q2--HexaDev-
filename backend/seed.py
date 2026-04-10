"""
Seed script — inserts 100+ test users into the `useraccount` table.
Run from backend/ folder: python seed.py
"""
import os, random
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import MySQLdb

load_dotenv()
conn = MySQLdb.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    user=os.getenv('MYSQL_USER', 'root'),
    passwd=os.getenv('MYSQL_PASSWORD', ''),
    db=os.getenv('MYSQL_DB', 'csit314'),
)
cur = conn.cursor()

FIRST = ['Alice','Bob','Charlie','Diana','Ethan','Fiona','George','Hannah',
         'Ivan','Julia','Kevin','Laura','Michael','Nina','Oscar','Paula',
         'Quinn','Rachel','Steven','Tina','Uma','Victor','Wendy','Xander','Yara','Zach']
LAST  = ['Tan','Lim','Wong','Lee','Ng','Chen','Koh','Ong','Teo','Goh',
         'Chua','Yap','Sim','Tay','Ho','Low','Phua','Soh','Wee','Foo']

def make(n, role):
    f, l = random.choice(FIRST), random.choice(LAST)
    is_active = 0 if random.random() < 0.1 else 1  # 10% suspended
    return (
        f"{f.lower()}.{l.lower()}{n}",
        generate_password_hash("Password123!"),
        is_active,
        role
    )

# Known demo accounts (easy to use for demo/testing)
users = [
    ('admin01',     generate_password_hash('admin123'),   1, 'admin'),
    ('fr01',        generate_password_hash('fr123'),      1, 'fund_raiser'),
    ('donee01',     generate_password_hash('donee123'),   1, 'donee'),
    ('pm01',        generate_password_hash('pm123'),      1, 'platform_manager'),
    ('suspended01', generate_password_hash('test123'),    0, 'donee'),
]

# Bulk test data — 100+ records
for i in range(1, 6):  users.append(make(i, 'admin'))
for i in range(1, 6):  users.append(make(i, 'platform_manager'))
for i in range(1, 46): users.append(make(i, 'fund_raiser'))
for i in range(1, 46): users.append(make(i, 'donee'))

# Insert — columns match useraccount table exactly
cur.executemany(
    "INSERT IGNORE INTO useraccount (username, password_hash, isActive, role) VALUES (%s, %s, %s, %s)",
    users
)
conn.commit()
print(f"Seeded {cur.rowcount} users into useraccount table.")
cur.close()
conn.close()
