import json
import logging
import re
import time
from pathlib import Path

from config import ANTHROPIC_CLIENT

logger = logging.getLogger(__name__)

def preprocess_sense_text(sense_text):
    sense_text = re.sub("\d+\.", "", sense_text)
    return sense_text



def parse_senses_with_claude(word_id, word, descriptions):
    descriptions = preprocess_sense_text(descriptions)
    senses_dict = {}
    time.sleep(5)
    try:
        message = ANTHROPIC_CLIENT.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8192,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": f"""
གཤམ་གྱི་བརྗོད་པ་ནང་ནས་མ་ཚིག་གི་POS tagདང་, Tag འགྲེལ་བ། དཔེར་བརྗོད་ཚིག་སྒྲུབ་ ལུང་ཚིག ལུང་ཁུངས་བཅས་དབྱེ་བ་ཕྱེས་ཏེ་
གཤམ་གྱི་Dictionary format ནང་སྤྲད་རོགས། 
Dictionary format: 
{{
'1':{{
    'description': 'description1', 
    'POS_tag': 'pos tag1',
    'example_sentence': ['example 1', 'example 2'],
    'tag': ['tag1','tag2'],
    'citation': {{
            '1':{{
                'text': 'citation_text1',
                'source': 'citation_source1'
            }},
            '2':{{
                'text': 'citation_text2',
                'source': 'citation_source2'
            }}
        }}
    }},
'2':{{
    'description': 'description2', 
    'POS_tag': 'pos tag2',
    'example_sentence': ['example 1', 'example 2'],
    'tag': ['tag1','tag2'],
    'citation': {{
            '1':{{
                'text': 'citation_text1',
                'source': 'citation_source1'
            }},
            '2':{{
                'text': 'citation_text2',
                'source': 'citation_source2'
            }}
        }}
    }},
}}
Tag དང་དཔེར་བརྗོད་ཚིག་སྒྲུབ་ཡོད་ཚད་List ནང་འཇུག་རོགས། 
གལ་ཏེ་བརྗོད་པའི་ནང་POS Tag, Tag དང་། འགྲེལ་བ། དཔེར་བརྗོད་ཚིག་སྒྲུབ་ ལུང་ཚིག ལུང་ཁུངས་གང་རུང་གསལ་སྟོན་བྱས་མེད་ན་སྟོང་པ་འཇོག་རོགས། 
བརྗོད་པའི་ནང་སྐབས་རེར་ལུང་ཚིག་དང་ལུང་ཁངས་གཅིག་ལས་མང་བ་ཡོད་སྲིད། 
བརྗོད་པ་:
{word}
{descriptions}
"""
                                }
                            ]
                        }
                    ]
                )
        senses = message.content[0].text
        senses = senses.replace("'", '"')
        senses_dict = json.loads(senses)

    except Exception as e:
        logger.error(f"Error processing sense text {descriptions} of {word}/{word_id}") 
    
    return senses_dict


if __name__ == "__main__":
    """
    The above code has been tested with all the corner cases and it is working fine.
    """
    corner_case_files = list(Path('./test/sense_corner_cases').glob('*.txt'))
    corner_case_files.sort()
    for word_id, file in enumerate(corner_case_files[-1:],1):
        descriptions = file.read_text()
        descriptions = preprocess_sense_text(descriptions)
        word = file.stem.split("_")[0]
        senses = parse_senses_with_claude(word_id, word, descriptions)
        with open(f"./test/sense_corner_cases/test_res/{file.stem}.json", "w") as f:
            json.dump(senses, f, ensure_ascii=False, indent=4)
 
    