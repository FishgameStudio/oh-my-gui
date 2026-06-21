"""
#### Welcome to module `Oh My Stylesheet`!
Here is an example to use OMS:
```
# Comments start with '#'
XXXWidget {
    attribute1 = 123456;
    attribute2 = "hello world";
    attribute3 = None;
}

```
"""

from typing import TypeAlias as _TypeAlias
from enum import Enum as _Enum
from logging import info as _info, warning as _warning, error as _error

_info(f"module {__name__} loaded")
 
QssString: _TypeAlias = str

class TokenType(_Enum):
    Identifier     = 0
    Number         = 1
    String         = 2
    Lpar           = 3   # Left  parenthesis
    Rpar           = 4   # Right parenthesis
    Lsqb           = 5   # Left  Square bracket
    Rsqb           = 6   # Right Square bracket
    Lbrace         = 7
    Rbrace         = 8
    Colon          = 9
    Semi           = 10  # Semicolon
    Dot            = 11
    Comma          = 12
    At             = 13  # @
    Eq             = 14
    Invalid        = 999
class Token:
    def __init__(self, type: TokenType, val: str) -> None:
        self.type = type
        self.val  = val
    @property
    def digitval(self) -> int:
        assert self.type == TokenType.Number, "digitval only for Number token"
        return int(self.val)
tt: _TypeAlias = TokenType


def _is_identifier_start(c: str) -> bool:
    return c.isalpha() or c == '_'
def _is_identifier_name(c: str) -> bool:
    return _is_identifier_start(c) or c.isdigit()
def _isspace(c: str) -> bool:
    return c.isspace()
def _isdigit(c: str) -> bool:
    return c.isdigit()

OP = {
    '(': tt.Lpar, 
    ')': tt.Rpar, 
    '[': tt.Lsqb, 
    ']': tt.Rsqb, 
    '{': tt.Lbrace, 
    '}': tt.Rbrace, 
    ':': tt.Colon, 
    ';': tt.Semi, 
    '.': tt.Dot, 
    ',': tt.Comma, 
    '@': tt.At
}
CONSTANTS = {
    'None': None, 
}
WIDGET = {
    "Text":          "QLabel",
    "Button":        "QPushButton",
    "InputEntry":    "QLineEdit",
    "PasswordEntry": "QLineEdit",
    "RadioButton":   "QRadioButton",
    "ComboBox":      "QComboBox",
    "ListWidget":    "QListWidget",
    "Table":         "QTableWidget",
    "Tree":          "QTreeWidget",
    "Slider":        "QSlider",
    "Progress":      "QProgressBar",
    "Dial":          "QDial",
    "IntegerEntry":  "QSpinBox",
    "DoubleEntry":   "QDoubleSpinBox",
    "TextEdit":      "QTextEdit",
    "Canvas":        "QGraphicsView",
    # Picture mixes two types of internal objects(QSvgWidget, QPixmap)
    "Picture":       "QLabel",     
    "Video":         "QVideoWidget",
    "SplashScreen":  "QSplashScreen"
}
def _isoperator(c: str) -> bool:
    return c in OP

def lexer(oms: str) -> list[Token]:
    """The lexer."""
    res = []
    idx = 0
    while idx < len(oms):
        c = oms[idx]
        # Match the char
        if _is_identifier_start(c):
            _info(f"Char '{c}' matched tt.Identifier")
            id_name = ""
            while idx < len(oms) and _is_identifier_name(c):
                id_name += c
                idx += 1
                if idx < len(oms):
                    c = oms[idx]
                else:
                    break
            res.append(Token(tt.Identifier, id_name))
            continue
        elif _isdigit(c):
            _info(f"Char '{c}' matched tt.Number")
            num_str = ""
            while idx < len(oms) and _isdigit(c):
                num_str += c
                idx += 1
                if idx < len(oms):
                    c = oms[idx]
                else:
                    break
            res.append(Token(tt.Number, num_str))
            continue
        elif c == '"' or c == '\'':
            _info(f"Char '{c}' matched tt.String")
            s = ""
            quote_mark = c
            idx += 1
            c = oms[idx] if idx < len(oms) else ""
            while idx < len(oms) and c != quote_mark:
                s += c
                idx += 1
                c = oms[idx] if idx < len(oms) else ""
            idx += 1
            s = s.encode("unicode_escape").decode("ascii")
            res.append(Token(tt.String, s))
            continue
        elif _isoperator(c):
            _info(f"Char '{c}' matched Operator")
            res.append(Token(OP[c], c))
            idx += 1
            continue
        elif c == '#':
            # Comments
            while idx < len(oms) and oms[idx] != '\n':
                idx += 1
            continue
        elif _isspace(c):
            # Skip whitespaces
            idx += 1
            continue
        else:
            _error(f"Unknown token {c} at index {idx}")
            idx += 1
            continue
    return res

# This means: dict[tuple[object_name, object_status], dict[attr_name, value]]
AST_Type: _TypeAlias = dict[tuple[str, str], dict[str, str | int | None]]

