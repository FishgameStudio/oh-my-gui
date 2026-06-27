"""
#### Welcome to module `Oh My Stylesheet`!
Convert OMS markup language to standard Qt QSS source code
OMS Unique Features (Different from raw QSS):
1. Unit suffix: px/em/pt, e.g width = 800px;
2. Color literal #hex / rgb(r,g,b) without quotes
3. Global reusable @style block + use keyword
4. Global variable $xxx constant cross all rules
5. Multi state chain Widget:hover:pressed {}
6. Rect group shorthand rect{ w=200px; fill=#333; }
7. Built-in true/false/None constant literals
8. Fixed @import preprocess file read bug
Syntax example:
```
# Global constant
$BG_COLOR = "#f0f0f0";
# Global reusable style
@style BaseBtn {
    width = 120px;
    height = 36px;
}
# Main style rule
Button submitBtn :hover:pressed {
    use BaseBtn;
    rect{ w=110px; h=34px; fill=#2266cc; }
    color = $BG_COLOR;
    border = #000000;
    visible = true;
}
# Wildcard support
any { opacity = 255; }
```
"""
from typing import TypeAlias as _TypeAlias
from enum import Enum as _Enum
from logging import info as _info, warning as _warning, error as _error, critical as _critical
from os.path import exists as _exists
from sys import exit as _exit

_info(f"module {__name__} loaded")

# Type Alias
QssString: _TypeAlias = str

class TokenType(_Enum):
    Identifier     = 0
    Number         = 1
    String         = 2
    Lpar           = 3   # (
    Rpar           = 4   # )
    Lsqb           = 5   # [
    Rsqb           = 6   # ]
    Lbrace         = 7
    Rbrace         = 8
    Colon          = 9
    Semi           = 10  # Semicolon
    Dot            = 11
    Comma          = 12
    At             = 13  # @ import / @style
    Eq             = 14
    Star           = 15
    HashColor      = 16  # #ff00ff hex color literal
    DollarVar      = 17  # $GlobalConst
    UnitSuffix     = 18  # px em pt
    Invalid        = 999

class Token:
    def __init__(self, type: TokenType, val: str) -> None:
        self.type = type
        self.val  = val
    @property
    def digitval(self) -> int:
        assert self.type == TokenType.Number, "digitval only for Number token"
        return int(self.val)

# Short alias same as original OMS code
tt: _TypeAlias = TokenType

# Char classification helpers
def _is_identifier_start(c: str) -> bool:
    return c.isalpha() or c == '_'
def _is_identifier_name(c: str) -> bool:
    return _is_identifier_start(c) or c.isdigit()
def _isspace(c: str) -> bool:
    return c.isspace()
def _isdigit(c: str) -> bool:
    return c.isdigit()

# Single char operator map
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

# constant literals
CONSTANTS = {
    'None': None,
    'true': True,
    'false': False
}

# OMS short widget name -> Qt QSS native widget class
WIDGET = {
    "Window":        "QMainWindow",
    "Application":   "QApplication",
    "App":           "QApplication",
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
    "Picture":       "QLabel",
    "Video":         "QVideoWidget",
    "SplashScreen":  "QSplashScreen",
    "any":           "*", 
    "all":           "*"
}

# Unit suffix support list
UNIT_LIST = ("px", "em", "pt")

def _isoperator(c: str) -> bool:
    return c in OP

# Limit of errors.
ERROR_LIMIT = 15

class ErrorLimitExceededError(Exception):
    """Error limit exceeded."""
    pass
class _Error:
    def __init__(self) -> None:
        self._cnt = 0
    def __iadd__(self, other: int) -> int:
        self._cnt += other
        if self._cnt > ERROR_LIMIT:
            _critical(f"FATAL: Error limit exceeded during parsing OMS")
            raise ErrorLimitExceededError()
        return self._cnt
ERRORS = _Error()

