from enum import Enum
from typing import Iterable

from transformers import MBartForConditionalGeneration, MBart50TokenizerFast


model_name = "facebook/mbart-large-50-many-to-many-mmt"
model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer = MBart50TokenizerFast.from_pretrained(
    model_name, clean_up_tokenization_spaces=True
)


class Lang(Enum):
    JA = "ja_XX"
    EN = "en_XX"


def translate(text: str, src_lang: Lang, tgt_lang: Lang):
    tokenizer.src_lang = src_lang.value
    bos_token_id = tokenizer.lang_code_to_id[tgt_lang.value]

    encoded = tokenizer(text, return_tensors="pt")

    generated_tokens = model.generate(
        **encoded, forced_bos_token_id=bos_token_id
    )

    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)


def translate_batch(texts: Iterable[str], src_lang: Lang, tgt_lang: Lang):
    tokenizer.src_lang = src_lang.value
    bos_token_id = tokenizer.lang_code_to_id[tgt_lang.value]

    translated_texts = []

    for text in texts:
        encoded = tokenizer(text, return_tensors="pt")
        generated_tokens = model.generate(
            **encoded, forced_bos_token_id=bos_token_id
        )
        translated_texts.append(
            tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        )

    return translated_texts
