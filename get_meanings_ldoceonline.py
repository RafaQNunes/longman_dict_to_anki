#!/usr/bin/env python
# coding: utf-8

# # Packages
# ### Verify if all packages are OK

# In[153]:


# Function to check and load libraries
def import_and_check(library: str, sublibrary: str = '', librename: str = '', import_module: bool = False):

    # Organizing parameters
    if librename != '': _librename = ' as ' + librename.strip()
    else: _librename = ''
    
    if sublibrary == '': text_execution = f'import {library}{_librename}'
    else: text_execution = f'from {library} import {sublibrary}{_librename}'

    if librename != '': final = librename.strip()
    elif sublibrary != '': final = sublibrary.strip()
    else: final = library.strip()
    
    # Execute check
    try:
        exec(text_execution) # Import the module just inside the function
        if import_module:
            exec(f'globals()[final] = {final}') # Move parameter to use if import_module == True
            print(f"Library {library} is installed and imported.")
        else:
            print(f"Library {library} is installed, but it is not imported.")
        return True
    except ImportError:
        print(f"Library {library} not is installed.")
        return False


# In[154]:


# Check if a package is imported
def is_package_imported(package_name):
    return package_name in sys.modules


# In[155]:


if 'openai' in globals(): del openai # delete openai package if it's loaded

# Load and check libraries
if import_and_check('sys', import_module = True) and     import_and_check('os', import_module = True) and     import_and_check('time', import_module = True) and     import_and_check('requests', import_module = True) and     import_and_check('bs4','BeautifulSoup', import_module = True) and     import_and_check('json', import_module = True)         : print('All necessary packages were imported')
else:
    print('Not all packages were imported. Finish the application.')
    time.sleep(5)
    exit()


# In[156]:


print('\nStart the application for getting meanings from ldoceonline.com with Python. By Rafael de Queiroz Nunes.')


# # Variables

# In[157]:


########################################
### Model variables

# Open the JSON file
if 'data_json' in globals(): del data_json # delete openai package if it's loaded
try:
    with open('ldoceonline_params.json', 'r') as file_json:
        data_json = json.load(file_json)
except FileNotFoundError:
    print('\nThe file ldoceonline_params.json is not found in the same path as application. Application will be closed.')
    time.sleep(5)
    exit()


# In[158]:


# Access the data
try:
    language_to_translate = data_json['language_to_translate']

    if type(language_to_translate) != str:
        raise TypeError("Key 'language_to_translate' is not in correct type 'str'.")
    # Language to translate. If None, you won't translate anything.
    # If you translate, it's a must to load GoogleTranslator frfom deep_translation module
    # Standard: None


    flag_use_chatgpt = data_json['flag_use_chatgpt']

    if type(flag_use_chatgpt) != bool:
        raise TypeError("Key 'flag_use_chatgpt' is not in correct type 'bool'.")
    # Do you want to use chatgpt application?
    # Standard: False


    openai_api_key = data_json['openai_api_key']

    if type(openai_api_key) != str:
        raise TypeError("Key 'openai_api_key' is not in correct type 'str'.")
    # Open AI API key to use chatgpt generate ai.
    # Standard: ''


    flag_fill_phonetic_transc = data_json['flag_fill_phonetic_transc']

    if type(flag_fill_phonetic_transc) != bool:
        raise TypeError("Key 'flag_fill_phonetic_transc' is not in correct type 'bool'.")
    # If you fill the non-found phonetic transcriptions with eng_to_ipa package
    # Standard: False


    trans_word_method = data_json['trans_word_method']

    if type(trans_word_method) != str:
        raise TypeError("Key 'trans_word_method' is not in correct type 'str'.")
    # Parameters for translating examples
    # None: don't translate;
    # 'chatgpt': use chatgpt (don't recommended, translator is enought. 'flag_use_chatgpt = True' is a must.);
    # 'gtrans': use Google Translator package (recommended. 'flag_use_gtrans = True' is a must.).
    # Standard: 'gtrans'


    fill_examples_chatgpt = data_json['fill_examples_chatgpt']

    if type(fill_examples_chatgpt) != str:
        raise TypeError("Key 'fill_examples_chatgpt' is not in correct type 'str'.")
    # Parameters for filling examples that was not found on Longman Dictionary
    # 'phrases': you fill the phrase fill with one example with chat-gpt if there is no other tool to use ('flag_use_chatgpt = True' is a must.;
    # 'all': fill all examples fields with chat-gpt if necessary;
    # None: you don't fill it with chat-gpt.
    # Standard: None


    trans_examples_method = data_json['trans_examples_method']

    if type(fill_examples_chatgpt) != str:
        raise TypeError("Key 'fill_examples_chatgpt' is not in correct type 'str'.")
    # Parameters to translate words inserted
    # None: don't translate;
    # 'chatgpt': use chatgpt (recommended, but it spends tokens. 'flag_use_chatgpt = True' is a must.);
    # 'gtrans': use Google Translator package (don't recommended. 'flag_use_gtrans = True' is a must.).
    # Standard: None


    images_per_noun = data_json['images_per_noun']

    if (type(images_per_noun) != int):
        raise TypeError("Key 'images_per_noun' is not in correct type 'int'.")
    # Words to find the meaning
    # It should be a list (of strings) or a string


    words = data_json['words']

    if (type(words) != list) and (type(words) != str):
        raise TypeError("Key 'words' is not in correct type 'str' or 'list of strings'.")
    # Words to find the meaning
    # It should be a list (of strings) or a string

except KeyError as e:
    print('\nKey ' + str(e) + ' was not found. Application will be closed.')
    time.sleep(5)
    exit()
