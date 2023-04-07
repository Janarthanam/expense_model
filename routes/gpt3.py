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

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"convert bank messages to json format. keys in json: \"bank\", \"account\", \"amount\", \"currency\", \"transaction_type\":credit/debit/due, \"date\", \"beneficiary\", \"msg_date\", \"transaction_id\", \"beneficiary_type\", \"merchant_type\"\nbeneficiary is not available use \"self\"\nbeneficiary_type is individual or merchant. \nmerchant_type\ncurrency use standard currency type\nmsg_date is same as date\ntransaction_id is a string\n{input.text}",
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0
        )

        return ExpenseOutput(**json.loads(response.choices[0].text))
    except Exception as e:
        print(f"Exception {response.choices[0].text}")
