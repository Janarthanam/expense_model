#!/usr/bin/env python3
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import openai
import os
import json

from data.expense_model import ExpenseInput,ExpenseOutput

router = APIRouter()

__prompt = """convert a text from bank in to json format.
    fields could be: bank*,account*,amount*, currency*, transaction_type, date,transaction_id,beneficiary, beneficiary_type
    fields with * are mandatory fields
    transaction_type is one of credit, debit or due
    beneficiary_type is one of merchant,personal
    default currency is INR
    replace all empty values in json with null
"""

__eot = "<|endoftext|>"

def llm_parser(input: ExpenseInput):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{__prompt}{input.text}{__eot}",
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        print(response)
        return ExpenseOutput(**json.loads(response.choices[0].text))
    except Exception as e:
        print(f"Exception {e} {response}")


@router.post("/extract")
@router.post("/gpt3/extract")
async def extract(input: ExpenseInput):
    return llm_parser(input)
