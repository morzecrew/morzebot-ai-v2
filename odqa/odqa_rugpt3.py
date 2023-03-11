import ruprompts
from transformers import pipeline
from transformers import GPT2LMHeadModel, AutoTokenizer

from odqa.odqa import ODQA

model_id = "sberbank-ai/rugpt3large_based_on_gpt2"
class PretrainedLLM:
    def __init__(self, model_id):
        self.model_name = model_id

    def tokenizer(self):


model = GPT2LMHeadModel.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

context = """В 1997 году Шмидхубер и Сепп Хохрайтер опубликовали работу, описывающую рекуррентную нейронную сеть, которую авторы назвали «Долгая краткосрочная память». В 2015 году эта архитектура была использована в новой реализации распознавания речи в программном обеспечении компании Google для смартфонов.

Исследования Шмидхубера также включают в себя генерализации колмогоровской сложности и метрики «скорость важна» (Speed Prior), создание концепции Машины Гёделя.

В 2014 году Шмидхубер основал компанию Nnaisense для работы в сфере коммерческого применения технологий искусственного интеллекта в таких областях как финансы, тяжёлая промышленность и самоуправляемый автотранспорт. Сепп Хохрайтер и Яан Таллинн занимают в компании пост советников."""

ppln_qa = pipeline("text2text-generation-with-prompt", prompt="konodyuk/prompt_rugpt3large_qa_sberquad", model=model, tokenizer=tokenizer, device=0)
ppln_qa({"context": context, "question": "С кем Шмидхубер опубликовал работу?"})


class RuGPT3QA(ODQA):
    def __init__(self):
        super().__init__()
        pass

    def answer(self, context:str):
