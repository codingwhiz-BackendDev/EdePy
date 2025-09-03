from io import BytesIO
import tokenize
from token import NAME
from typing import Dict


# Base Yoruba -> Python mapping for keywords and common builtins
BASE_MAPPING: Dict[str, str] = {
    # Keywords
    "iṣẹ́": "def",            # function def
    "pada": "return",         # return
    "ti": "if",               # if
    "bibẹẹkọ": "else",        # else
    "bibẹẹkọ_ti": "elif",     # elif
    "nigbati": "while",       # while
    "fun": "for",             # for
    "ni": "in",               # in
    "and": "and",             # keep English when used
    "ati": "and",             # logical and
    "tabi": "or",             # logical or
    "kii_se": "not",          # not (ASCII-friendly)
    "kìíṣe": "not",           # not (accented)
    
    # Booleans / null
    "bẹẹni": "True",          # True
    "rárá": "False",          # False
    "rara": "False",          # False (alt)
    "ohunkohun": "None",      # None

    # Common builtins
    "so": "print",            # print
    "wọlé": "input",          # input
    "gigun": "len",           # len
}


def translate_yoruba(source_code: str, mapping: Dict[str, str] | None = None) -> str:
    """Translate Yorùbá-like Python into real Python using tokenize.

    Only NAME tokens that exactly match keys in the mapping are replaced.
    Indentation, strings, comments and non-NAME tokens are preserved.
    """
    effective_mapping = dict(BASE_MAPPING)
    if mapping:
        effective_mapping.update(mapping)

    token_stream = tokenize.tokenize(BytesIO(source_code.encode("utf-8")).readline)
    translated = []

    for tok in token_stream:
        # Replace only NAME tokens whose string is in the mapping
        if tok.type == NAME and tok.string in effective_mapping:
            tok = tokenize.TokenInfo(tok.type, effective_mapping[tok.string], tok.start, tok.end, tok.line)
        translated.append(tok)

    result = tokenize.untokenize(translated)
    if isinstance(result, bytes):
        return result.decode("utf-8")
    return result


def translate_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    return translate_yoruba(code)

