import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the DATABASE_URL from the environment
DATABASE_URL = os.getenv('DATABASE')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TransactionRecord(Base):
    __tablename__ = 'transaction_records'
    id = Column(Integer, primary_key=True)
    order_id = Column(String, index=True)
    transaction_type = Column(String)
    payment_type = Column(String)
    net_amount = Column(Float)
    invoice_amount = Column(Float)
    description = Column(String)  

Base.metadata.create_all(bind=engine)

def load_data_to_database(df, db_session):
    try:
        transactions = [
            TransactionRecord(
                order_id=row['Order ID'],
                transaction_type=row['Transaction Type'],
                payment_type=row['Payment Type'],
                net_amount=row['Net Amount'],
                invoice_amount=row['Invoice Amount'],
                description=row['Description']
            )
            for index, row in df.iterrows()
        ]
        db_session.bulk_save_objects(transactions)
        db_session.commit()
        print("Data loaded to the database successfully")
    except Exception as e:
        db_session.rollback()
        print(f"Error loading data to the database: {str(e)}")
        raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    # Read the Merchant Tax Report and Payment Report
    df_merchant = pd.read_excel('/mnt/data/Merchant.xlsx')
    df_payment = pd.read_csv('/mnt/data/Payment.csv')

    # Process Merchant Tax Report
    df_merchant = df_merchant[df_merchant['Transaction Type'] != 'Cancel']
    df_merchant['Transaction Type'] = df_merchant['Transaction Type'].replace({'Refund': 'Return', 'FreeReplacement': 'Return'})

    # Process Payment Report
    df_payment = df_payment[df_payment['Type'] != 'Transfer']
    df_payment = df_payment.rename(columns={'Type': 'Payment Type'})
    df_payment['Payment Type'] = df_payment['Payment Type'].replace({
        'Ajdustment': 'Order', 'FBA Inventory Fee': 'Order', 'Fulfilment Fee Refund': 'Order', 'Service Fee': 'Order', 'Refund': 'Return'
    })
    df_payment['Transaction Type'] = 'Payment'

    # Merge DataFrames
    df_combined = pd.concat([df_merchant, df_payment], ignore_index=True)

    # Use a database session to load data
    with SessionLocal() as session:
        load_data_to_database(df_combined, session)

# Reads data from both the Merchant Tax Report and the Payment Report.
# Processes each according to your specifications.
# Merges them into a single DataFrame.
# Loads the data into your database using SQLAlchemy ORM.
