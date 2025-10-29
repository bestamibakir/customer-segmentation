import pandas as pd
import psycopg2
from sqlalchemy import create_engine

DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'dbname': 'postgres',  # Başlangıçta postgres db'sine bağlan
    'user': 'postgres',
    'password': '123456'  # Kendi şifrenizi yazın
}
    
    # 1. Postgres'e bağlan ve yeni veritabanı oluştur
def create_database_and_upload():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Eğer veritabanı yoksa oluştur
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'customer_segmentation'")
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute('CREATE DATABASE customer_segmentation')
        print("customer_segmentation database created")
    else:
        print("customer_segmentation is here")
    
    cursor.close()
    conn.close()
    
    # 2. Yeni veritabanına bağlan ve tabloyu oluştur
    # 3. CSV dosyasını oku
    DB_CONFIG['dbname'] = 'customer_segmentation'
    engine = create_engine(f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")
    
    df = pd.read_csv('customer_segmentation.csv')
    print(f"CSV read: {len(df)} row, {len(df.columns)} column")
    
    # 4. Sütun isimlerini temizle (PostgreSQL için)
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # 5. Tarih sütununu düzelt
      # 6. PostgreSQL'e yükle
    if 'dt_customer' in df.columns:
        df['dt_customer'] = pd.to_datetime(df['dt_customer'], dayfirst=True)
    
  
    df.to_sql('customers', engine, if_exists='replace', index=False)
    print(f" {len(df)} row downloaded to PostgreSQL")
    print(f"Table name: customers")
    
    # 7. Basit kontrol sorgusu
    result = pd.read_sql_query("SELECT COUNT(*) as total_rows FROM customers", engine)
    print(f"Control: {result['total_rows'].iloc[0]} row")

if __name__ == "__main__":
    create_database_and_upload()