import cv2
from pyzbar.pyzbar import decode
import numpy as np

def correct_skew(image, contour):
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)  # np.int0 should be np.int32

    width = int(rect[1][0])
    height = int(rect[1][1])

    src_pts = box.astype("float32")
    dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")

    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(image, M, (width, height))
    return warped

def read_barcodes(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200, 255)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    barcode_data = []

    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Filter out small contours
            try:
                rotated_img = correct_skew(img, contour)
                barcodes = decode(rotated_img)
                if barcodes:
                    for barcode in barcodes:
                        barcode_info = barcode.data.decode('utf-8')
                        barcode_type = barcode.type
                        barcode_data.append((barcode_info, barcode_type))
                        print(f'Barcode: {barcode_info}, Type: {barcode_type}')

                        x, y, w, h = barcode.rect
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(img, f'{barcode_info} ({barcode_type})', (x, y - 10), font, 0.5, (0, 255, 0), 2)
                else:
                    print("No barcodes found in the corrected image.")
            except Exception as e:
                print(f"Error processing contour: {e}")

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
