import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class ReportGenerator:
    def __init__(self):
        model_name = "microsoft/phi-2"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            device_map="cpu"
        )

    def generate_report(self, query, retrieved_chunks):
        context = "\n\n".join([chunk for _, chunk in retrieved_chunks])

        prompt = f"""
You are a financial analyst.

Using ONLY the context provided below, generate a structured financial report.

Structure:
1. Revenue Analysis
2. Profitability
3. Balance Sheet Strength
4. Cash Flow
5. Risk Signals
6. Overall Assessment

Context:
{context}

Instruction:
{query}

Report:
"""

        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=400,
                temperature=0.2,
                do_sample=False
            )

        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result