# ==== Lexer ====
def lexer(oms: str) -> list[Token]:
    global ERRORS
    """Lexer, support color/unit/$var"""
    line_buffer = []
    for raw_line in oms.splitlines():
        stripped_line = raw_line.strip()
        if stripped_line.startswith("@import "):
            path = stripped_line[8:].strip()
            if _exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        import_text = f.read()
                    line_buffer.append(import_text)
                    _info(f"Lexer Preprocess: loaded import file {path}")
                except Exception as e:
                    _error(f"Lexer Preprocess: read {path} failed: {str(e)}")
                    ERRORS += 1
            else:
                _warning(f"Lexer Preprocess: import file {path} not found")
        else:
            line_buffer.append(raw_line)
    full_src = "\n".join(line_buffer)

    token_list: list[Token] = []
    idx = 0
    src_len = len(full_src)
    while idx < src_len:
        c = full_src[idx]
        # Global constant $Identifier
        if c == "$":
            idx += 1
            var_buf = ""
            while idx < src_len and _is_identifier_name(full_src[idx]):
                var_buf += full_src[idx]
                idx += 1
            token_list.append(Token(tt.DollarVar, var_buf))
            continue
        # Hex color literal #ffffff
        elif c == "#":
            idx += 1
            color_buf = "#"
            while idx < src_len and full_src[idx] in "0123456789abcdefABCDEF":
                color_buf += full_src[idx]
                idx += 1
            token_list.append(Token(tt.HashColor, color_buf))
            continue
        # Comments start with //
        elif c == "/" and idx+1 < src_len and full_src[idx+1] == "/":
            idx += 2
            while idx < src_len and full_src[idx] != "\n":
                idx += 1
            continue
        # Identifier / Widget / attr name
        if _is_identifier_start(c):
            _info(f"Lexer char '{c}' matched Identifier")
            id_buf = ""
            while idx < src_len and _is_identifier_name(c):
                id_buf += c
                idx += 1
                if idx < src_len:
                    c = full_src[idx]
            token_list.append(Token(tt.Identifier, id_buf))
            continue
        # Number + unit suffix like 200px
        elif _isdigit(c):
            _info(f"Lexer char '{c}' matched Number")
            num_buf = ""
            while idx < src_len and _isdigit(c):
                num_buf += c
                idx += 1
                if idx < src_len:
                    c = full_src[idx]
            token_list.append(Token(tt.Number, num_buf))
            # Match trailing unit
            unit_buf = ""
            while idx < src_len and _is_identifier_name(full_src[idx]):
                unit_buf += full_src[idx]
                idx += 1
            if unit_buf in UNIT_LIST:
                token_list.append(Token(tt.UnitSuffix, unit_buf))
            continue
        # Single/Double quote string
        elif c in ('"', "'"):
            _info(f"Lexer quote '{c}' matched String")
            str_buf = ""
            quote_mark = c
            idx += 1
            if idx >= src_len:
                _error("Lexer unclosed string at EOF")
                ERRORS += 1
                continue
            c = full_src[idx]
            while idx < src_len and c != quote_mark:
                str_buf += c
                idx += 1
                if idx < src_len:
                    c = full_src[idx]
            idx += 1
            str_buf = str_buf.encode("unicode_escape").decode("ascii")
            token_list.append(Token(tt.String, str_buf))
            continue
        # Single char operator
        elif _isoperator(c):
            _info(f"Lexer char '{c}' matched Operator")
            token_list.append(Token(OP[c], c))
            idx += 1
            continue
        # Comment skip to newline
        elif c == "#":
            while idx < src_len and full_src[idx] != '\n':
                idx += 1
            continue
        # Whitespace skip
        elif _isspace(c):
            idx += 1
            continue
        # Unknown character
        else:
            _error(f"Lexer unknown char '{c}' at index {idx}")
            ERRORS += 1
            idx += 1
            continue
    return token_list

# ==== AST Type Definition ====
OMSAttrValue: _TypeAlias = str | int | None | bool
OMSAttrDict: _TypeAlias = dict[str, OMSAttrValue]

class OmsStyleBlock:
    """Global reusable @style block storage"""
    def __init__(self, name: str, attrs: OMSAttrDict):
        self.name = name
        self.attrs = attrs

class OmsRule:
    """Single style selector rule AST node"""
    def __init__(
        self,
        widget_short: str,
        states: list[str],
        attrs: OMSAttrDict,
        use_styles: list[str],
        rect_groups: OMSAttrDict
    ):
        self.widget_short = widget_short
        self.states = states
        self.attrs = attrs
        self.use_styles = use_styles
        self.rect_groups = rect_groups

# Full top-level AST bundle (store all global data)
class FullAST:
    def __init__(self):
        self.global_vars: dict[str, OMSAttrValue] = {}
        self.style_blocks: dict[str, OmsStyleBlock] = {}
        self.rules: list[OmsRule] = []

AST_Type: _TypeAlias = FullAST