except TypeError as e:
    print('\n' + str(e) + ' Application will be closed.')
    time.sleep(5)
    exit()


# In[159]:


# Print data
print('\nVariables from ldoceonline_params.json are loaded:\n')
print('- Parameters imported:\n')
print('- language_to_translate: ', language_to_translate)
print('- flag_use_chatgpt: ',flag_use_chatgpt)
print('- openai_api_key: ',openai_api_key)
print('- flag_fill_phonetic_transc: ',flag_fill_phonetic_transc)
print('- trans_word_method: ',trans_word_method)
print('- fill_examples_chatgpt: ',fill_examples_chatgpt)
print('- images_per_noun: ',images_per_noun)
print('- trans_examples_method: ',trans_examples_method)
print('- words: ',words)


# # Pre-definited variables

# Fields of the table:
# - **Word**: the word name with the number if there is duplicates;
# - **Translation**: the translation of the field 'Word', considering the context of the field 'Meaning';
# - **Phonetic_Transcription**: the Phonetic Transcription of this word. The transcription must be between '/'. (Example: /laɪ/);
# - **Meaning**: In original language, not translated, I want the Part of Speech between parenthesis in beggining and after the complete meaning of the word;
# - **Phrase**: In original language, a phrase or sentence about the word, that helps to understand about its meaning. The word itself must be bold in html format;
# - **Translation_Phrase**: the translation of the field 'Phrase'. The translated word itself must be bold in html format;
# - **Example**: In original language, another phrase or sentence about the word, that helps to understand about its meaning. The word itself must be bold in html format;
# - **Translation_Example**: the translation of the field 'Example'. The translated word itself must be bold in html format;
# - **sPhrase**: empty;
# - **sExample**: empty;
# - **Image**: empty;
# - **Tags**: the original language in upper case, and the Part of Speech in lower case. (Example: ENGLISH adjective).
# 

# In[160]:


#   WORDS TO DELETE FROM GRAMMAR KEYS
list_gram_del = ['always','+','adverb/preposition','linking verb',']','[','linking verb']

# COLUMNS NAMES
columns_names = ['ID','word','word_url','Translation','POS','Phonetic_Transcription','Meaning','Phrase','Translation_Phrase','Example','Example_Phrase','sPhrase','sExample','Image','Credits','Tags']

# COLUMNS NAMES
log_columns_names = ['word','order_id','qtd_meanings','qtd_images','new_words_to_search']


# # Functions

# ### Open AI, chatgpt and dall-e functions

# In[161]:


# Check OPEN AI API status
def openai_api_status(module, send_ok_print: bool = True, send_error_print: bool = True):
    try:
        module.Completion.create(model="text-babbage-001", prompt="Test")  # A simple API call to check the key
        if send_ok_print: print('No errors')
        return True
    except Exception as e:
        if send_error_print: print(f"Error: {e}")
        return False


# In[162]:


# Check and retry to check open ai status
def openai_api_check_restart(module, send_ok_print: bool = True, send_error_print: bool = True):
    if not openai_api_status(module, send_ok_print, send_error_print): # First check
        if send_error_print: print('Trying to reconnect with Open AI API.')
        if openai_api_status(module, send_error_print, send_error_print): # Second check
            if send_error_print: print('Open AI API is working.')
            return True
        else:
            if send_error_print: print('Open AI API is not working. Close Open AI application.')
            return False
    else:
        if send_ok_print: print('Open AI API is OK.')
        return True


# In[163]:


# Generate example phrases from word and definition
def chatgpt_get_phrase_from_word(word: str, DEF: str = ''):
    if not openai_api_check_restart(openai, False, True): return '', 0, 0

    content = f"Generate a creative example phrase with \"{word}\".It's '{DEF.split()[0]}' and use its meaning: '{' '.join(DEF.split()[1:])}'."

    price_engine = 0.002 / 1000 # gpt-3.5-turbo costs $ 0.002 por 1,000 tokens at jul, 06 2023

    return_string = ''
    tokens = 0
    price = 0
    i = 0
    while (i <= 2): # loop to attempt to get the word meaning from chatgpt
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                max_tokens=250,
                n=1,
                temperature=1.0,
                messages=[{"role": "system", "content": content}]
            )
            return_string = response.choices[0].message.content
            i = 3
            tokens = response['usage']['total_tokens']
            price = round(response['usage']['total_tokens'] * price_engine,10)
            time.sleep(2)
        except Exception as e:
            error_text = str(e).strip()[:len('RateLimitError')]
            print(error_text)
            if error_text == 'RateLimitError':
                time.sleep(91)
                i += 1
            else:
                print(f'Error on ChatGPT module: {e}')
                i = 3

    if return_string == '': print('ChatGPT could not to return the phrase by a error process.')

    # Return string, spent tokens and price of tokens   
    return return_string, tokens, price


# In[164]:


# Generate word's translation from word, Part of speech, meaning and language to translate
def chatgpt_translate_word_from_eng(word: str, POS: str, MEANING: str, language: str):
    if not openai_api_check_restart(openai, False, True): return '', 0, 0

    content = f"How do you say '{word}' (part of speech '{POS}' and meaning '{MEANING}') from English to {language}? Return just the saying."

    price_engine = 0.002 / 1000 # gpt-3.5-turbo costs $ 0.002 por 1,000 tokens at jul, 06 2023

    return_string = ''
    tokens = 0
    price = 0
    i = 0
    while (i <= 2): # loop to attempt to get the word meaning from chatgpt
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                max_tokens=200,
                n=1,
                temperature=0,
                messages=[{"role": "system", "content": content}]
            )
            return_string = response.choices[0].message.content
            i = 3
            tokens = response['usage']['total_tokens']
            price = round(response['usage']['total_tokens'] * price_engine,10)
            time.sleep(2)
        except Exception as e:
            error_text = str(e).strip()[:len('RateLimitError')]
            print(error_text)
            if error_text == 'RateLimitError':
                time.sleep(91)
                i += 1
            else:
                print(f'Error on ChatGPT module: {e}')
                i = 3

    if return_string == '': print('ChatGPT could not to return the translation by a error process.')

    # Return string, spent tokens and price of tokens   
    return return_string, tokens, price


