from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import requests
from PIL import Image

# Initialize processor and model
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

# Load and preprocess image
url = "https://fki.tic.heia-fr.ch/static/img/a01-122-02.jpg"
image_file = requests.get(url, stream=True).raw
image = Image.open(image_file).convert("RGB")
pixel_values = processor(image, return_tensors="pt").pixel_values

# Generate text with increased max_new_tokens
generated_ids = model.generate(
    pixel_values,
    max_new_tokens=50,  # Adjust based on expected text length
    num_beams=4,         # Optional: improves quality
    early_stopping=True  # Optional: stops generation early if possible
)

# Decode the generated tokens to text
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

print("Generated Text:", generated_text)