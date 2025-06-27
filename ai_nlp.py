import spacy
import re

nlp = spacy.load("en_core_web_sm")

def smart_keyword_check(text, keywords):
    doc = nlp(text)
    present_keywords = []
    for keyword in keywords:
        for token in doc:
            if token.similarity(nlp(keyword)[0]) > 0.7:
                present_keywords.append(keyword)
                break
    missing = [kw for kw in keywords if kw not in present_keywords]
    return present_keywords, missing

def extract_specifications(text):
    specs = {}
    patterns = {
        "pH": r"pH[:\s]*([\d.]+)",
        "Appearance": r"Appearance[:\s]*([\w\s,.-]+)",
        "Color": r"Color[:\s]*([\w\s,.-]+)",
        "Odor": r"Odor[:\s]*([\w\s,.-]+)",
        "CO2 Emissions Per Gram": r"CO2 Emissions.*?[:\s]*([\d.]+\s*g)",
        "CO2 Per Kg": r"CO2.*?Per Kg[:\s]*([\d.]+\s*kg)",
        "aW": r"aW[:\s]*([\d.]+)",
        "Viscosity": r"Viscosity[:\s]*([\d.]+\s*cps)",
        "Specific Gravity": r"Specific Gravity[:\s]*([\d.]+)",
        "Storage Instructions": r"Storage Instructions[:\s]*([\w\s,.-]+)",
        "Shelf Life": r"Shelf Life[:\s]*([\w\s,.-]+)",
        "Price per Unit": r"Price per Unit[:\s]*([\$€£]?\d+[.,]?\d*)",
        "Avg. Quantity per Order": r"Average Quantity per Order[:\s]*([\d.\s\w]+)"
    }
    for label, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            specs[label] = match.group(1).strip()
    return specs
