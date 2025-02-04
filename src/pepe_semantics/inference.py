import torch
from transformers import AutoTokenizer
from pathlib import Path
from pepe_semantics.config import BERTWEET_WEIGHTS_PATHS, INDEX_DIR
from pepe_semantics.model.index import GIFIndex
from pepe_semantics.model.tweet_encoder import (TEXT_ENCODER_MODEL_NAME,
                                                TweetEncoder)


class InferenceModel:
    # TODO: add moving to cuda if available: weights and inputs
    def __init__(self, tweet_encoder_weights_path):
        self.tweet_encoder = TweetEncoder.load(tweet_encoder_weights_path) 
        self._text_tokenizer = AutoTokenizer.from_pretrained(TEXT_ENCODER_MODEL_NAME)

    def tokenize_text(self, text):
        return self._text_tokenizer([text], return_tensors="pt")["input_ids"]

    def embed_text(self, text):
        with torch.no_grad():
            input_ids = self.tokenize_text(text)
            return self.tweet_encoder(input_ids)[0].cpu().detach().numpy()


def get_giphy_links(
    input_text,
    k=5,
    index_dir=Path("/app/pepe_semantics/index/pepe_index/"), #INDEX_DIR,
    #index_dir = Path("/Users/jobquiroz/OneDrive/MachineLearningHero/PEPE/PEPE-Semantics/pepe_semantics/index/pepe_index"),
    bertweet_weights_fpath=Path("/app/pepe_semantics/model/bertweet_weights.pth") #BERTWEET_WEIGHTS_PATHS[1],
    #bertweet_weights_fpath = Path("/Users/jobquiroz/OneDrive/MachineLearningHero/PEPE/PEPE-Semantics/pepe_semantics/model/bertweet_weights.pth")
):
    model = InferenceModel(bertweet_weights_fpath)
    index = GIFIndex.load(index_dir)
    text_emb = model.embed_text(input_text)
    return index.get_giphy_links(text_emb, k=k)
