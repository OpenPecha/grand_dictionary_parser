import json
import time
from pathlib import Path

from config import ANTHROPIC_CLIENT


def parse_citations_with_claude(ciation_text):
    time.sleep(5)
    try:
        ai_response = ANTHROPIC_CLIENT.messages.create(
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
གཤམ་གྱི་བརྗོད་པ་ནང་ནས་དཔེ་དེབ་ཀྱི་མཚན་བྱང་། མཚན་བྱང་བསྡུས་པ། པོད་ཕྲེང་། ཤོག་ངོས། ཐིག་ཕྲེང་། 
རྩོམ་སྒྲིག་པ། རྩོམ་སྒྲིག་པ་སྐྱེས་ལོ། རྩོམ་སྒྲིག་པ་འདས་ལོ། རྩོམ་སྒྲིག་གི་རྣམ་པ།
གཏེར་སྟོན་གྱི་མིང་། གཏེར་སྟོན་གྱི་སྐྱེས་ལོ། གཏེར་སྟོན་གྱི་འདས་ལོ།
རྩོམ་པ་པོའི་མིང་། རྩོམ་པ་པོའི་སྐྱེས་ལོ། རྩོམ་པ་པོའི་འདས་ལོ།
ལོ་ཙཱ་བའི་མིང་། ལོ་ཙཱ་བའི་སྐྱེས་ལོ། ལོ་ཙཱ་བའི་འདས་ལོ།
དཔེ་སྐྲུན་ལོ། དཔེ་སྐྲུན་ཁང་མིང་། TBRC information
བཅས་དབྱེ་བ་ཕྱེས་ཏེ་
གཤམ་གྱི་Dictionary format ནང་སྤྲད་རོགས། 
Dictionary format: 
{{
    'citation': {{
        '1':{{
            'book_title': 'book_title1',
            'alt_title': 'alt_title1',
            'volume': 'volume_info',
            'page': 'page_info,
            'line': 'line_info',
            'author': {{
                'name': 'author_name',
                'year_of_birth': 'yob',
                'year_of_death': 'yod'
            }},
            'terton': {{
                'name': 'terton_name',
                'year_of_birth': 'yob',
                'year_of_death': 'yod'
            }},
            'translator': {{
                'name': 'translator_name',
                'year_of_birth': 'yob',
                'year_of_death': 'yod'
            }},
            'editor': {{
                'name': 'editor_name',
                'year_of_birth': 'yob',
                'year_of_death': 'yod'
            }},
            'publisher': 'publisher_name',
            'publication_year': 'year',
            'collection': 'collection_name',
            'TBRC': 'TBRC_info',
            }},
         }}
}}
གལ་ཏེ་བརྗོད་པའི་ནང་གོང་གི་གནས་ཚུལ་གང་རུང་གསལ་སྟོན་བྱས་མེད་ན་སྟོང་པ་འཇོག་རོགས། 
བརྗོད་པ་:
{ciation_text}
"""
                            }
                        ]
                    }
                ]
            )
        citations = ai_response.content[0].text
        citations = citations.replace("'", '"')
        citations = citations.replace('"s', "'s")
        citations_dict = json.loads(citations)


    except Exception as e:
        print(f"Error processing citation: {e}")
    
    return citations_dict


if __name__ == "__main__":
    """
    The above code has been tested with all the corner cases and it is working fine.
    """
    corner_case_files = list(Path('./test/citation_corner_cases').glob('*.txt'))
    corner_case_files.sort()
    for file in corner_case_files[2:3]:
        citation_text = file.read_text()
        citations = parse_citations_with_claude(citation_text)
        citation_path = Path(f"./test/citation_corner_cases/results/{file.stem}.json")
        citation_path.write_text(json.dumps(citations, indent=4, ensure_ascii=False))