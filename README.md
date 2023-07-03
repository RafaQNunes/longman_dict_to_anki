# longman_dict_to_anki
This a Python program that makes a web scrapping on Longman Dictionary Online (https://www.ldoceonline.com/) and extract, based on a listed parameters and words on a json file, all meanings and examples that is possible.

To use it, config 'ldoceonline_params.json' file, which has the followed parameters:

# How to execute:
- On Windows, execute the file 'exec_get_meanings.cmd', checking the files 'ldoceonline_params.json' and 'get_meanings_ldoceonline.py' are disposal.

# Required python modules:
- sys;
- os;
- time;
- requests;
- bs4;
- json;

# Optional python modules:
- eng_to_ipa (for complementary phonetic transcriptions);
- openai (for translations and sentences fields to fill if empty);
- deep_translator (for using Google Translator tool to translate sentences).

# Json parameters:
- **language_to_translate** (standard = "pt"): acronym of the language you want to translate. Check the list below to see which you can use or not. "pt" (Portuguese) is the standard;
- **flag_use_chatgpt** (standard = false): flag true/false to confirm if you want to use chatgpt for translating and getting examples. It spends api tokens;
- **openai_api_key**: openai api key to use chatgpt;
- **flag_fill_phonetic_transc** (standard = true): flag true/false to use eng_to_ipa module to fill the non-found phonetic transcriptions found from Longman Dictionary;
- **trans_word_method** (standard = "None"): choice the method to translate the sentences gotten from ldoceonline or chatgpt.
  - "chatgpt": use chatgpt (don't recommended, translator is enought. 'flag_use_chatgpt = True' is a must.);
  - "gtrans": use Google Translator package;
  - "None" (or other value): there won't be no translation of sentences;
- **fill_examples_chatgpt** (standard = "None"): sentences that was not filled with chatgpt
  - "phrases": you fill the phrase fill with one example with chatgpt if there is no other tool to use ('flag_use_chatgpt = True' is a must.;
  - "all": fill all examples fields with chat-gpt if necessary;
  - "None" (or other value): sentences won't be filled;
- **trans_examples_method** (standard = "None"):
  - "chatgpt": use chatgpt (recommended, but it spends tokens. 'flag_use_chatgpt = True' is a must.);
  - "gtrans": use Google Translator package.
  - "None" (or other value): sentences won't be translated;
- **images_per_noun**: it's numeric, and how many images will be downloadede bases on the word to be translated (if it's a noun);
- **words**: list of words that will be translated.

# Fields of the table:
- **Word**: the word name with the number if there is duplicates;
- **Translation**: the translation of the field 'Word', considering the context of the field 'Meaning';
- **Phonetic_Transcription**: the Phonetic Transcription of this word. The transcription must be between '/'. (Example: /laɪ/);
- **Meaning**: In original language, not translated, I want the Part of Speech between parenthesis in beggining and after the complete meaning of the word;
- **Phrase**: In original language, a phrase or sentence about the word, that helps to understand about its meaning. The word itself must be bold in html format;
- **Translation_Phrase**: the translation of the field 'Phrase'. The translated word itself must be bold in html format;
- **Example**: In original language, another phrase or sentence about the word, that helps to understand about its meaning. The word itself must be bold in html format;
- **Translation_Example**: the translation of the field 'Example'. The translated word itself must be bold in html format;
- **sPhrase**: empty;
- **sExample**: empty;
- **Image**: empty;
- **Tags**: the original language in upper case, and the Part of Speech in lower case. (Example: ENGLISH adjective).


# Anki model:
- Check the anki model to use with the .csv output for the words;

# List of languages to translate:
'language' : 'acronym'
- 'afrikaans': 'af',
- 'albanian': 'sq',
- 'amharic': 'am',
- 'arabic': 'ar',
- 'armenian': 'hy',
- 'assamese': 'as',
- 'aymara': 'ay',
- 'azerbaijani': 'az',
- 'bambara': 'bm',
- 'basque': 'eu',
- 'belarusian': 'be',
- 'bengali': 'bn',
- 'bhojpuri': 'bho',
- 'bosnian': 'bs',
- 'bulgarian': 'bg',
- 'catalan': 'ca',
- 'cebuano': 'ceb',
- 'chichewa': 'ny',
- 'chinese (simplified)': 'zh-CN',
- 'chinese (traditional)': 'zh-TW',
- 'corsican': 'co',
- 'croatian': 'hr',
- 'czech': 'cs',
- 'danish': 'da',
- 'dhivehi': 'dv',
- 'dogri': 'doi',
- 'dutch': 'nl',
- 'english': 'en',
- 'esperanto': 'eo',
- 'estonian': 'et',
- 'ewe': 'ee',
- 'filipino': 'tl',
- 'finnish': 'fi',
- 'french': 'fr',
- 'frisian': 'fy',
- 'galician': 'gl',
- 'georgian': 'ka',
- 'german': 'de',
- 'greek': 'el',
- 'guarani': 'gn',
- 'gujarati': 'gu',
- 'haitian creole': 'ht',
- 'hausa': 'ha',
- 'hawaiian': 'haw',
- 'hebrew': 'iw',
- 'hindi': 'hi',
- 'hmong': 'hmn',
- 'hungarian': 'hu',
- 'icelandic': 'is',
- 'igbo': 'ig',
- 'ilocano': 'ilo',
- 'indonesian': 'id',
- 'irish': 'ga',
- 'italian': 'it',
- 'japanese': 'ja',
- 'javanese': 'jw',
- 'kannada': 'kn',
- 'kazakh': 'kk',
- 'khmer': 'km',
- 'kinyarwanda': 'rw',
- 'konkani': 'gom',
- 'korean': 'ko',
- 'krio': 'kri',
- 'kurdish (kurmanji)': 'ku',
- 'kurdish (sorani)': 'ckb',
- 'kyrgyz': 'ky',
- 'lao': 'lo',
- 'latin': 'la',
- 'latvian': 'lv',
- 'lingala': 'ln',
- 'lithuanian': 'lt',
- 'luganda': 'lg',
- 'luxembourgish': 'lb',
- 'macedonian': 'mk',
- 'maithili': 'mai',
- 'malagasy': 'mg',
- 'malay': 'ms',
- 'malayalam': 'ml',
- 'maltese': 'mt',
- 'maori': 'mi',
- 'marathi': 'mr',
- 'meiteilon (manipuri)': 'mni-Mtei',
- 'mizo': 'lus',
- 'mongolian': 'mn',
- 'myanmar': 'my',
- 'nepali': 'ne',
- 'norwegian': 'no',
- 'odia (oriya)': 'or',
- 'oromo': 'om',
- 'pashto': 'ps',
- 'persian': 'fa',
- 'polish': 'pl',
- 'portuguese': 'pt',
- 'punjabi': 'pa',
- 'quechua': 'qu',
- 'romanian': 'ro',
- 'russian': 'ru',
- 'samoan': 'sm',
- 'sanskrit': 'sa',
- 'scots gaelic': 'gd',
- 'sepedi': 'nso',
- 'serbian': 'sr',
- 'sesotho': 'st',
- 'shona': 'sn',
- 'sindhi': 'sd',
- 'sinhala': 'si',
- 'slovak': 'sk',
- 'slovenian': 'sl',
- 'somali': 'so',
- 'spanish': 'es',
- 'sundanese': 'su',
- 'swahili': 'sw',
- 'swedish': 'sv',
- 'tajik': 'tg',
- 'tamil': 'ta',
- 'tatar': 'tt',
- 'telugu': 'te',
- 'thai': 'th',
- 'tigrinya': 'ti',
- 'tsonga': 'ts',
- 'turkish': 'tr',
- 'turkmen': 'tk',
- 'twi': 'ak',
- 'ukrainian': 'uk',
- 'urdu': 'ur',
- 'uyghur': 'ug',
- 'uzbek': 'uz',
- 'vietnamese': 'vi',
- 'welsh': 'cy',
- 'xhosa': 'xh',
- 'yiddish': 'yi',
- 'yoruba': 'yo',
- 'zulu': 'zu'
