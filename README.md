# english-search-engine-for-rakuten-ichiba

## How to Use Translator

1. Example One
```python

from translator import translator

text = "Bank"
translated_text = translator.translate(text, translator.Lang.EN, translator.Lang.JA)
print(translated_text)
```
Output:  `銀行`

2. Example Two
```python

from translator import translate, Lang

text = "Bank"
translated_text = translate(text, Lang.EN, Lang.JA)
print(translated_text)
```
Output:  `銀行`

3. Example Three (Batch)
```python

from translator import translate_batch, Lang


list_of_texts = ["Child", "Parent", "School", "University"]
translated_texts = translate_batch(list_of_texts, Lang.EN, Lang.JA)

print(translated_texts)
```
Output: `['チャイルド', '親', '学校', '大学']`