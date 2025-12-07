from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id")
    children: list["Category"] = Relationship(back_populates="parent", sa_relationship_kwargs={"cascade":"all,delete"})
    parent: Optional["Category"] = Relationship(back_populates="children")

class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    balance: float = 0.0
    currency: str = "USD"

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    currency: str = "USD"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    description: Optional[str] = None
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    year_month: str  # format YYYY-MM
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    amount: float

class PlannedItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    amount: float
    due_date: Optional[datetime] = None
    type: str = "expense"  # or 'income'
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

class Attachment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    path: str
    transaction_id: Optional[int] = Field(default=None, foreign_key="transaction.id")
    planned_id: Optional[int] = Field(default=None, foreign_key="planneditem.id")
