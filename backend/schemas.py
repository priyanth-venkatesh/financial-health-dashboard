from pydantic import BaseModel


class FinancialInput(BaseModel):
    revenue: float
    expenses: float
    debt: float
    cash: float


class InsightOut(BaseModel):
    summary: str