import os
from gpt4all import GPT4All
from transformers import AutoModelForCausalLM, AutoTokenizer

class ModelLoader:
    def __init__(self):
        self.model_type = os.getenv("MODEL_TYPE", "gpt4all")  # Default: GPT4All
        self.model = self._load_model()

    def _load_model(self):
        if self.model_type == "gpt4all":
            return GPT4All(os.getenv("MODEL_PATH"))
        elif self.model_type == "openchat":
            return OpenChatModel()
        else:
            raise ValueError(f"Modelo não suportado: {self.model_type}")

    def generate(self, prompt):
        return self.model.generate(prompt)

class OpenChatModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("openchat/openchat-3.5")
        self.model = AutoModelForCausalLM.from_pretrained("openchat/openchat-3.5")

    def generate(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=200)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)