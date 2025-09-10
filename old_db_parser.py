import json
import difflib
import logging
from pathlib import Path
from utils import csv_to_df, get_new_df
from sense_parser import parse_senses_with_claude
from citation_parser import parse_citations_with_claude

logging.basicConfig(
    level=logging.INFO,
    filename='grand_dictionary.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_similarity_score(title, source):
    return difflib.SequenceMatcher(None, title, source).ratio()

def get_citation(citations, citation_source):
    citation = {}
    if citation_source == "" and citations:
        citation = citations['citation'][0]
    for citation_id, citation_info in citations['citation'].items():
        book_title = citation_info["book_title"]
        alt_title = citation_info["alt_title"]
        if get_similarity_score(book_title, citation_source) > 0.8:
            citation = citation_info
            break
        elif get_similarity_score(alt_title, citation_source) > 0.8:
            citation = citation_info
            break
    if citation == {} and citation_source:
        citation = {
            "book_title": citation_source
        }
    return citation, citation_id

def get_sense(word_id, word, explanations, notes):
    senses = {}
    citations = {}
    structured_senses = parse_senses_with_claude(word_id, word, explanations)
    if notes:
        citations = parse_citations_with_claude(word_id, word, notes)
    
    for sense_id, sense in structured_senses.items():
        description = sense["description"]
        pos_tag = sense["POS_tag"]
        example_sesntences = sense["example_sentence"]
        tag = sense["tag"]
        if sense['citation_text'] == "":
            citation = {}
        else:
            citation = get_citation(citations, sense['citation_source'])
        citation['citation_text'] = sense['citation_text']
        cur_sense = {
            "description": description,
            "pos_tag": pos_tag,
            "example_sesntences": example_sesntences,
            "tag": tag,
            "citation": citation
        }
        senses[sense_id] = cur_sense
    return senses

def is_key_word(key_word):
    if key_word:
        if "རྒྱུན་སྤྱོད" in str(key_word):
            return True
    return False

def is_new_word(new_word):
    if new_word:
        if "མ་ཚིག་གསར་པ" in str(new_word):
            return True
    return False

def get_register(use, archaic):
    if use == "" and archaic:
        return archaic
    elif use:
        return use
    return ""



def get_new_word(row):
    word = row["word"]
    word_id = row["wordindexid"]
    sense = get_sense(word_id, word, row['explanation'], row['note'])
    new_word = {
        "word_id": row["wordindexid"],
        "lemma": word,
        "origin": row["origin"],
        "sense": sense,
        "is_key_word": is_key_word(row["key_word"]),
        "is_new_word": is_new_word(row["newword"]),
        "register": get_register(row["use"], row["archaic"]),
        "editor": row["editor"],
        "editor_group": row["editor_group"],
        "datetime": row["datetime"],
        "monlamitemploye": row["monlamitemploye"],
    }

    return new_word

def save_new_word(new_word, batch_id):
    word_id = int(new_word["word_id"])
    Path(f'./data/new_db/{batch_id}/{word_id}.json').write_text(json.dumps(new_word, ensure_ascii=False, indent=2))


def convert_to_new_db(df, batch_id):
    Path(f'./data/new_db/{batch_id}').mkdir(parents=True, exist_ok=True)
    for index, row in df.iterrows():
        word_id = row["wordindexid"]
        if Path(f'./data/new_db/{batch_id}/{word_id}.json').exists():
            continue
        new_word = get_new_word(row)
        save_new_word(new_word, batch_id)
    


def parse_old_db(file_path):
    batch_id = file_path.stem
    df = csv_to_df(file_path)
    columns =["wordindexid","word","explanation","note","key_word","origin","image","archaic","newword","use","noun_tayp","editor","editor_group","datetime","monlamitemploye",]
    new_df = get_new_df(df, columns)
    convert_to_new_db(new_df, batch_id)

if __name__ == "__main__":
    # old_dict_dir = Path("./data/old_db")
    # old_dict_files = list(old_dict_dir.iterdir())
    # old_dict_files.sort()
    # for file_path in old_dict_files[:2]:
    #     parse_old_db(file_path)
    citations = Path("./test/citation_corner_cases/")
    
