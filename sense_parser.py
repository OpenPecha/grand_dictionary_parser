import anthropic
import json
import time
from pathlib import Path

from config import ANTHROPIC_CLIENT



def parse_senses_with_claude(word, descriptions):
    senses = {}
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
གཤམ་གྱི་བརྗོད་པ་ནང་ནས་མ་ཚིག་དང་། POS tag, Tag འགྲེལ་བ། དཔེར་བརྗོད་ཚིག་སྒྲུབ་ ལུང་ཚིག ལུང་ཁུངས་བཅས་དབྱེ་བ་ཕྱེས་ཏེ་
གཤམ་གྱི་Dictionary format ནང་སྤྲད་རོགས། 
Dictionary format: 
{{
    'lemma': 'word', 
    'sense': {{
        '1':{{
            'description': 'description1', 
            'POS_tag': 'pos tag1',
            'example_sentence': ['example 1', 'example 2'],
            'tag': ['tag1','tag2'],
            'citation_text': 'text1',
            'citation_source": 'source1'
            }},
        '2':{{
            'description': 'description2', 
            'POS_tag': 'pos tag2',
            'example_sentence': ['example 1', 'example 2'],
            'tag': ['tag1','tag2'],
            'citation_text': 'text2',
            'citation_source": 'source2'
            }},
        
         }}
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
        print(f"Error processing {word}: {e}")
    
    return senses_dict


if __name__ == "__main__":
    """
    The above code has been tested with all the corner cases and it is working fine.
    """
    word = "བྲོ་"
    descriptions = Path("./test/sense_corner_cases/sense1.txt").read_text()
    senses = parse_senses_with_claude(word, descriptions)
 
    