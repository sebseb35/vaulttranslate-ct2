import ctranslate2
from transformers import AutoTokenizer

MODEL_DIR = "/home/sebseb/models/opus-mt-en-fr-ct2"
TOKENIZER_DIR = "/home/sebseb/models/opus-mt-en-fr-hf"

translator = ctranslate2.Translator(MODEL_DIR, device="cpu")
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_DIR)

source_text = "Hello world. This is a secure local translation test."

source_tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(source_text))
results = translator.translate_batch([source_tokens])
target_tokens = results[0].hypotheses[0]
translated = tokenizer.decode(tokenizer.convert_tokens_to_ids(target_tokens), skip_special_tokens=True)

print("SOURCE    :", source_text)
print("TRANSLATED:", translated)