class Preprocessing:
    def __init__(self):
        pass

    def preprocessing(self, text):
        raise NotImplementedError

    def __tokenizer_sent(self, text: str):  # text = "abc bca ass" --> ["abc", "bca", "ass"]
        raise NotImplementedError

    def __tokenizer_intent(self,
                           text: list):  # text = ["abc abc", "ass ssa", "hui hui"] -->[["abc", "abc"],["ass", "ssa"],["hui", "hui"]]
        raise NotImplementedError

    def __word_emb(self,
                   text: list):  # text = ["hui", "moy"] --> [array([0.12, 0.15, 0.45, ... N=300]), array([0.34, 0.15, 0.05, ... N=300])]
        raise NotImplementedError

    def __sent_emb(self, text_emb):
        raise NotImplementedError