# In[165]:


# Generate word's translation from word, Part of speech, meaning and language to translate
def chatgpt_translate_phrase_from_eng(phrase: str, language: str):
    if not openai_api_check_restart(openai, False, True): return '', 0, 0

    content = f"How do you say the sentence '{phrase}' from English to {language}? Return just the saying."

    price_engine = 0.002 / 1000 # gpt-3.5-turbo costs $ 0.002 por 1,000 tokens at jul, 06 2023

    return_string = ''
    tokens = 0
    price = 0
    i = 0
    while (i <= 2): # loop to attempt to get the word meaning from chatgpt
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                max_tokens=200,
                n=1,
                temperature=0,
                messages=[{"role": "system", "content": content}]
            )
            return_string = response.choices[0].message.content
            i = 3
            tokens = response['usage']['total_tokens']
            price = round(response['usage']['total_tokens'] * price_engine,10)
            time.sleep(2)
        except Exception as e:
            error_text = str(e).strip()[:len('RateLimitError')]
            print(error_text)
            if error_text == 'RateLimitError':
                time.sleep(91)
                i += 1
            else:
                print(f'Error on ChatGPT module: {e}')
                i = 3

    if return_string == '': print('ChatGPT could not to return the translation by a error process.')              

    # Return string, spent tokens and price of tokens   
    return return_string, tokens, price 


# ### Auxiliary functions

# In[166]:


# Clean repetitive words from string
def unique_words_in_string(input_string):
    cleaned_words = []
    for word in input_string.strip().split():
        if word not in cleaned_words: cleaned_words.append(word)
    return ' '.join(cleaned_words)


# In[167]:


# Mark duplicated values from list
def list_mark_duplicates(list: list):
    if not str(type(list)).replace("<class '","").replace("'>","") == 'list': return # Check if it''s a list
    else: return [True if v in list[:i] else False for i, v in enumerate(list)] # Returning


# In[92]:


# Return random values from string
def get_random_values(my_list: list, num_values: int):

    # Generate pseudorandom number
    def generate_pseudo_random(seed):
        return (1103515245 * seed + 12345) % (2**31 - 1)
    
    # Use the hash of the memory address as the seed for the pseudo-random number generator
    seed = hash(id(my_list))

    # Generate a list of num_values pseudo-random indices
    indices = []
    i = 1
    while i <= num_values:
        seed = generate_pseudo_random(seed)
        index = seed % len(my_list)

        if index in indices: continue # Checking repetitive values

        indices.append(index)
        i += 1

    return [my_list[index] for index in indices]


# In[169]:


