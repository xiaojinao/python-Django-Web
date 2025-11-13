import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name LIKE "myapp_%"')
tables = [row[0] for row in cursor.fetchall()]
print("Tables found:", tables)