def ast(tokens: list[Token]) -> AST_Type:
    """Build AST"""
    idx = 0
    def next_tok() -> Token:
        nonlocal idx
        idx += 1
        if idx >= len(tokens):
            _error("Parser: token stream out of range")
            return Token(tt.Invalid, "")
        return tokens[idx]
    def curr() -> Token:
        nonlocal idx
        if idx >= len(tokens):
            _error("Parser: token stream out of range when read curr")
            return Token(tt.Invalid, "")
        return tokens[idx]
    def prev() -> Token:
        nonlocal idx
        idx -= 1
        return tokens[idx]
    in_decl = False   # In `xxx { ... }`
    curr_object = "" # The current object name for decl
    curr_attributes: dict[str, str | int | None] = {} # Current attributes of the current object
    ast: AST_Type = {}
    while idx < len(tokens):
        tok = tokens[idx]
        if (not in_decl) and tok.type != tt.Identifier:
            _error(f"Parser: Expect declaration at idx {idx}")
            idx += 1
            continue
        elif (not in_decl) and tok.type == tt.Identifier:
            in_decl = True
            # curr() is:
            # `xxx { ... }`
            #  ^^^~~~~~~~~
            curr_object = tok.val
            curr_status = "default" # The current status of the object
            curr_attributes = {}
            if curr_object not in WIDGET:
                _error(f"Parser: unknown object '{curr_object}'")
                continue
            if curr_object in ast:
                _warning(f"Parser: object '{curr_object}' duplicated")
            next_t = next_tok()
            if next_t.type == tt.Colon:
                # current:
                # xxx: status { ... }
                # ~~~^~~~~~~~~~~~~~~~
                status_tok = next_tok()
                if status_tok.type != tt.Identifier:
                    _error(f"Parser: Expect identifier at idx {idx}")
                    idx += 1
                    continue
                curr_status = status_tok.val
                next_t = next_tok()

            if next_t.type != tt.Lbrace:
                _error(f"Parser: Expect '{{' at idx {idx}")
                idx += 1
                continue
            while idx < len(tokens) and curr().type != tt.Rbrace:
                curr_tok = curr()
                if curr_tok.type == tt.Identifier:
                    attr_name = curr_tok.val
                    if attr_name in curr_attributes:
                        _warning(f"Parser: Attribute '{attr_name}' duplicated at idx {idx}")
                    # Enter `xxx_attr = xxx_value;`
                    colon_t = next_tok()
                    if colon_t.type != tt.Eq:
                        _error(f"Parser: Expect '=' at idx {idx}")
                    # Now the next() will return: 
                    # `xxx_attr = xxx_value;`
                    # ~~~~~~~~~~~^^^^^^^^^~
                    n = next_tok()
                    val: str | int | None = None
                    if n.type not in (tt.Number, tt.String, tt.Identifier):
                        _error(f"Parser: Expect value at idx {idx}")
                    elif n.type == tt.Number:
                        val = n.digitval
                    elif n.type == tt.String:
                        val = n.val
                    elif n.type == tt.Identifier:
                        # Find constants
                        if n.val not in CONSTANTS:
                            _error(f"Parser: Unknown identifier {n.val} at idx {idx}")
                        else:
                            val = CONSTANTS[n.val]
                    # Now the next() will return: 
                    # `xxx_attr = xxx_value;`
                    # ~~~~~~~~~~~~~~~~~~~~^
                    semi_t = next_tok()
                    if semi_t.type != tt.Semi:
                        _warning(f"Parser: Expect ';' at idx {idx}")
                    _info(f"Parser: attribute '{attr_name}' from '{curr_object}' set as value '{val}'")
                    curr_attributes[attr_name] = val
                else:
                    _error(f"Parser: Expect attribute identifier at idx {idx}")
                idx += 1
            _info(f"Parser: attribute of object '{curr_object}' with status '{curr_status}' has been set")
            ast[curr_object, curr_status] = curr_attributes
            in_decl = False
        idx += 1
    return ast

def convert(ast: AST_Type) -> QssString:
    """Convert ast to QSS"""
    res = "// @generated by OMS Converter, oh-my-gui\n// Lincense: MIT\n"
    objects: list[str] = []
    for obj, attributes in ast.items():
        attrs: list[str]   = []
        for attr, val in attributes.items():
            if val is None:
                val_str = ""
            elif isinstance(val, int):
                val_str = str(val)
            else:
                val_str = f'"{val}"'
            curr_attr_string = f"{attr}: {val_str}; \n"
            attrs.append(curr_attr_string)
        obj_name   = WIDGET[obj[0]] if obj[0] in WIDGET else obj[0]
        obj_status = obj[1]
        curr_object_string = f"""
{obj_name}:{obj_status} {{\n
{'    '.join(attrs)}\n
}}\n
"""
        objects.append(curr_object_string)
    res = "\n".join(objects)
    return res

def convert_oms_to_qss(oms: str) -> QssString:
    """Parse OMS(Oh my stylesheet) and convert to QSS."""
    return convert(ast(lexer(oms)))