import re
import cv2
import os
import uuid

PII_PATTERNS = {
    "aadhaar": r"\b\d{4}\s\d{4}\s\d{4}\b",
    "phone": r"\b[6-9]\d{9}\b",
    "dob": r"\b\d{4}-\d{2}-\d{2}\b|\b\d{2}[/-]\d{2}[/-]\d{4}\b",
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
}


def is_pii(text):
    for pattern in PII_PATTERNS.values():
        if re.search(pattern, text):
            return True
    return False


def mask_pii(image_path, data):
    image = cv2.imread(image_path)
    n = len(data['text'])

    pii_keywords = ['नाम', 'Name', 'Address', 'पता',
                    'DOB', 'जन्म', 'Date', 'Phone', 'Email']
    lines_to_mask = set()

    for i in range(n):
        text = data['text'][i].strip()
        if any(kw.lower() in text.lower() for kw in pii_keywords):
            lines_to_mask.add(data['line_num'][i])
        if is_pii(text):
            lines_to_mask.add(data['line_num'][i])

    for i in range(n):
        if data['line_num'][i] in lines_to_mask and int(data['conf'][i]) > 60:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)

    os.makedirs("output", exist_ok=True)
    output_path = f"output/masked_{uuid.uuid4()}.png"
    cv2.imwrite(output_path, image)
    return output_path
