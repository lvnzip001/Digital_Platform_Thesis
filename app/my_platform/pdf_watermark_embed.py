import sys
import PyPDF2
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import sys
sys.path.insert(0, 'c:/Django_3/Django_3.3/mysite')

def create_watermark(file_name, content):
    c = canvas.Canvas(file_name, pagesize=(30 * cm, 30 * cm))
    # Move the coordinate origin (the lower left of the coordinate system is(0,0))
    c.translate(50, 600)
    # Font Type and Size
    c.setFont("Helvetica", 30)
    # Colour
    #c.setFillColorRGB(255, 0, 0)
    c.setFillColorRGB(255, 255, 110)
    # Transparency
    c.setFillAlpha(0.5)
    # Draw a few texts, pay attention to the influence of coordinate system rotation

    c.drawString(2 * cm, 0 * cm, content)
    # Close and save the pdf file
    c.save()
    return file_name


def pdf_embed_watermark(pdf_file_in, watermarkInfo, pdf_file_out,tmp_file = "tmp.pdf"):
    pdf_file_mark = create_watermark(tmp_file, watermarkInfo)

    # Input file
    pdf_input = PyPDF2.PdfFileReader(open(pdf_file_in, 'rb'))
    # Read the watermark pdf file
    pdf_watermark = PyPDF2.PdfFileReader(open(pdf_file_mark, 'rb'))
    # Output file
    pdf_output = PyPDF2.PdfFileWriter()

    # Get the number of pages of the input pdf file
    pageNum = pdf_input.getNumPages()
    for i in range(pageNum):
        page = pdf_input.getPage(i)
        # Embed the watermark information on the last page
        if i == pageNum - 1:
            page.mergePage(pdf_watermark.getPage(0))
            page.compressContentStreams()  # Compressed content
        pdf_output.addPage(page)
    pdf_output.write(open(pdf_file_out, 'wb'))
    return("Water mark inserted successfully")



