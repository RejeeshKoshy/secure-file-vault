from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -------------------------------
# Replace this with your DB URL
# For SQLite (local dev):
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# For PostgreSQL (if needed):
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
# -------------------------------

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ This is what routes/auth.py is importing
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
