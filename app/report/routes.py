from flask import Blueprint, request, jsonify, send_file, render_template
import base64
from io import BytesIO
from weasyprint import HTML
from playwright.sync_api import sync_playwright

from app.utils.pdf_generator import generate_pdf_from_image

report_blueprint = Blueprint('report', __name__,template_folder="../../templates")

@report_blueprint.route('/pdf', methods=['POST'])
def generate_pdf_method_image():
    try:
        data = request.json

        if "image" not in data:
            return jsonify({"error": "No image provided"}), 400

        base64_image = data["image"]

        # remove prefix: data:image/png;base64,...
        if "," in base64_image:
            base64_image = base64_image.split(",")[1]

        image_bytes = base64.b64decode(base64_image)

        pdf_buffer = generate_pdf_from_image(image_bytes)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="report.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@report_blueprint.route('/pdf-method2', methods=['POST'])
def generate_pdf_method_template():
    data = request.get_json()
    
    html_string = render_template(
        "report.html",
        date = data.get("date"),
        location = data.get("location"),
        inspector = data.get("inspector"),
        measurements = data.get("measurements"),
        notes = data.get("notes")
    )

    pdf= HTML(string=html_string).write_pdf()

    return send_file(
        BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name="report.pdf"
    )


@report_blueprint.route('/pdf-method3', methods=['POST'])
def generate_pdf_method_headless():
    data = request.get_json()

    url = data.get('url')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, wait_until='networkidle')

        page.wait_for_selector('#report')

        pdf_bytes = page.pdf(
            format= 'A4',
            print_background=True,
            margin={
                "top" : '20px',
                'bottom' : '20px',
                'left' : '20px',
                'right' : '20px',
            }
        )

        browser.close()

        return send_file(
            BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='report.pdf'
        )