# Export list to csv
def export_to_csv(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for row in data:
            line = ';'.join('"'+str(value)+'"' for value in row)
            file.write(line + '\n')


# In[170]:


# Remove special characters
def remove_special_characters(string):
    return ''.join([char if ((char.isalnum()) or char == ' ') else '' for char in string])


# In[171]:


# Remove excessive spaces on a string
def remove_excessive_spaces(string : str):
    return ' '.join(string.strip().split())


# In[172]:


# Get formatted time
def get_complete_datetime():
    current_time = time.localtime()
    month = time.strftime("%B", current_time)
    day = time.strftime("%d", current_time)
    year = time.strftime("%Y", current_time)
    hour = time.strftime("%H", current_time)
    minute = time.strftime("%M", current_time)
    
    ordinal_suffix = "th" if 11 <= int(day) <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(int(day) % 10, "th")
    
    return f"{month} {day}{ordinal_suffix}, {year}, {hour}:{minute}"


# In[173]:


# Replace special characters
def replace_special_characters(string : str, replacement : str = ''):
    return ''.join([char if ((char.isalnum()) or char == ' ') else replacement for char in string])

    # special_characters = "!@#$%^&*()[]{};:,./<>?\|`~-=_+’\'\""
    # translation_table = str.maketrans(special_characters, replacement * len(special_characters))
    # return text.translate(translation_table)


# ### Main functions (execution, web scrapping etc.)

# In[174]:


#############################################################################
# FUNCTION: Create the link of the word
def meanings_word_ldoceonline(word, url):

    ########################
    # CONNECT AND GET HTML FROM URL
    response = requests.get(url, headers={
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })
    soup = BeautifulSoup(response.text, "html.parser")

    list_meaning = []
    list_return_words = []
    list_return_urls = []

    ########################
    # LOOP BY ALL 'DICTENTRY' THAT IS POSSIBLE ON LONGMAN DICTIONARY WORD

    m = 0 # meaning word ID
    total_chatgpt_token = 0
    total_chatgpt_price = 0
    phonetic_transcription = '' # No return from word's phonetic transcription

    count_dictentry = 0
    for dictentry in soup.find_all("span", attrs={"class": "dictentry"}): # Loop in 'dictentry' class
        count_dictentry += 1

    for dictentry in soup.find_all("span", attrs={"class": "dictentry"}): # Loop in 'dictentry' class

        ###########
        # Get subclass 'dictlink'
        dictlink = dictentry.find("span", {"class": "dictlink"})
        if not isinstance(dictlink.find("span", {"class": "ldoceEntry Entry"}), type(None)): subclass = "ldoceEntry Entry"
        elif (count_dictentry == 1) and (not isinstance(dictlink.find("span", {"class": "bussdictEntry Entry"}), type(None))): subclass = "bussdictEntry Entry"
        else: continue
        dict_content = dictlink.find("span", {"class": subclass})

        ###########
        # Get Phonetic Transcription
        phonetic_transcription_html = dict_content.find("span", {"class": 'PronCodes'})
        if not isinstance(phonetic_transcription_html, type(None)): phonetic_transcription = phonetic_transcription_html.text
 
        ###########
        # Get Related Topic
        topic_1_html = dict_content.find("a", {"class": 'topic'})
        if isinstance(topic_1_html, type(None)): topic_str = ''
        else:
            topic_html = topic_1_html.find("a", {"class": 'topic'})
            if isinstance(topic_html, type(None)): topic_str = ''
            else: topic_str = (topic_html.text).lower().replace('topic','').strip()
        
        ###########    
        # Get Part of Speech
        POS_html = dict_content.find("span", {"class": 'POS'})
        if isinstance(POS_html, type(None)): POS_str = 'expression'
        else: POS_str = (POS_html.text).strip()
        
        ###########
        # Get Inflections (Part of Speech)
        Inflections_html = dict_content.find("span", {"class": 'Inflections'})
        if isinstance(Inflections_html, type(None)): Inflections_str = ''
        else: Inflections_str = Inflections_html.text
        
        ###########
        # Get Gramatical classification from POS at all
        Gram_HTML = dict_content.find("span", attrs={"class":"Head"}).find("span", attrs={"class":"GRAM"})
        if isinstance(Gram_HTML, type(None)):
            Gram_tag_gen = ''
            Gram_str_gen = ''
        else:
            Gram_tag_gen = ' '.join([word for word in (Gram_HTML.text).strip().replace(']','').replace('[','').split() if word not in list_gram_del])
            Gram_str_gen = Gram_HTML.text.strip() + ' '

        ###########
        # Word header
        Header_str = (POS_str + ' ' + Inflections_str + ' ' + Gram_str_gen).strip()

        ###########
        # Check dict_content tail
        runon_str = ''
        for TAIL_html in dict_content.find_all("span", attrs={"class":"Tail"}):

            # Get all new words to get in Tail of dictcontext
            if not isinstance(TAIL_html.find("span", attrs={"class":"Crossref"}), type(None)):
                for crossRef_html in TAIL_html.find("span", attrs={"class":"Crossref"}).find_all("a", attrs={"class":"crossRef"}):
                    if word.strip().upper() in crossRef_html.text.upper():
                        list_return_words.append((crossRef_html.get('title')).strip())
                        list_return_urls.append('https://www.ldoceonline.com' + crossRef_html.get('href').strip())  

            # Get derivated words to save on word's meaning: 'RunOn'
            if not isinstance(TAIL_html.find("span", attrs={"class":"RunOn"}), type(None)):
                for RunOn_html in TAIL_html.find_all("span", attrs={"class":"RunOn"}):

                    if isinstance(RunOn_html.find("span", attrs={"class":"DERIV"}), type(None)): text_deriv = ''
                    else: text_deriv = RunOn_html.find("span", attrs={"class":"DERIV"}).text.strip()

                    if isinstance(RunOn_html.find("span", attrs={"class":"POS"}), type(None)): text_POS = ''
                    else: text_POS = RunOn_html.find("span", attrs={"class":"POS"}).text.strip()

                    runon_str += '\n' + ( '— ['+ text_POS + '] ' + text_deriv).strip()
                del RunOn_html, text_deriv, text_POS


        ###########
        # Count the quantity of meanings here
        m_count = 0
        for sense in dict_content.find_all("span", attrs={"class":"Sense"}):
            if isinstance(sense.find("span", attrs={"class":"Crossref"}), type(None)): m_count +=1

        ###########
        # Loop for all senses for the word
        for sense in dict_content.find_all("span", attrs={"class":"Sense"}):
            
            DEF, PURE_DEF, Example_1, Example_2, Example_1_T, Example_2_T = '', '', '', '', '', ''
            TAG = ('English ' + POS_str + ' ' + Gram_tag_gen + ' ' + topic_str).strip()

            # Check if the meaning is just a Crossref to another page
            if not isinstance(sense.find("span", attrs={"class":"Crossref"}), type(None)):

                # If sense refers to a crossref word, get the link to upload its meaning in future loop
                crossRef_html = sense.find("a", attrs={"class":"crossRef"})
                if not isinstance(crossRef_html, type(None)):
                    if word.strip().upper() in crossRef_html.text.upper():
                        list_return_words.append((crossRef_html.get('title')).strip())
                        list_return_urls.append('https://www.ldoceonline.com' + crossRef_html.get('href'))

            if not isinstance(sense.find("span", attrs={"class":"DEF"}), type(None)):

                m += 1 # Add one to meaning ID

                # Get Signpost
                SIGNPOST_html = sense.find("span", attrs={"class":"SIGNPOST"})
                if isinstance(SIGNPOST_html, type(None)): SIGNPOST = ''
                else: 
                    SIGNPOST = (SIGNPOST_html.get_text()).strip().upper()
                    if len(SIGNPOST.replace("/"," ").split()) < 3:
                        TAG = TAG + ' ' + SIGNPOST.replace("/"," ")
                    SIGNPOST = '\n[' + SIGNPOST + ']'

                # Check if the meaning has 'Subsense' to get its meaning and improve TAG values
                if not isinstance(sense.find("span", attrs={"class":"Subsense"}), type(None)):

                    # Loop for all senses for the word
                    for Subsense in sense.find_all("span", attrs={"class":"Subsense"}):

                        # Get sensenum_span
                        NUM_html = Subsense.find("span", attrs={"class":"sensenum span"})
                        if isinstance(NUM_html, type(None)): NUM_str = ''
                        else: NUM_str = NUM_html.text + ' '

                        # Get word definition
                        DEF_html = Subsense.find("span", attrs={"class":"DEF"})
                        if isinstance(DEF_html, type(None)): DEF_str = ''
                        else: DEF_str = DEF_html.text

                        # Get word gramatical substance
                        Gram_HTML = Subsense.find("span", attrs={"class":"GRAM"})
                        if isinstance(Gram_HTML, type(None)): Gram_str = ''
                        else:
                            Gram_tag = ' '.join([word for word in (Gram_HTML.text).strip().replace(']','').replace('[','').split() if word not in list_gram_del])
                            TAG = TAG + ' ' + Gram_tag
                            Gram_str = Gram_HTML.text.strip() + ' '

                        # Get synominous (BREQUIV or SYN)
                        SYN_html = Subsense.find("span", attrs={"class":"BREQUIV"})
                        if isinstance(SYN_html, type(None)):
                            SYN_html = Subsense.find("span", attrs={"class":"SYN"})
                            if isinstance(SYN_html, type(None)): SYN_str = ''
                            else:  SYN_str = ' (' + SYN_html.text.strip() + ')'
                        else: SYN_str = ' (' + SYN_html.text.strip() + ')'

                        # Get geographic reference
                        GEO_html = Subsense.find("span", attrs={"class":"GEO"})
                        if isinstance(GEO_html, type(None)): GEO_str = ''
                        else:
                            TAG = TAG + ' ' + GEO_html.text.lower().replace('english','').strip().capitalize()
                            GEO_str = '[' + GEO_html.text.strip() + '] '

                        # Save word definition var
                        DEF_content = NUM_str + Gram_str + GEO_str + DEF_str.strip().capitalize() + '.' + SYN_str
                        if DEF == '': DEF = Header_str + SIGNPOST + '\n' + DEF_content
                        else: DEF = DEF + ';\n' + DEF_content
                        PURE_DEF +=  ('; ' + DEF_content).strip()

                    # Finish DEF with derivated words
                    DEF += runon_str

                else:
                    # Nulify sensespan_num
                    NUM_str = ''

                    # Get word definition
                    DEF_html = sense.find("span", attrs={"class":"DEF"})
                    if isinstance(DEF_html, type(None)): DEF_str = ''
                    else: DEF_str = DEF_html.text

                    # Get word gramatical substance
                    Gram_HTML = sense.find("span", attrs={"class":"GRAM"})
                    if isinstance(Gram_HTML, type(None)): Gram_str = ''
                    else:
                        Gram_tag = ' '.join([word for word in (Gram_HTML.text).strip().replace(']','').replace('[','').split() if word not in list_gram_del])
                        TAG = TAG + ' ' + Gram_tag
                        Gram_str = Gram_HTML.text.strip() + ' '

                    # Get synominous (BREQUIV or SYN)
                    SYN_html = sense.find("span", attrs={"class":"BREQUIV"})
                    if isinstance(SYN_html, type(None)):
                        SYN_html = sense.find("span", attrs={"class":"SYN"})
                        if isinstance(SYN_html, type(None)): SYN_str = ''
                        else:  SYN_str = ' (' + SYN_html.text.strip() + ')'
                    else: SYN_str = ' (' + SYN_html.text.strip() + ')'

                    # Get geographic reference
                    GEO_html = sense.find("span", attrs={"class":"GEO"})
                    if isinstance(GEO_html, type(None)): GEO_str = ''
                    else:
                        TAG = TAG + ' ' + GEO_html.text.lower().replace('english','').strip().capitalize()
                        GEO_str = '[' + GEO_html.text.strip() + '] '

                    # Save word definition var
                    DEF_content = NUM_str + Gram_str + GEO_str + DEF_str.strip().capitalize() + '.' + SYN_str
                    if DEF == '': DEF = Header_str + SIGNPOST + '\n' + DEF_content
                    else: DEF = DEF + ';\n' + DEF_content
                    PURE_DEF +=  ('; ' + DEF_content).strip()

                    # Finish DEF with derivated words
                    DEF += runon_str

                # Insert examples from sense
                list_examples = [(Example_html.text).strip().capitalize() for Example_html in sense.find_all("span", attrs={"class":"EXAMPLE"})]
                if len(list_examples) > 1: Example_1, Example_2 = get_random_values(list_examples, 2)
                elif len(list_examples) == 1: Example_1, Example_2 = list_examples[0], ''
                del list_examples

                # Fill empty examples
                # With example list of we have just one meaning
                if (m_count == 1) and ((Example_1 == '') or (Example_2 == '')):
                    for ASSETLINK_html in dictentry.find_all("span", attrs={"class":"assetlink"}):
                        if not isinstance(ASSETLINK_html.find("span", attrs={"class":"cexa1g1 exa"}), type(None)):

                            # Insert examples from examples list
                            list_examples = [POSEXAMPLE_html.text.strip().replace('• ','') for POSEXAMPLE_html in ASSETLINK_html.find_all("span", attrs={"class":"cexa1g1 exa"})]
                            if len(list_examples) > 1:
                                if (Example_1 == '') and (Example_2 == ''): Example_1, Example_2 = get_random_values(list_examples, 2)
                                elif Example_1 == '': Example_1 = get_random_values(list_examples, 1)[0]
                                elif Example_2 == '': Example_2 = get_random_values(list_examples, 1)[0]
                            elif len(list_examples) == 1:
                                if Example_1 == '': Example_1 = list_examples[0]
                                elif Example_2 == '': Example_2 = list_examples[0]
                            del list_examples

                # With chatgpt if set
                if global_fexamp_gpt in ['phrases','all']:
                    if Example_1 == '':
                        str_value, token_value, price_value = chatgpt_get_phrase_from_word(word, DEF)
                        Example_1 = str_value
                        total_chatgpt_token += token_value
                        total_chatgpt_price += price_value
                        del str_value, token_value, price_value
                    if (global_fexamp_gpt == 'all') and (Example_2 == ''):
                        str_value, token_value, price_value = chatgpt_get_phrase_from_word(word, DEF)
                        Example_2 = str_value
                        total_chatgpt_token += token_value
                        total_chatgpt_price += price_value
                        del str_value, token_value, price_value

                # Translate examples - use Google Translator or Chat GPT
                if global_texamp == 'gtrans':
                    if Example_1 != '':
                        try:
                            Example_1_T = GoogleTranslator(source='en', target=global_lang_simple).translate(text=Example_1)
                        except Exception as inst:
                            print(f'Error: example {Example_1} was not translated by a error on text itself.')
                            Example_1_T = ''
                    if Example_2 != '':
                        try:
                            Example_2_T = GoogleTranslator(source='en', target=global_lang_simple).translate(text=Example_2)
                        except Exception as inst:
                            print(f'Error: example {Example_2} was not translated by a error on text itself.')
                            Example_2_T = ''
                elif global_texamp == 'chatgpt':
                    if Example_1 != '':
                        str_value, token_value, price_value = chatgpt_translate_phrase_from_eng(word, global_lang_compl)  # Get example's translation from chatgpt
                        Example_1 = str_value
                        total_chatgpt_token += token_value
                        total_chatgpt_price += price_value
                        del str_value, token_value, price_value
                    if Example_2 != '':
                        str_value, token_value, price_value = chatgpt_translate_phrase_from_eng(word, global_lang_compl)  # Get example's translation from chatgpt
                        Example_2 = str_value
                        total_chatgpt_token += token_value
                        total_chatgpt_price += price_value
                        del str_value, token_value, price_value
                
                # Translate word - use Google Translator or Chat GPT
                if global_tword == 'gtrans': Word_T = GoogleTranslator(source='en', target=global_lang_simple).translate(text=word)
                if global_tword == 'chatgpt':
                    str_value, token_value, price_value = chatgpt_translate_word_from_eng(word, POS_str, PURE_DEF, global_lang_compl) # Get word's translation from chatgpt
                    Word_T = str_value.replace('"','').replace("'","").replace(".","")
                    total_chatgpt_token += token_value
                    total_chatgpt_price += price_value
                    del str_value, token_value, price_value
                else: Word_T = ''

                # Adjust phonetic_transcription - use eng_to_ipa package
                if phonetic_transcription == '' and global_phonetic_transc: phon_transc = '/' + eng_to_ipa.convert(word) + '/'
                else: phon_transc = phonetic_transcription

                # Save meanings
                list_meaning.append([replace_special_characters(word).strip().replace(' ','_') + '__' + str(m).zfill(2) + '__' + POS_str.strip().replace(' ','_') # ID
                    ,'to ' + word if POS_str in ['verb','phrasal verb'] else word # Word
                    ,remove_excessive_spaces(replace_special_characters(word.strip()," ")).replace(' ','-').lower() # Word_URL
                    ,Word_T # Translation
                    ,POS_str # POS
                    ,phon_transc # Phonetic transcription
                    ,DEF # Definition
                    ,Example_1 # Phrase
                    ,Example_1_T # Phrase translation
                    ,Example_2 # Example translation
                    ,Example_2_T # Example translation
                    ,'' # Phrase audio
                    ,'' # Example audio
                    ,'' # Image
                    ,global_credits # Credits
                    ,unique_words_in_string(TAG)])               

        m_prev = m # Update m_prev for checking only one meaning applied by 'dictentry'

    return list_meaning, [list_return_words, list_return_urls], total_chatgpt_token, total_chatgpt_price


# In[175]:


#############################################################################
# FUNCTION: GET IMAGES FROM GOOGLE BY WORD

def get_google_images(query: str, img_name: str, images_limit: int):

    # Function to use beautiful soap
    def get_soup(url,header):
        return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))

    # you can change the query for the image  here  
    query = "picture object " + query.lower().strip()
    query= query.split()
    query='+'.join(query)
    url=f"https://www.google.com/search?q={query}&tbm=isch&ved=2ahUKEwjEi-G5-bb_AhUruZUCHeQRALAQ2-cCegQIABAA&oq=sun+glasses&gs_lcp=CgNpbWcQDFAAWABgvFloAHAAeACAAX2IAfUBkgEDMC4ymAEAqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=AYGDZISHG6vy1sQP5KOAgAs&bih=833&biw=1745"

    soup = get_soup(url,{'User-Agent': 'Mozilla/5.0'})

    if not os.path.exists(os.getcwd() + "\\" + "ldoceonline_images"): os.makedirs(os.getcwd() + "\\" + "ldoceonline_images")

    images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
    for i, img in enumerate(images):
        if (i + 1) > images_limit: break

        raw_img = urllib2.urlopen(img).read()
        
        DIR = os.getcwd() + "\\" + "ldoceonline_images" # Add the directory for your image here 

        f = open(DIR + "\\" + img_name + '_' + str(i + 1).zfill(2) + '.jpg', 'wb')
        f.write(raw_img)
        f.close()

    return


