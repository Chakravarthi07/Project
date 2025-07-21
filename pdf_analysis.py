import fitz  # PyMuPDF
import os
import json
import re

pdf_path = r"C:\Users\chakr\Downloads\IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"
doc = fitz.open(pdf_path)
os.makedirs("images", exist_ok=True)

final_data = []

for page_number, page in enumerate(doc, start=1):
    print(f"\nProcessing Page {page_number}")

    # Extract text and split into individual questions
    full_text = page.get_text().strip()

    # Use regex to find each question (start with number + dot)
    question_blocks = re.split(r'\n?\s*\d+\.\s+', full_text)
    question_blocks = [q.strip() for q in question_blocks if q.strip()]

    # Extract images from the page
    images = []
    for img_index, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_path = f"images/page{page_number}_image{img_index}.{image_ext}"
        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)
        images.append(image_path)

    # Now match questions with images using pattern: 1 question image + 4 option images
    i = 0  # image index
    for q_index, question_text in enumerate(question_blocks):
        question_data = {
            "question": question_text,
            "images": None,
            "option_images": []
        }

        if i < len(images):
            question_data["images"] = images[i]
            i += 1

        for _ in range(4):
            if i < len(images):
                question_data["option_images"].append(images[i])
                i += 1

        final_data.append(question_data)

# Save final structured data
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=2, ensure_ascii=False)

print("✅ Saved as output.json")
