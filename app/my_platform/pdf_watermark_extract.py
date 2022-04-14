import PyPDF2
import sys


def pdf_extract_watermark(file_watermarked):
    # Input file
    pdf_input = PyPDF2.PdfFileReader(open(file_watermarked, 'rb'))
    pageNum = pdf_input.getNumPages()
    extractedText = pdf_input.getPage(pageNum - 1).extractText()
    watermarkInfo = extractedText.split()[-1]
    result = watermarkInfo.split("-")     # split into 3 variables if we have a resource ID 
    try:
        return result

    except: 
        return('No watermark imformation found, please make sure you have the correct file')


