
from image_watermark_embed import watermark_embed
from image_watermark_extract import watermark_extract


import sys
sys.path.insert(0,'C:/Django_3/Django_3.3/mysite/mytest')

filePath = "mytest/Proof_of_Registration_ZLuvuno_qX2gRS6.pdf"                                     # What would be nice would be to get these as an input. Thus I am thinking I need to use the get function
watermarkInfo = "zluvuno@gmail.com-JohnBezo@yahoo.com-2232"
outPath = "/Proof_of_Registration_ZLuvuno.pdf"

watermark_embed(filePath, watermarkInfo, outPath)
watermark_extract(outPath)
