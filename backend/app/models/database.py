from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the DATABASE_URL from the environment
DATABASE_URL=os.getenv('DATABASE')

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()