# In[176]:


#############################################################################
# FUNCTION: LOOP TO GET COMPLETE DEFINITION FROM LONGMAN DICTIONARY
def list_word_ldoceonline(list_words):

    ########################
    # Validate the inputed variable 'list_words'
    type_list_words = str(type(list_words)).replace("<class '","").replace("'>","")
    if type_list_words == 'str':
        list_words = [list_words]
    elif type_list_words == 'list':
        list_words = list(list_words)
        for values in list_words:
            if not str(type(values)).replace("<class '","").replace("'>","") == 'str':
                print("Your list from 'list_words' must have only strings.")
                return []
    else:
        print("'list_words' must be a string or a list.")
        return []
    

    ########################
    # Create lists
    list_words = list((list_words,["https://www.ldoceonline.com/dictionary/" + remove_excessive_spaces(replace_special_characters(word.strip()," ")).replace(' ','-') for word in list_words])) # Add the URL of Longman Dictionary on the list

    list_all_meaning = [] # List empty to get all meaning and examples
    log_list = [] # List empty to get all meaning and examples

    # Clean duplicated words
    list_check_dup = list_mark_duplicates(list_words[0])
    list_words = [[value for value, marked in zip(sublist, list_check_dup) if not marked] for sublist in list_words]


    ########################
    # Loop the values
    print(f'\nStart to search meanings.\n')
    i = 0
    total_chatgpt_token = 0
    total_chatgpt_price = 0
    i_max = len(list_words[0])

    while (i < i_max):

        # Print the current word
        print(f'- Word "{list_words[0][i]}". {i+1} of {(i_max)}.')

        # Get the meaning and examples
        list_1_tmp, list_2_tmp, token_chatgpt, price_chatgpt = meanings_word_ldoceonline(list_words[0][i].strip(),list_words[1][i]) # Get from function meanings and new expressions to find

        # Update lists
        list_all_meaning += list_1_tmp # Save meanings found
        list_words[0] += list_2_tmp[0] # Update new words/expressions to find
        list_words[1] += list_2_tmp[1] # Update their URLs
        total_chatgpt_token += token_chatgpt # Sum of total tokens used from chatgpt
        total_chatgpt_price += price_chatgpt # Sum of total money spent from chatgpt
        
        # Clean duplicated words
        list_check_dup = list_mark_duplicates([word_check.lower() for word_check in list_words[0]])
        list_words = [[value for value, marked in zip(sublist, list_check_dup) if not marked] for sublist in list_words]

        # Print the updates of values
        print(f'{len(list_1_tmp)} meanings from word "{list_words[0][i]}" and {(len(list_words[0]) - i_max)} news words to look for.')

        # Get images to optionally use after on your Anki Cards
        if global_images > 0:
            if 'noun' in [POS[4] for POS in list_1_tmp]:
                qtd_images = global_images
                get_google_images(replace_special_characters(list_words[0][i]).strip().replace(' ','_'), 'img_' + list_words[0][i].strip(), global_images) # generate images to save
                print(str(global_images) + ' images were imported from word ' + list_words[0][i].strip())
            else: qtd_images = 0

        # Update log list
        log_list.append([list_words[0][i], i+1, len(list_1_tmp), qtd_images, (len(list_words[0]) - i_max)])

        # Update temporary variables
        i_max = len(list_words[0])
        i += 1
        del list_1_tmp, list_2_tmp, list_check_dup, token_chatgpt, price_chatgpt


    if total_chatgpt_token > 0: print(f'\nChat GPT spends: {total_chatgpt_token} tokens and {total_chatgpt_price} dolars.')
    print(f'{len(list_all_meaning)} meanings from {len(list_words[0])} words were found and mapped.')
    print(f'\nSearching meanings is finished.')

    ########################
    # Finish the function returning the list
    return list_all_meaning, log_list


