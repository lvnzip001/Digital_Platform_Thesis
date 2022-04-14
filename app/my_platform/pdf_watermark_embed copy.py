import sys
import PyPDF2
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


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


def embed_watermark(pdf_file_in, tmp_file, watermarkInfo, pdf_file_out):
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


print('CLI inputs below')
if __name__ == '__main__':
    #use for CLI arguments
    #pdf_file = sys.argv[1]
    #tmp_file = sys.argv[2]
    #watermarkInfo = sys.argv[3]
    #file_out = sys.argv[4]

    tmp_file = "tmp.pdf"
    resourceowner = "zluvuno@gmail.com"
    newuser = '-JohnBezo@yahoo.com' 
    watermarkInfo = resourceowner+newuser
    print(watermarkInfo)
    pdf_file = "./out.pdf"
    file_out = "./out2.pdf"

    embed_watermark(pdf_file, tmp_file, watermarkInfo, file_out)



