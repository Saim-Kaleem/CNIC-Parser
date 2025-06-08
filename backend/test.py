import easyocr

image_path = 'test1.png'
reader = easyocr.Reader(['en'], gpu=False)
result = reader.readtext(image_path, detail=1)
print(result)