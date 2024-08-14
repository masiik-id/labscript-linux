import cv2
from pyzbar.pyzbar import decode
import numpy as np

def correct_skew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    
    if lines is not None:
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi
            angles.append(angle)
        median_angle = np.median(angles)
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated
    return image

def read_barcodes(image_path):
    img = cv2.imread(image_path)
    img = correct_skew(img)
    barcodes = decode(img)
    barcode_data = []

    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        barcode_data.append((barcode_info, barcode_type))
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f'{barcode_info} ({barcode_type})', (x, y - 10), font, 0.5, (0, 255, 0), 2)

    cv2.imshow('Image with Barcodes', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return barcode_data

# Path to the uploaded image
image_path = 'barcode-miring.jpeg'
barcodes = read_barcodes(image_path)

# Print the output
for info, btype in barcodes:
    print(f'Barcode: {info}, Type: {btype}')
