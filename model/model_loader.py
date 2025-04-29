from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from functools import lru_cache
import os
from config.config import MODEL_TYPE, MODEL_PATH, OPENCHAT_MODEL

class HFWrapper:
    def __init__(self, pipe):
        self.pipe = pipe
    def generate(self, prompt: str) -> str:
        out = self.pipe(prompt, max_new_tokens=512)
        return out[0].get("generated_text", "").strip()

def _load_openchat():
    model_name = "openchat/openchat-3.5-0106"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    if torch.cuda.is_available():
        # GPU disponível: use float16 + device_map automático
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            trust_remote_code=True,
            device_map="auto"
        )
    else:
        # CPU puro: carregue tudo em float32 e SEM device_map
        model = AutoModelForCausalLM.from_pretrained(model_name)
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            trust_remote_code=True
        )

    return HFWrapper(pipe)

def _load_gpt4all():
    from gpt4all import GPT4All
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"GPT4All model not found at {MODEL_PATH}")
    return GPT4All(MODEL_PATH)

@lru_cache(maxsize=1)
def load_model():
    mt = MODEL_TYPE.lower()
    if mt == "gpt4all":
        return _load_gpt4all()
    elif mt == "openchat":
        return _load_openchat()
    else:
        raise ValueError(f"Unknown MODEL_TYPE: {MODEL_TYPE}")
