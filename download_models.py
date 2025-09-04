from transformers import AutoProcessor, AutoModelForZeroShotImageClassification

processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch16")
processor.save_pretrained("./clip-vit")

model = AutoModelForZeroShotImageClassification.from_pretrained("openai/clip-vit-base-patch16")
model.save_pretrained("./clip-vit")
