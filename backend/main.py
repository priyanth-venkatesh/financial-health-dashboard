from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd

from database import SessionLocal, engine, Base
from models import User, FinancialRecord, Insight
from simple_auth import create_token
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- LOGIN SCHEMA ----------------
class LoginRequest(BaseModel):
    email: str
    password: str


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "Backend working ✅"}


# ---------------- LOGIN ----------------
@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token(user.email)
    return {"token": token}


# ---------------- UPLOAD CSV ----------------
@app.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):

    df = pd.read_csv(file.file)

    required_cols = {"revenue", "expenses", "debt", "cash"}
    if not required_cols.issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail="CSV must contain: revenue, expenses, debt, cash",
        )

    summaries = []

    for _, row in df.iterrows():
        revenue = float(row["revenue"])
        expenses = float(row["expenses"])
        debt = float(row["debt"])
        cash = float(row["cash"])

        record = FinancialRecord(
            user_id=1,
            revenue=revenue,
            expenses=expenses,
            debt=debt,
            cash=cash,
        )
        db.add(record)

        if revenue > expenses and cash > debt:
            summary = "Profitable with healthy liquidity."
        elif revenue > expenses:
            summary = "Profitable but liquidity risk."
        else:
            summary = "Running at loss. Reduce expenses."

        db.add(Insight(user_id=1, summary=summary))
        summaries.append(summary)

    db.commit()

    return {"summary": summaries[-1], "all": summaries}