# # Apply parameters

# In[177]:


print('\n###################################################################')
print('Import modules according with the parameters:\n')


# In[178]:


#### PARAMETER: flag_fill_phonetic_transc -> global_phonetic_transc
global_phonetic_transc = False
text_warning = "\nNo empty phonetic transcription from Longman Dictionary won't be filled."
if flag_fill_phonetic_transc:
    if import_and_check('eng_to_ipa', import_module = True):
        global_phonetic_transc = True
        text_warning = "\neng_to_ipa module will be used to fill empty phonetic transcriptions fields."

print(text_warning)


# In[179]:


#### PARAMETER: flag_use_chatgpt, openai_api -> global_apply_chatgpt
global_apply_chatgpt = False
text_warning = '\nopenai module won\'t be used on this execution.'
if flag_use_chatgpt:
    if import_and_check('openai', import_module = True):
        openai.api_key = openai_api_key # Use chatgpt api key
        if openai_api_check_restart(openai): # Check if chatgpt is working
            global_apply_chatgpt = True
            text_warning = '\nopenai module will be used for Chat GPT applications.'

print(text_warning)


# In[180]:


#### PARAMETER: language_to_translate -> global_apply_trans, global_lang_simple, global_lang_compl, langs_dict
# Load supported languages pack
global_apply_trans = False
global_lang_simple, global_lang_compl = '', ''
text_warning = "\nGoogleTranslator (from deep_translator module) will not be used on this execution."
if not language_to_translate in [None,'']:
    if import_and_check('deep_translator','GoogleTranslator', import_module = True):
        global_apply_trans = True
        text_warning = "\nGoogleTranslator (from deep_translator module) will be used on this execution."

        # List of valid languages
        langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)

        # Confirm language configured
        if language_to_translate not in langs_dict.values(): global_lang_simple = 'pt'
        else: global_lang_simple = language_to_translate

        # Get complete language name
        for key, val in langs_dict.items():
            if val == global_lang_simple:
                global_lang_compl = key.strip()
                break

