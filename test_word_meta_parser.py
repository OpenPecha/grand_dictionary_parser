from old_db_parser import is_key_word, is_new_word, get_register


def test_is_key_word():
    assert is_key_word("རྒྱུན་སྤྱོད།") == True
    assert is_key_word("") == False
    assert is_key_word("གསར་པ") == False
    

def test_is_new_word():
    assert is_new_word("མ་ཚིག་གསར་པ།") == True
    assert is_new_word("") == False
    assert is_new_word("གསར་པ") == False

def test_get_register():
    assert get_register("", "བརྡ་རྙིང་།") == "བརྡ་རྙིང་།"
    assert get_register("བརྡ་རྙིང་།", "") == "བརྡ་རྙིང་།"
    assert get_register("མངོན་བརྗོད།", "") == "མངོན་བརྗོད།"
    assert get_register("", "") == ""
    assert get_register("མངོན་བརྗོད།","བརྡ་རྙིང་།", ) == "མངོན་བརྗོད།"

if __name__ == '__main__':
    test_is_key_word()
    test_is_new_word()
    test_get_register()
    print("All tests passed!")