from utils import csv_to_df, get_new_df

def get_sense(explanations, notes):
    senses = {}
    return senses

def is_key_word(key_word):
    if "རྒྱུན་སྤྱོད" in key_word:
        return True
    return False

def is_new_word(new_word):
    if "མ་ཚིག་གསར་པ" in new_word:
        return True
    return False

def get_register(use, archaic):
    if use == "" and archaic:
        return archaic
    elif use:
        return use
    return ""



def get_new_word(row):
    sense = get_sense(row['explanation'], row['note'])
    new_word = {
        "word_id": row["wordindexid"],
        "lemma": row["word"],
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


def convert_to_new_db(df):
    for index, row in df.iterrows():
        new_word = get_new_word(row)
        save_new_word(new_word)


def parse_old_db(file_path):
    df = csv_to_df(file_path)
    columns =["wordindexid","word","explanation","note","key_word","origin","image","archaic","newword","use","noun_tayp","editor","editor_group","datetime","monlamitemploye",]
    new_df = get_new_df(df, columns)
    convert_to_new_db(new_df)
