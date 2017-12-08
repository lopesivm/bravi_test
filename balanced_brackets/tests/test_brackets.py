from balanced_brackets import validate_bracket_input

def test_symmetric_input_success():
    input = '[({})]'
    assert validate_bracket_input(input)

def test_asymmetric_input_success():
    input = '[](){}'
    assert validate_bracket_input(input)

def test_asymmetric_enclosed_input_success():
    input = '[[](){}()](){}'
    assert validate_bracket_input(input)

def test_odd_characters_failure():
    input = '(){}[]]'
    assert not validate_bracket_input(input)

def test_even_characters_invalid_pattern_failure():
    input = '{([))}'
    assert not validate_bracket_input(input)

def test_invalid_characters_failure():
    input = '{([aa])}'
    assert not validate_bracket_input(input)