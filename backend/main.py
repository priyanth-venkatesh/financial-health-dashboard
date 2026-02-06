from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd
import os

from database import SessionLocal, engine, Base
from models import User, FinancialRecord, Insight
from simple_auth import create_token

from pydantic import BaseModel

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend access (Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DB Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- Schemas ----------------
class LoginRequest(BaseModel):
    email: str
    password: str


# ---------------- Root ----------------
@app.get("/")
def root():
    return {"message": "Finance backend is running 🚀"}


# ---------------- Login ----------------
@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.email)
    return {"token": token}


# ---------------- Upload CSV & Analyze ----------------
@app.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Read CSV
        df = pd.read_csv(file.file)

        # Validate required columns
        required_cols = {"revenue", "expenses", "debt", "cash"}
        if not required_cols.issubset(set(df.columns)):
            raise HTTPException(
                status_code=400,
                detail="CSV must contain columns: revenue, expenses, debt, cash",
            )

        summaries = []

        for _, row in df.iterrows():
            revenue = float(row["revenue"])
            expenses = float(row["expenses"])
            debt = float(row["debt"])
            cash = float(row["cash"])

            # Save financial record
            record = FinancialRecord(
                user_id=1,  # demo user
                revenue=revenue,
                expenses=expenses,
                debt=debt,
                cash=cash,
            )
            db.add(record)

            # Simple rule-based insight
            if revenue > expenses and cash > debt:
                summary = "The business is profitable with healthy liquidity."
            elif revenue > expenses:
                summary = "The business is profitable but liquidity risk detected."
            else:
                summary = "The business is running at a loss. Reduce expenses."

            insight = Insight(user_id=1, summary=summary)
            db.add(insight)

            summaries.append(summary)

        db.commit()

        return {
            "summary": summaries[-1],  # return latest insight
            "all_summaries": summaries,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
