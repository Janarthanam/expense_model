#!/usr/bin/env python3
# Extracting bulk transaction data and categorizing merchant
# There may be many formats. currently we are interested in pdf only
#

import io
import openai
import json
from fastapi import APIRouter, FastAPI, File, UploadFile
import PyPDF2

router = APIRouter()

__model = "text-davinci-003"
__prompt = """statement from bank
transactions are in table format
format only transactions as json
date, details, amount, cr/dr, balance, benificiary/merchant, category
beneficiary for UPI look like email
category may be personal
"""

__eot = "<|endoftext|>"


@router.post("/extract_bulk")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type == 'application/pdf':
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))

        try:
            result = []
            for page in pdf_reader.pages:
                print(page.extract_text())
                response = openai.Completion.create(
                    model = __model,
                    temperature = 0,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    max_tokens=1000,
                    prompt = f"{__prompt}{page.extract_text()}{__eot}"
                )
                print(response.choices[0].text)
                result.append(json.loads(response.choices[0].text))
        except Exception as e:
            print(f"Exception {e}")

        return {"text": result}
    else:
        return {"error": "Invalid file type"}
