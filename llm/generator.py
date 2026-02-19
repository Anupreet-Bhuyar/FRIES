from transformers import pipeline


class ReportGenerator:
    def __init__(self):
        self.generator = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            device=-1
        )

    def generate_report(self, query, retrieved_chunks):
        context = "\n\n".join([chunk for _, chunk in retrieved_chunks])

        prompt = f"""
You are a professional financial analyst.

Using ONLY the context below, generate a structured financial report.

Structure your response clearly with these sections:

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

        output = self.generator(
            prompt,
            max_new_tokens=400,
            temperature=0.2,
            do_sample=False
        )

        return output[0]["generated_text"]
