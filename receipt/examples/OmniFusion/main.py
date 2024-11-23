import torch
from PIL import Image
from transformers import AutoTokenizer, AutoModelForCausalLM
from urllib.request import urlopen
from huggingface_hub import hf_hub_download

# Определяем устройство
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
PROMPT = "This is a dialog with AI assistant.\n"

# Загрузка токенизатора и модели
tokenizer = AutoTokenizer.from_pretrained("AIRI-Institute/OmniFusion", subfolder="OmniMistral-v1_1/tokenizer", use_fast=False)
model = AutoModelForCausalLM.from_pretrained(
    "AIRI-Institute/OmniFusion", subfolder="OmniMistral-v1_1/tuned-model", torch_dtype=torch.float16 if DEVICE == "mps" else torch.bfloat16
).to(DEVICE)

# Загрузка дополнительных ресурсов
projection_path = hf_hub_download(repo_id="AIRI-Institute/OmniFusion", filename="OmniMistral-v1_1/projection.pt")
special_embs_path = hf_hub_download(repo_id="AIRI-Institute/OmniFusion", filename="OmniMistral-v1_1/special_embeddings.pt")
projection = torch.load(projection_path, map_location=DEVICE)
special_embs = torch.load(special_embs_path, map_location=DEVICE)

# Загрузка и настройка CLIP-модели
from models import CLIPVisionTower

clip = CLIPVisionTower("openai/clip-vit-large-patch14-336")
clip.load_model()
clip.to(device=DEVICE, dtype=torch.float16 if DEVICE == "mps" else torch.bfloat16)

# Функция для генерации ответа
def gen_answer(model, tokenizer, clip, projection, query, special_embs, image=None):
    bad_words_ids = tokenizer(["\n", "</s>", ":"], add_special_tokens=False).input_ids + [[13]]
    gen_params = {
        "do_sample": False,
        "max_new_tokens": 50,
        "early_stopping": True,
        "num_beams": 3,
        "repetition_penalty": 1.0,
        "remove_invalid_values": True,
        "eos_token_id": 2,
        "pad_token_id": 2,
        "forced_eos_token_id": 2,
        "use_cache": True,
        "no_repeat_ngram_size": 4,
        "bad_words_ids": bad_words_ids,
        "num_return_sequences": 1,
    }
    with torch.no_grad():
        image_features = clip.image_processor(image, return_tensors='pt').to(DEVICE)
        image_embedding = clip(image_features['pixel_values']).to(DEVICE)

        projected_vision_embeddings = projection(image_embedding).to(DEVICE)
        prompt_ids = tokenizer.encode(f"{PROMPT}", add_special_tokens=False, return_tensors="pt").to(DEVICE)
        question_ids = tokenizer.encode(query, add_special_tokens=False, return_tensors="pt").to(DEVICE)

        prompt_embeddings = model.model.embed_tokens(prompt_ids)
        question_embeddings = model.model.embed_tokens(question_ids)

        embeddings = torch.cat(
            [
                prompt_embeddings,
                special_embs['SOI'][None, None, ...],
                projected_vision_embeddings,
                special_embs['EOI'][None, None, ...],
                special_embs['USER'][None, None, ...],
                question_embeddings,
                special_embs['BOT'][None, None, ...]
            ],
            dim=1,
        ).to(DEVICE)
        out = model.generate(inputs_embeds=embeddings, **gen_params)
    out = out[:, 1:]
    generated_texts = tokenizer.batch_decode(out)[0]
    return generated_texts

# Загрузка изображения
img_url = "https://i.pinimg.com/originals/32/c7/81/32c78115cb47fd4825e6907a83b7afff.jpg"
question = "What is the sky color on this image?"
img = Image.open(urlopen(img_url))

# Генерация ответа
answer = gen_answer(
    model,
    tokenizer,
    clip,
    projection,
    query=question,
    special_embs=special_embs,
    image=img
)

img.show()
print(question)
print(answer)