# ==== Recursive Parser ====
def ast(tokens: list[Token]) -> AST_Type:
    """Parser"""
    global ERRORS
    idx: int = 0
    token_count = len(tokens)
    full_ast = FullAST()

    # Cursor helper functions
    def curr() -> Token:
        nonlocal idx
        global ERRORS
        if idx >= token_count:
            _error("Parser curr() out of token range")
            ERRORS += 1
            return Token(tt.Invalid, "")
        return tokens[idx]
    def next_tok() -> Token:
        nonlocal idx
        global ERRORS
        idx += 1
        if idx >= token_count:
            _error("Parser next_tok() EOF")
            ERRORS += 1
            return Token(tt.Invalid, "")
        return tokens[idx]
    def prev() -> Token:
        nonlocal idx
        idx -= 1
        return tokens[idx]
    def peek_next() -> Token:
        nonlocal idx
        if idx + 1 >= token_count:
            return Token(tt.Invalid, "")
        return tokens[idx + 1]

    def parse_value() -> OMSAttrValue:
        global ERRORS
        """Parse all supported value types"""
        val_t = curr()
        val: OMSAttrValue = None
        if val_t.type == tt.Number:
            val = val_t.digitval
            # Skip unit suffix token
            if peek_next().type == tt.UnitSuffix:
                next_tok()
        elif val_t.type == tt.String:
            val = val_t.val
        elif val_t.type == tt.HashColor:
            val = val_t.val
        elif val_t.type == tt.DollarVar:
            var_name = val_t.val
            val = full_ast.global_vars.get(var_name, f"${var_name}")
        elif val_t.type == tt.Identifier:
            if val_t.val in CONSTANTS:
                val = CONSTANTS[val_t.val]
            else:
                val = val_t.val
        else:
            _error(f"Parser invalid value token type {val_t.type}")
            ERRORS += 1
        next_tok()
        return val

    def parse_block_inner() -> tuple[OMSAttrDict, OMSAttrDict, list[str]]:
        global ERRORS
        """Parse content inside {}: attr, use style, rect group shorthand"""
        nonlocal idx
        attrs: OMSAttrDict = {}
        rect_attrs: OMSAttrDict = {}
        use_list: list[str] = []
        while idx < token_count and curr().type != tt.Rbrace:
            ct = curr()
            # use StyleName; syntax
            if ct.type == tt.Identifier and ct.val == "use":
                next_tok()
                style_name = curr().val
                use_list.append(style_name)
                next_tok()
                if curr().type == tt.Semi:
                    next_tok()
                continue
            # rect { w=xx; fill=xx; } group shorthand
            if ct.type == tt.Identifier and ct.val == "rect":
                next_tok()
                if curr().type != tt.Lbrace:
                    _error("rect shorthand must follow {")
                    ERRORS += 1
                    idx += 1
                    continue
                next_tok()
                while idx < token_count and curr().type != tt.Rbrace:
                    r_key = curr().val
                    next_tok()
                    if curr().type != tt.Eq:
                        _error(f"rect attr {r_key} missing =")
                        ERRORS += 1
                        idx += 1
                        continue
                    next_tok()
                    r_val = parse_value()
                    if curr().type == tt.Semi:
                        next_tok()
                    rect_attrs[r_key] = r_val
                next_tok()
                continue
            # Normal attr = value;
            if ct.type == tt.Identifier and peek_next().type == tt.Eq:
                attr_key = ct.val
                next_tok()
                next_tok() # skip =
                attr_val = parse_value()
                if curr().type == tt.Semi:
                    next_tok()
                if attr_key in attrs:
                    _warning(f"Parser duplicate attr '{attr_key}'")
                attrs[attr_key] = attr_val
                _info(f"Parser set attr [{attr_key}] = {attr_val}")
                continue
            # Unknown token inside block
            _error(f"Parser unexpected token '{ct.val}' inside block")
            ERRORS += 1
            idx += 1
        return attrs, rect_attrs, use_list

    def parse_global_var():
        """Parse $VAR_NAME = value;"""
        global ERRORS
        var_name = curr().val
        next_tok()
        if curr().type != tt.Eq:
            _error(f"Global var ${var_name} missing = assignment")
            ERRORS += 1
            return
        next_tok()
        var_val = parse_value()
        if curr().type == tt.Semi:
            next_tok()
        full_ast.global_vars[var_name] = var_val
        _info(f"Parser register global constant ${var_name} = {var_val}")

    def parse_style_def():
        global ERRORS
        """Parse @style Name { ... }"""
        next_tok() # skip @
        next_tok() # skip style identifier
        style_name = curr().val
        next_tok()
        if curr().type != tt.Lbrace:
            _error(f"@style {style_name} missing opening {{")
            ERRORS += 1
            return
        next_tok()
        style_attrs, _, _ = parse_block_inner()
        next_tok()
        full_ast.style_blocks[style_name] = OmsStyleBlock(style_name, style_attrs)
        _info(f"Parser register global style [{style_name}]")

    def parse_rule():
        global ERRORS
        """Parse WidgetName[:state1:state2] { ... } style rule"""
        widget_short = curr().val
        next_tok()
        # Parse multi state chain :hover:pressed
        states = []
        while curr().type == tt.Colon:
            next_tok()
            state_tok = curr()
            if state_tok.type != tt.Identifier:
                _error("Parser invalid state identifier after colon")
                ERRORS += 1
                break
            states.append(state_tok.val)
            next_tok()
        # Expect opening brace
        if curr().type != tt.Lbrace:
            _error(f"Parser widget {widget_short} missing {{")
            ERRORS += 1
            return
        next_tok()
        rule_attrs, rect_groups, use_styles = parse_block_inner()
        next_tok()
        rule = OmsRule(widget_short, states, rule_attrs, use_styles, rect_groups)
        full_ast.rules.append(rule)
        _info(f"Parser finish rule {widget_short} states={states}")

    # Top level main loop
    while idx < token_count:
        current_tok = curr()
        # Global $ variable
        if current_tok.type == tt.DollarVar:
            parse_global_var()
            continue
        # @style definition
        if current_tok.type == tt.At and peek_next().val == "style":
            parse_style_def()
            continue
        # Widget selector rule
        if current_tok.type == tt.Identifier and current_tok.val in WIDGET:
            parse_rule()
            continue
        idx += 1
    return full_ast

