from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document
from ai_nlp import smart_keyword_check, extract_specifications

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

KEYWORDS = [
    "CAS", "SDS", "Composition", "D4", "D5", "pH", "Appearance", "Color", "Odor",
    "CO2 Emissions Per Gram", "CO2 Per Kg", "aW", "Viscosity", "cps", "Specific Gravity",
    "Storage Instructions", "Shelf Life", "Price per Unit", "Average Quantity per Order",
    "Ingredient Statement", "Natural Rubber", "Fragrance", "Preservatives", "Animal-Derived",
    "Source", "Claims", "Dyes", "Metals", "Prop 65 Materials Present", "Walmart Clean",
    "EU Fragrance Allergen Statement", "Product Origin", "Palm Oil Statement", "Vegan Statement",
    "Manufacturing Geo Location", "GMO/non-GMO", "Marketing Sales Sheet", "Animal Testing Statement",
    "Prop 65 Compliancy", "Allergen Statement", "Global Compliance", "COA Specs", "1,4-Dioxane",
    "Heavy metal", "PFAs", "BSE/TSE Statement", "Nanomaterial", "Microplastics", "CMR Statement",
    "Phthalates", "VOC Statement"
]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    return " ".join([page.extract_text() or "" for page in reader.pages])

def extract_text_from_docx(filepath):
    doc = Document(filepath)
    return " ".join([para.text for para in doc.paragraphs])

def extract_text(filepath):
    if filepath.endswith('.pdf'):
        return extract_text_from_pdf(filepath)
    elif filepath.endswith('.docx'):
        return extract_text_from_docx(filepath)
    elif filepath.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    return ""

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    specs = {}
    if request.method == 'POST':
        files = request.files.getlist('files')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                text = extract_text(filepath)
                _, missing_keywords = smart_keyword_check(text, KEYWORDS)
                extracted_specs = extract_specifications(text)
                results[filename] = missing_keywords
                specs[filename] = extracted_specs
        return render_template('index.html', results=results, specs=specs)
    return render_template('index.html', results=None, specs=None)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
