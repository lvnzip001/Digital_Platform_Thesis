from pathlib import Path
from image_watermark_embed import watermark_embed
from image_watermark_extract import watermark_extract

input_dir = Path.cwd()/"media"
print('This:',input_dir)
files_image = list(input_dir.rglob("*.jpg"))
image_1 = files_image[1]
#for image_path in files_image:
#    print(image_path)
print(image_1)
#print(image_1.__dict__)

#image_path = files_image[1]
#watermark_embed('./my_test/Pharmacists.jpg', 'zluvuno@gmail.com-JohnBezo@yahoo.com-2232', './my_test/Pharmacists2.jpg')
watermark_extract('./my_test/Pharmacists2.jpg')



