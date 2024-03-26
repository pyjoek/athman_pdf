from flask import Flask, request, jsonify
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fpdf import FPDF
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def convert_to(input_file, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    with open(input_file, 'rb') as file:
        # content = file.read().decode('utf-8')  # Decode binary content to text
        content = file.read().decode('latin-1') 
    c.setFont("Helvetica", 12)
    y = 750  # Initial y-coordinate
    lines = content.split('\n')
    for line in lines:
        c.drawString(100, y, line)
        y -= 15  # Move to the next line
        if y < 50:  # Check if at end of page
            c.showPage()  # Start a new page
            y = 750  # Reset y-coordinate
    c.save()

@app.route('/convert-to-pdf', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    # if file:
    #     pdf = FPDF()
    #     pdf.add_page()
    #     pdf.set_font("Arial", size=12)
    #     pdf.cell(200, 10, txt="Converted to PDF", ln=True, align="C")
    #     pdf.output("output.pdf")

    if file:
        filename = file.filename
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename.split('.')[0] + '.pdf')
        file.save(input_path)
        convert_to(input_path, output_path)

        return jsonify({'success': 'File converted to PDF successfully'})

if __name__ == '__main__':
    app.run(debug=True)
