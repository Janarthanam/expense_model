from data.expense_model import ExpenseInput, ExpenseOutput

#import joblib
import re
from fastapi import APIRouter

router = APIRouter()

# Load the machine learning model
# model = joblib.load("model.joblib")

debit_matcher = re.compile(r'\bAcct\s+(?P<account_number>\w+).*?for\s+Rs\s+(?P<amount>\d+\.\d{2}).*?on\s+(?P<date>\d{1,2}-[A-Za-z]{3}-\d{2}).*?(?P<beneficiary>[a-zA-Z\s]+)\bcredited')

# Define the API endpoint
@router.post("/regex/extract")
async def extract(input: ExpenseInput):
    # Make the prediction using the loaded model
    # prediction = model.predict([[feature1, feature2, feature3]])
    return extract_feature(input)

def extract_feature(expense_input: ExpenseInput) -> ExpenseOutput:
    match = debit_matcher.search(expense_input.text)
    out = ExpenseOutput()
    if not match:
        return out
    
    print(f"{match.groupdict()}")
    out.debit = True
    out.account = match.group(1)
    out.amount = match.group(2)
    out.date = match.group(3)
    out.beneficiary = match.group(4)

    return out

#test
test_input = {
    "text" : "ICICI Bank Acct XX601 debited for Rs 407.00 on 22-Mar-23; ALL MARKET SOBH credited."
}
response = extract_feature(ExpenseInput(**test_input))
print(response)
