## New Relevance Feature -----------------------------------------------------------------
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertJapaneseTokenizer, BertModel

model_name = "tohoku-nlp/bert-base-japanese"
tokenizer = BertJapaneseTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)
model = BertModel.from_pretrained(model_name)


def get_word_embedding(word: str):
    # Tokenize the word and get the model outputs
    inputs = tokenizer(word, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the embedding (mean pooling of the last hidden state)
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding


def caculate_by_relevance(keyword: str, items: list[dict]):
    keyword_embedding = get_word_embedding(keyword).reshape(1, -1)
    relevance = "relevanceScore"
    for i, item in enumerate(items):
        catchcopy_embedding = get_word_embedding(item["catchcopy"]).reshape(1, -1)
        similarity = cosine_similarity(keyword_embedding, catchcopy_embedding)[0][0]  # Cosine similarity
        items[i][relevance] = similarity.item()

    return items
