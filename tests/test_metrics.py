from openscan.metrics import cer, edit_distance, normalize, wer


def test_exact_text_has_zero_error():
    assert cer("hola mundo", "hola mundo") == 0.0
    assert wer("hola mundo", "hola mundo") == 0.0


def test_single_typo_is_counted():
    assert cer("gato", "pato") == 0.25
    assert wer("gato", "pato") == 1.0


def test_missing_reference_is_unknown_not_zero():
    assert cer(None, "texto inventado") is None
    assert wer("", "texto inventado") is None


def test_whitespace_is_normalized():
    assert normalize(" hola\n\nmundo  ") == "hola mundo"
    assert cer("hola\nmundo", "hola   mundo") == 0.0


def test_levenshtein_distance():
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("", "a") == 1
