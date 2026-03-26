from fpdf import FPDF
from PIL import Image
from io import BytesIO
import tempfile

def generate_pdf_from_image(image_bytes):
    image = Image.open(BytesIO(image_bytes))

    # Convert ke RGB (biar aman untuk PDF)
    if image.mode != "RGB":
        image = image.convert("RGB")

    # temp_buffer = BytesIO()
    # image.save(temp_buffer, format="JPEG")
    # temp_buffer.seek(0)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        image.save(temp_file.name, format="JPEG")
        temp_path = temp_file.name

    pdf = FPDF(unit="mm", format="A4")
    pdf.add_page()

    # A4 size: 210 x 297 mm
    pdf.image(temp_path, x=0, y=0, w=210)

    # output = BytesIO()
    # pdf.output(output)
    # output.seek(0)

    # return output

    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return BytesIO(pdf_bytes)