print(text_warning)


# In[181]:


#### PARAMETER: trans_word_method -> global_tword
if (not trans_word_method in ['chatgpt','gtrans']) or (global_apply_trans == False): global_tword = ''
elif trans_word_method == 'chatgpt' and global_apply_chatgpt: global_tword = trans_word_method
elif trans_word_method == 'gtrans': global_tword = trans_word_method
else: global_tword = ''

print('\n' + ('Words will be translated by ChatGPT' if global_tword == 'chatgpt' else 'Words will be translated by Google Translation (not recommended)' if global_tword == 'gtrans' else 'Words won\'t be translated.'))


# In[182]:


#### PARAMETER: trans_examples_method -> global_texamp
if (not trans_examples_method in ['chatgpt','gtrans']) or (global_apply_trans == False): global_texamp = ''
elif trans_examples_method == 'chatgpt' and global_apply_chatgpt: global_texamp = trans_examples_method
elif trans_examples_method == 'gtrans': global_texamp = trans_examples_method
else: global_texamp = ''

print('\n' + ('Examples will be translated by ChatGPT' if global_texamp == 'chatgpt' else 'Examples will be translated by Google Translation (not recommended)' if global_texamp == 'gtrans' else 'Examples won\'t be translated.'))


# In[183]:


#### PARAMETER: fill_examples_chatgpt -> global_fexamp_gpt
if (not fill_examples_chatgpt in ['phrases','all']) or (global_apply_chatgpt == False): global_fexamp_gpt = ''
else: global_fexamp_gpt = fill_examples_chatgpt

