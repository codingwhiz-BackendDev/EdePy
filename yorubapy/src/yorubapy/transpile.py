from io import BytesIO
import tokenize
from token import NAME
from typing import Dict
import sys


# Base Yoruba -> Python mapping for keywords and common builtins
# Using plain (non-accented) characters for easier typing
BASE_MAPPING: Dict[str, str] = {
    # Keywords
    "ise": "def",             # function def (was iṣẹ́)
    "pada": "return",         # return
    "ti": "if",               # if
    "bibeeko": "else",        # else (was bibẹẹkọ)
    "bibeeko_ti": "elif",     # elif (was bibẹẹkọ_ti)
    "nigbati": "while",       # while
    "fun": "for",             # for
    "ni": "in",               # in
    "and": "and",             # keep English when used
    "ati": "and",             # logical and
    "tabi": "or",             # logical or
    "kii_se": "not",          # not (ASCII-friendly)
    "gbeyanju": "try",        # try (was gbìyànjú)
    "mu": "except",            # except
    "keyin": "finally",        # finally (was kẹ̀yìn)
    "da": "break",             # break
    "tesiwaju": "continue",    # continue (was tẹ̀síwájú)
    "kilasi": "class",         # class
    "iru": "type",             # type
    "fi": "with",              # with
    "je": "is",                # is (was jẹ́)
    "kii_se_ni": "is not",     # is not (was kii_se)
    
    # Booleans / null
    "beeni": "True",           # True (was bẹẹni)
    "rara": "False",           # False (was rárá)
    "ohunkohun": "None",       # None

    # Common builtins
    "so": "print",             # print
    "wole": "input",           # input
    "gigun": "len",            # len
    "akooke": "str",           # str (was akọọlẹ)
    "nomb": "int",             # int function (was nọ́mbà)
    "nomb_ona": "float",       # float function (was nọ́mbà ọ̀nà)
    "akojo": "list",           # list (was àkójọ)
    "awon_oro": "dict",        # dict (was àwọn ọ̀rọ̀)
    "se": "do",                # do (placeholder for custom functions)
    "se_ni": "make",           # make (placeholder for constructors)
    "ka": "enumerate",         # enumerate
    "fi": "open",              # open file
    "pa": "close",             # close file
    "ka_faiili": "read",       # read file
    "ko_si_faiili": "write",   # write to file
}


def translate_error_message(error_msg: str) -> str:
    """Translate common Python error messages to Yorùbá."""
    error_mapping = {
        "NameError": "Asise Oruko:",
        "TypeError": "Asise Iru:",
        "ValueError": "Asise Iyi:",
        "IndexError": "Asise Ipin:",
        "KeyError": "Asise Ile:",
        "AttributeError": "Asise Asa:",
        "SyntaxError": "Asise Isoro:",
        "IndentationError": "Asise Iduro:",
        "ZeroDivisionError": "Asise Pinya:",
        "FileNotFoundError": "Faiili Ko Si:",
        "PermissionError": "Asise Iya:",
        "ModuleNotFoundError": "Moduulu Ko Si:",
        "ImportError": "Asise Igbewole:",
        "RuntimeError": "Asise Isise:",
        "Exception": "Asise:",
        "Error": "Asise:",
        "Traceback": "Itan Asise:",
        "line": "ona",
        "in": "ninu",
        "module": "moduulu",
        "function": "ise",
        "class": "kilasi",
        "method": "ona",
        "attribute": "asa",
        "argument": "oro",
        "parameter": "oro",
        "variable": "oro",
        "string": "oro",
        "integer": "nomb",
        "float": "nomb ona",
        "list": "akojo",
        "dictionary": "awon oro",
        "tuple": "akojo ti ko see yi",
        "set": "akojo ti ko see yi",
        "boolean": "oro ti o je beeni tabi rara",
        "None": "ohunkohun",
        "True": "beeni",
        "False": "rara",
    }
    
    translated = error_msg
    for english, yoruba in error_mapping.items():
        translated = translated.replace(english, yoruba)
    return translated


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


def translate_and_run_with_yoruba_errors(source_code: str, filename: str = "<yorubapy>") -> tuple[str, int]:
    """Translate Yorùbá code and run it with Yorùbá error messages."""
    translated = translate_yoruba(source_code)
    
    try:
        exec(compile(translated, filename, "exec"))
        return translated, 0
    except Exception as e:
        # Get the original traceback
        import traceback
        tb = traceback.format_exc()
        
        # Translate error messages to Yorùbá
        yoruba_tb = translate_error_message(tb)
        
        # Print Yorùbá error message
        print(f"Asise ninu koodu Yoruba:\n{yoruba_tb}", file=sys.stderr)
        
        return translated, 1


def translate_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    return translate_yoruba(code)

