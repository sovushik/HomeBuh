"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Category schemas
class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True


# Account schemas
class AccountCreate(BaseModel):
    name: str
    balance: float = 0.0
    currency: str = "USD"


class AccountResponse(BaseModel):
    id: int
    name: str
    balance: float
    currency: str

    class Config:
        from_attributes = True


# Transaction schemas
class TransactionCreate(BaseModel):
    amount: float
    currency: Optional[str] = "USD"
    description: Optional[str] = None
    account_id: Optional[int] = None
    category_id: Optional[int] = None


class TransactionResponse(BaseModel):
    id: int
    amount: float
    currency: str
    timestamp: datetime
    description: Optional[str]
    account_id: Optional[int]
    category_id: Optional[int]

    class Config:
        from_attributes = True


# Budget schemas
class BudgetCreate(BaseModel):
    year_month: str = Field(..., description="Format: YYYY-MM")
    category_id: Optional[int] = None
    amount: float


class BudgetResponse(BaseModel):
    id: int
    year_month: str
    category_id: Optional[int]
    amount: float

    class Config:
        from_attributes = True


# PlannedItem schemas
class PlannedItemCreate(BaseModel):
    title: str
    amount: float
    due_date: Optional[datetime] = None
    type: str = "expense"  # or 'income'
    category_id: Optional[int] = None


class PlannedItemResponse(BaseModel):
    id: int
    title: str
    amount: float
    due_date: Optional[datetime]
    type: str
    category_id: Optional[int]

    class Config:
        from_attributes = True


# Transfer schemas
class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float = Field(..., gt=0, description="Amount must be positive")
    currency: Optional[str] = "USD"
    description: Optional[str] = None


class TransferResponse(BaseModel):
    status: str
    from_tx: TransactionResponse
    to_tx: TransactionResponse


# AI Report schemas
class AIReportRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    query: Optional[str] = None


class ChartInfo(BaseModel):
    title: str
    url: str


class AIReportResponse(BaseModel):
    text: str
    charts: List[ChartInfo] = []


# Health check response
class HealthResponse(BaseModel):
    status: str
