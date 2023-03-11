import ruprompts
from transformers import pipeline
from transformers import GPT2LMHeadModel, AutoTokenizer

from odqa.odqa_base import ODQA


class PretrainedLLM:
    def __init__(self, model_path):
        self.model_name = model_path

    def tokenizer(self):
        try:
            tokenizer_model = AutoTokenizer.from_pretrained(self.model_name, local_files_only=True, )
        except:
            tokenizer_model = AutoTokenizer.from_pretrained(self.model_name)
        return tokenizer_model

    def model(self):
        try:
            model = GPT2LMHeadModel.from_pretrained(self.model_name, local_files_only=True, )
        except:
            model = GPT2LMHeadModel.from_pretrained(self.model_name)
        return model


class RuGPT3QA(ODQA):
    def __init__(self, model, tokenizer):
        super().__init__()
        self.ppln_qa = pipeline("text2text-generation-with-prompt", prompt="konodyuk/prompt_rugpt3large_qa_sberquad", model=model, tokenizer=tokenizer, device=0)

    def answer(self, context:str, question: str):
        return self.ppln_qa({"context": context, "question": question})


if __name__ == "__main__":
    text = "Трава зеленая"
    model_id = "sberbank-ai/rugpt3large_based_on_gpt2"
    q = "Зеленая ли трава?"
    llm = PretrainedLLM(model_id)
    tokenizer = llm.tokenizer()
    model = llm.model()
    odqa_model = RuGPT3QA(model, tokenizer)
    answer = odqa_model.answer(text, q)
    print(answer)
