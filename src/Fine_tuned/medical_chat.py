from simpletransformers.t5 import T5Model
import torch
from dotenv import load_dotenv 
from langsmith import traceable

load_dotenv()

class MedicalChat:
    def __init__(self, model_path):
        use_cuda = torch.cuda.is_available()
        
        self.model = T5Model(
            "mt5",
            model_path,
            use_cuda=use_cuda  #
        )
        self.tokenizer = self.model.tokenizer
        self.hf_model = self.model.model

    @traceable
    def predict(self, text, max_length=256, do_sample=True, top_k=50, top_p=0.95, temperature=0.9):
        device = self.hf_model.device
        inputs = self.tokenizer(text, return_tensors="pt").to(device)
        
        output_ids = self.hf_model.generate(
            inputs.input_ids,
            max_length=max_length,
            do_sample=do_sample,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
        )
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

