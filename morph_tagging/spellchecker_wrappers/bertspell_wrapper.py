from spellchecker_wrapper import SpellSheckerWrapper
# Импортируем библиотеки
from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast

# Зададим название выбронной модели из хаба
MODEL_NAME = 'UrukHan/t5-russian-spell'
MAX_INPUT = 256

# Загрузка модели и токенизатора
tokenizer = T5TokenizerFast.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Входные данные (можно массив фраз или текст)
input_sequences = ['сеглдыя хорош ден',
                   'когд а вы прдет к нам в госи']  # или можно использовать одиночные фразы:  input_sequences = 'сеглдыя хорош ден'

task_prefix = "Spell correct: "  # Токенизирование данных
if type(input_sequences) != list: input_sequences = [input_sequences]
encoded = tokenizer(
    [task_prefix + sequence for sequence in input_sequences],
    padding="longest",
    max_length=MAX_INPUT,
    truncation=True,
    return_tensors="pt",
)
# import torch
# if torch.cuda.is_available():
#   if use_gpu == 0:
#     device = torch.device('cuda')
#   else:
#     device = torch.device('cuda:' + use_gpu)
# else:
#   device = torch.device('cpu')


# print(encoded.to(device))
predicts = model.generate(**encoded.data)  # # Прогнозирование

print(tokenizer.batch_decode(predicts, skip_special_tokens=True))


class T5BERTModelWrapper:
    def __init__(self, model=model, tokenizer=tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def correct(self, sentense):
        task_prefix = "Spell correct: "  # Токенизирование данных
        # if type(sentense) != list: input_sequences = [sentense]
        if isinstance(sentense, list):
            encoded = tokenizer(
                [task_prefix + sequence for sequence in sentense],
                padding="longest",
                max_length=256,
                truncation=True,
                return_tensors="pt",
            )
        elif isinstance(sentense, str):
            encoded = tokenizer(
                task_prefix + sentense,
                padding="longest",
                max_length=256,
                truncation=True,
                return_tensors="pt",
            )
        predicts = self.model.generate(**encoded.data)  # # Прогнозирование
        # self.model.generate(**encoded.data)
        return tokenizer.batch_decode(predicts, skip_special_tokens=True)  # Декодируем данные


md = T5BERTModelWrapper(model, tokenizer)


class BERTSpellWarapper(SpellSheckerWrapper):
    def __init__(self, model=md):
        super().__init__(md)

    def correct(self, sentence):
        return self.model.correct(sentence)


# import time
#
# start = time.time()
# print(BERTSpellWarapper().correct('сгодны все лк')[0])
# print(time.time() - start)