# ==== AST -> QSS Converter ====
def convert(ast: AST_Type) -> QssString:
    """Convert Full AST to standard Qt QSS text"""
    qss_header = [
        "// @generated by OMS Converter, oh-my-gui",
        "// License: MIT",
        ""
    ]
    output_lines = qss_header

    def merge_rule_attrs(rule: OmsRule) -> OMSAttrDict:
        """Merge imported @style attrs + local attrs + rect shorthand"""
        merged = {}
        # Apply global style first
        for style_name in rule.use_styles:
            if style_name in ast.style_blocks:
                merged.update(ast.style_blocks[style_name].attrs)
        # Local attribute override style
        merged.update(rule.attrs)
        # Rect shorthand mapping
        rect_map = {
            "w": "width",
            "h": "height",
            "x": "x",
            "y": "y",
            "fill": "background-color"
        }
        for short_key, val in rule.rect_groups.items():
            if short_key in rect_map:
                merged[rect_map[short_key]] = val
        return merged

    def format_value(val) -> str:
        """Format OMS value to valid QSS literal"""
        if val is None:
            return ""
        elif isinstance(val, bool):
            return "1" if val else "0"
        elif isinstance(val, int):
            return str(val)
        elif isinstance(val, str):
            # Hex color direct output without quotes
            if val.startswith("#"):
                return val
            # Global constant reference
            if val.startswith("$"):
                const_name = val[1:]
                raw_val = ast.global_vars.get(const_name, "")
                if isinstance(raw_val, str) and raw_val.startswith("#"):
                    return raw_val
                return f'"{raw_val}"'
            return f'"{val}"'
        return str(val)

    # Render all style rules
    for rule in ast.rules:
        qss_widget = WIDGET.get(rule.widget_short, rule.widget_short)
        # Combine multi state selector
        state_suffix = ""
        if rule.states:
            state_suffix = ":" + ":".join(rule.states)
        merged_attrs = merge_rule_attrs(rule)
        attr_lines: list[str] = []
        for attr_name, attr_val in merged_attrs.items():
            formatted_val = format_value(attr_val)
            attr_lines.append(f"    {attr_name}: {formatted_val};")
        # Assemble full rule text
        rule_text = [
            f"{qss_widget}{state_suffix} {{",
            *attr_lines,
            "}"
        ]
        output_lines.extend(rule_text)
        output_lines.append("")
    return "\n".join(output_lines)

# Main entry function
def convert_oms_to_qss(oms: str) -> QssString:
    """Parse OMS source and output standard QSS string"""
    token_stream = lexer(oms)
    full_ast_tree = ast(token_stream)
    qss_result = convert(full_ast_tree)
    return qss_result

# Demo Test Entry
if __name__ == "__main__":
    test_oms_code = """
# Global constant
$MAIN_BG = "#f8f8f8";
# Global reusable style block
@style DefaultButton {
    width = 130px;
    height = 38px;
    font_size = 14pt;
}
# Window root style
Window {
    rect{ w=1200px; h=800px; fill=$MAIN_BG; }
}
# Multi state button
Button :hover:pressed {
    use DefaultButton;
    color = #ffffff;
    border = #0066ff;
    visible = true;
}
# Wildcard any widget
any {
    opacity = 255;
}
"""
    generated_qss = convert_oms_to_qss(test_oms_code)
    print(generated_qss)