from pydantic import BaseModel

# Define the input schema
class ExpenseInput(BaseModel):
    text: str

class ExpenseOutput(BaseModel):
    debit: bool = False
    account: str | None
    amount: float | None
    merchant: str | None
    date: str | None
    bank: str | None
    currency: str = "INR"
    transaction_type: str = "debit"
