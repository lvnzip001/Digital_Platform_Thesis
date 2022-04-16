import PyPDF2
import sys


def pdf_extract_watermark(file_watermarked):
    # Input file
    pdf_input = PyPDF2.PdfFileReader(open(file_watermarked, 'rb'))
    pageNum = pdf_input.getNumPages()
    extractedText = pdf_input.getPage(pageNum - 1).extractText()
    watermarkInfo_list = extractedText.split()

    def listToString(watermark_list):
        # initialize an empty string
        str1 = ""
        return (str1.join(watermark_list))
    result = listToString(watermarkInfo_list)
    
    try:
        return result
    except:
        return('No watermark imformation found, please make sure you have the correct file')
