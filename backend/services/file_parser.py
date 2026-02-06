from fastapi import UploadFile
import pandas as pd
import pdfplumber


def parse_file(file: UploadFile):
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)
    elif file.filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return {"raw_text": text}
    else:
        raise ValueError("Unsupported file format")

    return df.to_dict(orient="list")