print('\n' + ('Just empty initial phrases (example 1) will be filled by Chat GPT' if global_fexamp_gpt == 'phrases' else 'All empty examples will be filled by Chat GPT' if global_fexamp_gpt == 'all' else 'Examples won\'t be filled if empty.'))


# In[184]:


#### PARAMETER: images_per_noun -> global_images
text_warning = "\nImages will not be generated per word."
global_images = 0
if images_per_noun > 0:
     if import_and_check('urllib.request', librename = 'urllib2', import_module = False) and         import_and_check('re', import_module = False):
            
            # Import packages for images
            import re
            import urllib.request as urllib2
            print('re and urllib2 were imported.')

            # Update status
            global_images = images_per_noun
            text_warning = '\n' + str(images_per_noun) + " images will be generated per word."

print(text_warning)


# In[185]:


#print(global_phonetic_transc, global_apply_chatgpt, global_apply_trans, global_lang_simple, global_lang_compl, global_tword, global_texamp, global_fexamp_gpt)


# In[186]:


global_credits = 'Word definitions, meanings, and example sentences sourced from ldoceonline.com, by Pearson'
if (global_tword == 'chatgpt') or (global_texamp == 'chatgpt') or (global_fexamp_gpt in ['phrases','all']): 
    global_credits += ';\nadditional information and translation provided by ChatGPT, by OpenAI'
if (global_tword == 'gtrans') or (global_texamp == 'gtrans'):
    global_credits += ';\nother translations was executed by Google Translator, by deep_translator (Nidhal Baccouri) (https://pypi.org/project/deep-translator/)'
if global_phonetic_transc:
    global_credits += ';\nand some phonetic transcriptions were made by eng_to_ipa (https://pypi.org/project/eng-to-ipa/)'
global_credits += '\nWord were taken at ' + get_complete_datetime() + '.'

print('\nCredits:\n' + global_credits + '\n')


# # Applying model

# ### Input words to translate

# In[187]:


print('\n\n###################################################################')


# ###  Execute function

# In[188]:


list_ex, log = list_word_ldoceonline(words)


# In[189]:


print('\n\n###################################################################')


# ### Export results

# In[190]:


file_datetime = time.strftime("%Y%m%d_%H%M%S", time.localtime(int(time.time())))

# Export meanings
if not os.path.exists("words_" + file_datetime + ".csv"):    
    export_to_csv([columns_names] + list_ex, "words_" + file_datetime + ".csv")
    print('The file ' + "words_" + file_datetime + ".csv" + ' was created with the meanings from the inputed words.')
else:
    i = 1
    while os.path.exists("words_" + file_datetime + "_" + str(i).zfill(2) + ".csv"):
        i += 1
    export_to_csv([columns_names] + list_ex, "words_" + file_datetime + "_" + str(i).zfill(2) + ".csv")
    print('The log file ' + "words_" + "words_" + file_datetime + "_" + str(i).zfill(2) + ".csv" + ' was created from the inputed words.')

# Export log
if not os.path.exists("words_" + file_datetime + ".csv"):    
    export_to_csv([log_columns_names] + log, "log_" + file_datetime + ".csv")
    print('The file ' + "log_" + file_datetime + ".csv" + ' was created with the meanings from the inputed words.')
else:
    i = 1
    while os.path.exists("words_" + file_datetime + "_" + str(i).zfill(2) + ".csv"):
        i += 1
    export_to_csv([log_columns_names] + log, "log_" + file_datetime + ".csv")
    print('The log file ' + "words_" + "log_" + file_datetime + "_" + str(i).zfill(2) + ".csv" + ' was created from the inputed words.')
          
time.sleep(10)

