from simple_auth import create_token
from models import User

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models, schemas

from services.financial_metrics import compute_metrics
from services.ai_insights import generate_insight

from fastapi import UploadFile, File
import pandas as pd


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")

    # 🔹 DEMO USER (auto-create if not exists)
    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(email=email, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)

    # 🔹 Simple password check (demo only)
    if user.password != password:
        return {"error": "Invalid password"}

    token = create_token(user.email)

    return {"access_token": token, "token_type": "bearer"}

@app.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Read CSV
    df = pd.read_csv(file.file)

    # Take first row for demo
    row = df.iloc[0]

    revenue = float(row["revenue"])
    expenses = float(row["expenses"])
    debt = float(row["debt"])
    cash = float(row["cash"])

    # Reuse existing analysis logic
    metrics = compute_metrics(
        {
            "revenue": revenue,
            "expenses": expenses,
            "debt": debt,
            "cash": cash,
        }
    )

    insight_text = generate_insight(metrics)

    # Chart data for frontend
    chart_data = [
        {"name": "Revenue", "value": revenue},
        {"name": "Expenses", "value": expenses},
        {"name": "Debt", "value": debt},
        {"name": "Cash", "value": cash},
    ]

    return {
        "summary": insight_text,
        "chart_data": chart_data,
    }


@app.post("/analyze", response_model=schemas.InsightOut)
def analyze(data: schemas.FinancialInput, db: Session = Depends(get_db)):

    metrics = compute_metrics(data.dict())

    insight_text = generate_insight(metrics)

    insight = models.Insight(user_id=1, summary=insight_text)
    db.add(insight)
    db.commit()

    return {"summary": insight_text}