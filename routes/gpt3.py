#!/usr/bin/env python3
from fastapi import APIRouter
import openai
import os
import json

from data.expense_model import ExpenseInput,ExpenseOutput

router = APIRouter()

@router.post("/extract")
@router.post("/gpt3/extract")
async def extract(input: ExpenseInput):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="extract fields from the transaction messages: bank, account, amount, currency, transaction_type: credit/debit/due, date, merchant.\ncurrency is standard currency\nmerchant is not available use \"self\"\nformat json\n " + input.text,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    return ExpenseOutput(**json.loads(response.choices[0].text))
