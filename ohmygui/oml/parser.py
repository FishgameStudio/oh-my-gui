"""
#### Welcome to module `Oh My Modeling Language`! OML
Convert OML markup language to standard Qt QML source code
OML Unique Features (Different from raw QML):
1. Unit suffix: px/em/vw/vh, e.g width = 800px;
2. Color literal #hex / rgb(r,g,b) without quotes
3. Global reusable @style block + use keyword
4. Parametric @template component macro
5. Global variable $xxx constant
6. Group attr shorthand rect{ w=200px; fill=#fff; }
7. Signal arrow bind: onClick -> func::slot;
8. Multi state chain Widget:hover:pressed {}
9. True/False built-in constant, align with None
10. @meta header metadata block
Syntax example:
# Global constant
$WIN_TITLE = "OML Demo";
# Global reusable style
@style BaseButton {
    width = 120px;
    height = 36px;
}
# Param template macro
@template TextLabel(txt, font_sz) {
    Text {
        text = txt;
        font_size = font_sz;
    }
}
# Meta info
@meta {
    version = "1.0";
    author = "Fishgame Studio";
}
# Main Window
Window MainWin {
    width = 960px;
    height = 720px;
    title = $WIN_TITLE;
    color = #f5f5f5;
    rect{ w=900px; h=600px; fill=rgb(30,30,30); }
    # Reuse style
    Button submitBtn :hover:pressed {
        use BaseButton;
        text = "Confirm";
        onClick -> app::onSubmit;
    }
    # Use template macro
    TextLabel("Hello OML", 24em);
}
# Wildcard
any Item { opacity = 255; }
"""
from typing import Any, Literal, LiteralString, TypeAlias as _TypeAlias
from enum import Enum as _Enum
from logging import info as _info, warning as _warning, error as _error, critical as _critical
from os.path import exists as _exists

_info(f"module {__name__} loaded")

# Type Alias
QmlString: _TypeAlias = str
TokenTypeAlias: _TypeAlias = "TokenType"

class TokenType(_Enum):
    Identifier     = 0
    Number         = 1
    String         = 2
    Lpar           = 3   # (
    Rpar           = 4   # )
    Lsqb           = 5   # [
    Rsqb           = 6   # ]
    Lbrace         = 7   # {
    Rbrace         = 8   # }
    Colon          = 9   # :
    Semi           = 10  # ;
    Dot            = 11  # .
    Comma          = 12  # ,
    At             = 13  # @ import / @style / @template / @meta
    Eq             = 14  # = assign
    Star           = 15  # * wildcard
    DoubleColon    = 16  # :: func separator
    Arrow          = 17  # -> signal bind
    HashColor      = 18  # #ff00ff hex color
    DollarVar      = 19  # $GlobalVar
    UnitSuffix     = 20  # px em vw vh
    Invalid        = 999

class Token:
    def __init__(self, type: TokenType, val: str) -> None:
        self.type = type
        self.val  = val
    @property
    def digitval(self) -> int:
        assert self.type == TokenType.Number, "digitval only for Number token"
        return int(self.val)

# Short alias same as your OMS code
tt: _TypeAlias = TokenType

# Char classification helpers (copy OMS implementation)
def _is_identifier_start(c: str) -> bool:
    return c.isalpha() or c == '_'
def _is_identifier_name(c: str) -> bool:
    return _is_identifier_start(c) or c.isdigit()
def _isspace(c: str) -> bool:
    return c.isspace()
def _isdigit(c: str) -> bool:
    return c.isdigit()

# Single char operator map, extend DoubleColon / Arrow for OML unique syntax
OP: dict[str, Any] = {
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
    '@': tt.At,
    '=': tt.Eq,
    '*': tt.Star,
    '-': None,
    '>': None
}

# OML exclusive built-in constants
CONSTANTS: dict[str, Any] = {
    'None': None,
    'true': True,
    'false': False
}

# OML short name -> QML native Qt component type
COMPONENT_MAP: dict[str, str] = {
    "Window":        "Window",
    "Application":   "ApplicationWindow",
    "App":           "ApplicationWindow",
    "Text":          "Text",
    "Button":        "Button",
    "InputEntry":    "TextField",
    "PasswordEntry": "TextField",
    "RadioButton":   "RadioButton",
    "ComboBox":      "ComboBox",
    "ListWidget":    "ListView",
    "Table":         "TableView",
    "Tree":          "TreeView",
    "Slider":        "Slider",
    "Progress":      "ProgressBar",
    "Dial":          "Dial",
    "IntegerEntry":  "SpinBox",
    "DoubleEntry":   "DoubleSpinBox",
    "TextEdit":      "TextEdit",
    "Canvas":        "Canvas",
    "Picture":       "Image",
    "Video":         "VideoOutput",
    "SplashScreen":  "SplashScreen",
    "Item":          "Item",
    "Rectangle":     "Rectangle",
    "any":           "*", 
    "all":           "*"
}

# OML keyword exclusive
OML_KEYWORDS: dict[str, str] = {
    "use": "use",
    "style": "style",
    "template": "template",
    "meta": "meta",
    "rect": "rect"
}

# Unit suffix list
UNIT_LIST: tuple[Literal['px'], Literal['em'], Literal['vw'], Literal['vh']] = ("px", "em", "vw", "vh")

def _isoperator(c: str) -> bool:
    return c in OP

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

# ==== Lexer (Enhanced with OML unique token parse) ====
def lexer(oml: str) -> list[Token]:
    """OML Lexer, preprocess @import, tokenize raw text + OML exclusive syntax"""
    global ERRORS
    # Preprocess @import line replace file content
    line_buffer: list[Any] = []
    for line in oml.splitlines():
        stripped: str = line.strip()
        if stripped.startswith("@import "):
            path: str = stripped[8:].strip()
            if _exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        import_content = f.read()
                    line_buffer.append(import_content)
                    _info(f"OML Lexer Preprocess: import file {path} loaded")
                except Exception as e:
                    _error(f"OML Lexer Preprocess: read {path} failed: {str(e)}")
                    ERRORS += 1
                    line_buffer.append("")
            else:
                _warning(f"OML Lexer Preprocess: import file {path} not found")
                line_buffer.append("")
        else:
            line_buffer.append(line)
    raw_src: LiteralString = "\n".join(line_buffer)

    token_list: list[Any] = []
    idx = 0
    src_len: int = len(raw_src)
    while idx < src_len:
        c: LiteralString = raw_src[idx]
        # Global variable $Identifier
        if c == "$":
            idx += 1
            var_buf = ""
            while idx < src_len and _is_identifier_name(raw_src[idx]):
                var_buf += raw_src[idx]
                idx += 1
            token_list.append(Token(tt.DollarVar, var_buf))
            continue
        # Hex color literal #ffffff
        elif c == "#":
            idx += 1
            color_buf = "#"
            while idx < src_len and raw_src[idx] in "0123456789abcdefABCDEF":
                color_buf += raw_src[idx]
                idx += 1
            token_list.append(Token(tt.HashColor, color_buf))
            continue
        # Comments start with //
        elif c == "/" and idx+1 < src_len and raw_src[idx+1] == "/":
            idx += 2
            while idx < src_len and raw_src[idx] != "\n":
                idx += 1
            continue
        # Identifier / Component / attr name / keyword
        if _is_identifier_start(c):
            _info(f"OML Lexer char '{c}' matched Identifier")
            id_buf = ""
            while idx < src_len and _is_identifier_name(c):
                id_buf += c
                idx += 1
                if idx < src_len:
                    c = raw_src[idx]
            token_list.append(Token(tt.Identifier, id_buf))
            continue
        # Number + unit suffix (800px / 24em)
        elif _isdigit(c):
            _info(f"OML Lexer char '{c}' matched Number")
            num_buf = ""
            while idx < src_len and _isdigit(c):
                num_buf += c
                idx += 1
                if idx < src_len:
                    c = raw_src[idx]
            token_list.append(Token(tt.Number, num_buf))
            # Check follow unit suffix
            unit_buf = ""
            while idx < src_len and _is_identifier_name(raw_src[idx]):
                unit_buf += raw_src[idx]
                idx += 1
            if unit_buf in UNIT_LIST:
                token_list.append(Token(tt.UnitSuffix, unit_buf))
            continue
        # String quote single/double
        elif c in ('"', "'"):
            _info(f"OML Lexer quote '{c}' matched String")
            str_buf = ""
            quote_mark: Literal['"', '\''] = c
            idx += 1
            if idx >= src_len:
                _error("OML Lexer unclosed string literal at EOF")
                ERRORS += 1
                continue
            c = raw_src[idx]
            while idx < src_len and c != quote_mark:
                str_buf += c
                idx += 1
                if idx < src_len:
                    c = raw_src[idx]
            idx += 1
            # escape unicode same as OMS
            str_buf: str = str_buf.encode("unicode_escape").decode("ascii")
            token_list.append(Token(tt.String, str_buf))
            continue
        # Double colon :: func separator special handle
        elif c == ":" and idx + 1 < src_len and raw_src[idx+1] == ":":
            _info("OML Lexer matched DoubleColon ::")
            token_list.append(Token(tt.DoubleColon, "::"))
            idx += 2
            continue
        # Arrow -> signal bind
        elif c == "-" and idx + 1 < src_len and raw_src[idx+1] == ">":
            _info("OML Lexer matched Arrow ->")
            token_list.append(Token(tt.Arrow, "->"))
            idx += 2
            continue
        # Single char operator
        elif _isoperator(c):
            if OP[c] is not None:
                _info(f"OML Lexer char '{c}' matched Operator")
                token_list.append(Token(OP[c], c))
            idx += 1
            continue
        # # comment skip to newline
        elif c == "#":
            while idx < src_len and raw_src[idx] != "\n":
                idx += 1
            continue
        # whitespace skip
        elif _isspace(c):
            idx += 1
            continue
        # unknown char
        else:
            _error(f"OML Lexer unknown char '{c}' index {idx}")
            ERRORS += 1
            idx += 1
            continue
    return token_list

# ==== AST Type Definition (Extended for style/template/meta/global var) ====
# OML AST Node structure recursive type
OMLAttrValue: _TypeAlias = str | int | None | bool
OMLAttrDict: _TypeAlias = dict[str, OMLAttrValue]

class OmlStyleBlock:
    """Global reusable @style block AST"""
    def __init__(self, name: str, attrs: OMLAttrDict) -> None:
        self.name: str = name
        self.attrs: OMLAttrDict = attrs

class OmlTemplateMacro:
    """Parametric @template macro AST"""
    def __init__(self, name: str, params: list[str], root_node: "OmlNode") -> None:
        self.name: str = name
        self.params: list[str] = params
        self.root_node: OmlNode = root_node

class OmlMetaInfo:
    """@meta global metadata"""
    def __init__(self, data: OMLAttrDict) -> None:
        self.data: OMLAttrDict = data

class OmlNode:
    """Recursive AST Node for OML component tree"""
    def __init__(
        self,
        comp_short: str,       # OML short name e.g Window / Button
        inst_name: str,        # instance id e.g MainWin / submitBtn
        states: list[str],     # multi state chain [hover, pressed]
        attrs: OMLAttrDict,    # key-value attributes
        children: list["OmlNode"],
        use_styles: list[str], # imported @style names
        rect_groups: OMLAttrDict # rect{} grouped attr
    ) -> None:
        self.comp_short: str            = comp_short
        self.inst_name: str             = inst_name
        self.states: list[str]          = states
        self.attrs: OMLAttrDict         = attrs
        self.children: list[OmlNode]    = children
        self.use_styles: list[str]      = use_styles
        self.rect_groups: OMLAttrDict   = rect_groups

# Root full AST bundle (store all global OML unique blocks)
class FullAST:
    def __init__(self) -> None:
        self.meta: OmlMetaInfo | None = None
        self.global_vars: dict[str, OMLAttrValue] = {}
        self.style_blocks: dict[str, OmlStyleBlock] = {}
        self.template_macros: dict[str, OmlTemplateMacro] = {}
        self.top_nodes: list[OmlNode] = []

AST_Type: _TypeAlias = FullAST

# ==== Recursive Parser (Fully support OML exclusive grammar) ====
def ast(tokens: list[Token]) -> AST_Type:
    global ERRORS
    """Recursive descent parser build full OML AST with style/template/meta"""
    token_ptr: int = 0
    token_count: int = len(tokens)
    full_ast: FullAST = FullAST()

    # Helper cursor functions same as your OMS parser
    def curr() -> Token:
        global ERRORS
        nonlocal token_ptr
        if token_ptr >= token_count:
            _error("OML Parser curr() out of token range")
            ERRORS += 1
            return Token(tt.Invalid, "")
        return tokens[token_ptr]
    def next_tok() -> Token:
        global ERRORS
        nonlocal token_ptr
        token_ptr += 1
        if token_ptr >= token_count:
            _error("OML Parser next_tok() EOF")
            ERRORS += 1
            return Token(tt.Invalid, "")
        return tokens[token_ptr]
    def prev_tok() -> Token:
        global ERRORS
        nonlocal token_ptr
        token_ptr -= 1
        return tokens[token_ptr]
    def peek_next() -> Token:
        global ERRORS
        nonlocal token_ptr
        if token_ptr + 1 >= token_count:
            return Token(tt.Invalid, "")
        return tokens[token_ptr + 1]

    def parse_attr_value() -> OMLAttrValue:
        """Parse all value type: num, str, color, dollar var, const, func::slot"""
        global ERRORS
        nonlocal token_ptr
        val_t = curr()
        val: OMLAttrValue = None

        if val_t.type == tt.Number:
            num_str = val_t.val
            token_ptr += 1
            # 拼接后面的单位后缀
            if curr().type == tt.UnitSuffix:
                unit_str = curr().val
                token_ptr += 1
                val = num_str + unit_str
            else:
                val = num_str
        elif val_t.type == tt.String:
            val = val_t.val
            token_ptr += 1
        elif val_t.type == tt.HashColor:
            val = val_t.val
            token_ptr += 1
        elif val_t.type == tt.DollarVar:
            var_name = val_t.val
            token_ptr += 1
            val = full_ast.global_vars.get(var_name, f"${var_name}")
        elif val_t.type == tt.Identifier:
            if val_t.val in CONSTANTS:
                val = CONSTANTS[val_t.val]
                token_ptr += 1
            else:
                # function reference func::slot
                if peek_next().type == tt.DoubleColon:
                    func_id: str = val_t.val
                    token_ptr += 1
                    token_ptr += 1  # skip ::
                    slot_name: str = curr().val
                    token_ptr += 1
                    val = f"{func_id}::{slot_name}"
                else:
                    val = val_t.val
                    token_ptr += 1
        else:
            _error(f"OML Parser invalid value token {val_t.type}")
            ERRORS += 1
            token_ptr += 1
        return val

    def parse_attr_block() -> tuple[OMLAttrDict, OMLAttrDict, list[str]]:
        """Parse inside {}: attr, use style, rect group"""
        global ERRORS
        nonlocal token_ptr
        attrs: OMLAttrDict = {}
        rect_attrs: OMLAttrDict = {}
        use_list: list[str] = []
        while token_ptr < token_count and curr().type != tt.Rbrace:
            ct: Token = curr()
            # use StyleName;
            if ct.type == tt.Identifier and ct.val == "use":
                token_ptr += 1
                style_name: str = curr().val
                use_list.append(style_name)
                token_ptr += 1
                if curr().type == tt.Semi:
                    token_ptr += 1
                continue
            # rect { w=xx; fill=xx; } group attr
            if ct.type == tt.Identifier and ct.val == "rect":
                token_ptr += 1
                if curr().type != tt.Lbrace:
                    _error("rect must follow {")
                    ERRORS += 1
                    token_ptr += 1
                    continue
                token_ptr += 1
                while token_ptr < token_count and curr().type != tt.Rbrace:
                    ra: str = curr().val
                    token_ptr += 1
                    if curr().type != tt.Eq:
                        _error("rect attr missing =")
                        ERRORS += 1
                        token_ptr += 1
                        continue
                    token_ptr += 1
                    rv = parse_attr_value()
                    if curr().type == tt.Semi:
                        token_ptr += 1
                    rect_attrs[ra] = rv
                token_ptr += 1
                continue
            # signal bind attr onClick -> func::slot;
            if ct.type == tt.Identifier and peek_next().type == tt.Arrow:
                attr_key: str = ct.val
                token_ptr += 1
                token_ptr += 1 # skip ->
                val: OMLAttrValue = parse_attr_value()
                if curr().type == tt.Semi:
                    token_ptr += 1
                attrs[attr_key] = val
                continue
            # normal attr = value;
            if ct.type == tt.Identifier and peek_next().type == tt.Eq:
                attr_key = ct.val
                token_ptr += 1
                token_ptr += 1 # skip =
                val = parse_attr_value()
                if curr().type == tt.Semi:
                    token_ptr += 1
                attrs[attr_key] = val
                _info(f"OML Parser set attr [{attr_key}] = {val}")
                continue
            _error(f"Unexpected token {ct.val} inside block")
            ERRORS += 1
            token_ptr += 1
        return attrs, rect_attrs, use_list

    # Recursive parse component block: CompName [Id][:state1:state2] { attrs; children... }
    def parse_component() -> OmlNode:
        global ERRORS
        nonlocal token_ptr
        # Step 1: read component short identifier
        comp_tok: Token = curr()
        comp_short: str = comp_tok.val
        token_ptr += 1

        # Step 2: read instance name (optional identifier after component)
        inst_name = ""
        if curr().type == tt.Identifier and curr().val not in COMPONENT_MAP and curr().val not in OML_KEYWORDS:
            inst_name: str = curr().val
            token_ptr += 1

        # Step3: parse multi state chain :hover:pressed
        states: list[Any] = []
        while curr().type == tt.Colon:
            token_ptr += 1
            state_tok: Token = curr()
            if state_tok.type != tt.Identifier:
                _error(f"OML Parser expect state identifier after colon")
                ERRORS += 1
                break
            states.append(state_tok.val)
            token_ptr += 1

        # Step4: expect opening { Lbrace
        if curr().type != tt.Lbrace:
            _error(f"OML Parser expect '{{' after component declaration")
            ERRORS += 1
            raise SyntaxError("Missing opening brace {")
        token_ptr += 1

        attrs, rect_groups, use_styles = parse_attr_block()
        children: list[OmlNode] = []

        # Re-scan block for child components
        while token_ptr < token_count and curr().type != tt.Rbrace:
            current_t: Token = curr()
            # Branch1: template macro call TemplateName(arg1,arg2)
            if current_t.type == tt.Identifier and current_t.val in full_ast.template_macros and peek_next().type == tt.Lpar:
                tpl: OmlTemplateMacro = full_ast.template_macros[current_t.val]
                token_ptr += 1  # skip template name
                token_ptr += 1  # skip '('
                arg_vals: list[Any] = []
                while curr().type != tt.Rpar:
                    arg: OMLAttrValue = parse_attr_value()
                    arg_vals.append(arg)
                    if curr().type == tt.Comma:
                        token_ptr += 1
                token_ptr += 1  # skip ')'
                # Skip ';'
                if curr().type == tt.Semi:
                    token_ptr += 1
                # Shallow copy root node & inject args (Simplely expand)
                root_copy: OmlNode = tpl.root_node
                children.append(root_copy)
                continue
            # Branch2: normal widget
            if current_t.type == tt.Identifier and current_t.val in COMPONENT_MAP:
                child_node = parse_component()
                children.append(child_node)
                continue
            # Skip other char
            token_ptr += 1
        if curr().type == tt.Semi:
            token_ptr += 1
        # consume closing }
        if curr().type == tt.Rbrace:
            token_ptr += 1
        node: OmlNode = OmlNode(comp_short, inst_name, states, attrs, children, use_styles, rect_groups)
        _info(f"OML Parser finish component node {comp_short} id={inst_name} states={states}")
        return node

    # Parse top level global $Var = val;
    def parse_global_var() -> None:
        global ERRORS
        nonlocal token_ptr
        var_name = curr().val
        token_ptr += 1
        if curr().type != tt.Eq:
            _error("Global var missing =")
            ERRORS += 1
            return
        token_ptr += 1
        val: OMLAttrValue = parse_attr_value()
        if curr().type == tt.Semi:
            token_ptr += 1
        full_ast.global_vars[var_name] = val
        _info(f"Global var ${var_name} = {val}")

    # Parse @style Name { ... }
    def parse_style_block():
        global ERRORS
        nonlocal token_ptr
        token_ptr += 1 # skip @
        token_ptr += 1 # skip style
        style_name = curr().val
        token_ptr += 1
        if curr().type != tt.Lbrace:
            _error("@style must follow {")
            ERRORS += 1
            return
        token_ptr += 1
        attrs, _, _ = parse_attr_block()
        token_ptr += 1
        full_ast.style_blocks[style_name] = OmlStyleBlock(style_name, attrs)
        _info(f"Registered global style [{style_name}]")

    # Parse @template Name(p1,p2) { ... }
    def parse_template_macro() -> None:
        global ERRORS
        nonlocal token_ptr
        token_ptr += 1 # skip @
        token_ptr += 1 # skip template
        tpl_name: str = curr().val
        token_ptr += 1
        params: list[Any] = []
        if curr().type == tt.Lpar:
            token_ptr += 1
            while curr().type != tt.Rpar:
                p: str = curr().val
                params.append(p)
                token_ptr += 1
                if curr().type == tt.Comma:
                    token_ptr += 1
            token_ptr += 1
        if curr().type != tt.Lbrace:
            _error("@template must follow {")
            ERRORS += 1
            return
        token_ptr += 1
        root_node = parse_component()
        full_ast.template_macros[tpl_name] = OmlTemplateMacro(tpl_name, params, root_node)
        _info(f"Registered template macro [{tpl_name}] params={params}")

    # Parse @meta { ... }
    def parse_meta_block() -> None:
        global ERRORS
        nonlocal token_ptr
        token_ptr += 1 # skip @
        token_ptr += 1 # skip meta
        if curr().type != tt.Lbrace:
            _error("@meta must follow {")
            ERRORS += 1
            return
        token_ptr += 1
        meta_attrs, _, _ = parse_attr_block()
        token_ptr += 1
        full_ast.meta = OmlMetaInfo(meta_attrs)
        _info("Loaded global @meta info block")

    # Main top level loop
    while token_ptr < token_count:
        ct: Token = curr()
        # Global variable $NAME
        if ct.type == tt.DollarVar:
            parse_global_var()
            continue
        # @ meta / style / template
        if ct.type == tt.At:
            nt = peek_next()
            if nt.val == "meta":
                parse_meta_block()
            elif nt.val == "style":
                parse_style_block()
            elif nt.val == "template":
                parse_template_macro()
            else:
                token_ptr += 1
            continue
        # Component or template macro call
        if ct.type == tt.Identifier:
            # Template macro invoke
            if ct.val in full_ast.template_macros and peek_next().type == tt.Lpar:
                tpl: OmlTemplateMacro = full_ast.template_macros[ct.val]
                token_ptr += 1
                token_ptr += 1
                arg_vals: list[Any] = []
                while curr().type != tt.Rpar:
                    arg: OMLAttrValue = parse_attr_value()
                    arg_vals.append(arg)
                    if curr().type == tt.Comma:
                        token_ptr += 1
                token_ptr += 1
                # Inject args into template root node, shallow copy logic simplified
                root_copy: OmlNode = tpl.root_node
                full_ast.top_nodes.append(root_copy)
                continue
            # Normal component
            if ct.val in COMPONENT_MAP:
                node: OmlNode = parse_component()
                full_ast.top_nodes.append(node)
                continue
        token_ptr += 1
    return full_ast

# ==== AST -> QML Converter (Support all OML exclusive features) ====
def convert(ast: AST_Type) -> QmlString:
    """Recursively traverse full OML AST and output standard QML source text"""
    global ERRORS
    qml_header: list[str] = [
        "// @generated by OML Converter (Oh My Modeling Language)",
        "// OML Exclusive Syntax: unit, color, @style, @template, $var, multi-state",
        "// License: MIT",
        "import QtQuick 2.15",
        "import QtQuick.Controls 2.15",
        ""
    ]
    # Inject meta info comment header
    if ast.meta is not None:
        qml_header.append("/* Global Meta Info */")
        for k, v in ast.meta.data.items():
            qml_header.append(f"// {k}: {v}")
        qml_header.append("")
    # Inject global var const in QML root
    global_var_lines: list[Any] = []
    if ast.global_vars:
        global_var_lines.append("property var OML_GLOBAL: {")
        g_vars: list[Any] = []
        for name, val in ast.global_vars.items():
            if isinstance(val, str):
                g_vars.append(f'    "{name}": "{val}"')
            else:
                g_vars.append(f'    "{name}": {val}')
        global_var_lines.append(",\n".join(g_vars))
        global_var_lines.append("}")
        global_var_lines.append("")

    def merge_style_attrs(node: OmlNode) -> OMLAttrDict:
        """Merge component local attr + all imported @style attrs"""
        global ERRORS
        merged: dict[Any, Any] = {}
        # Apply style blocks first
        for style_name in node.use_styles:
            if style_name in ast.style_blocks:
                merged.update(ast.style_blocks[style_name].attrs)
        # Local attr override style
        merged.update(node.attrs)
        # Merge rect group shorthand to real QML rect attributes
        rect_map = {
            "w": "width",
            "h": "height",
            "x": "x",
            "y": "y",
            "fill": "color"
        }
        for rk, rv in node.rect_groups.items():
            if rk in rect_map:
                merged[rect_map[rk]] = rv
        return merged

    def render_value(val) -> str:
        global ERRORS
        if val is None:
            return "null"
        elif isinstance(val, bool):
            return "true" if val else "false"
        elif isinstance(val, int):
            return str(val)
        elif isinstance(val, str):
            if val.startswith("#"):
                return val
            if val.startswith("$"):
                return f'OML_GLOBAL["{val[1:]}"]'
            return f'"{val}"'
        return str(val)

    def render_node(node: OmlNode, indent: int = 0) -> list[str]:
        global ERRORS
        lines: list[str] = []
        indent_str: LiteralString = "    " * indent
        # resolve real QML component type
        qml_type: str = COMPONENT_MAP.get(node.comp_short, node.comp_short)
        # multi state join
        state_suffix = ""
        if node.states:
            state_suffix: str = ":" + ":".join(node.states)
        # instance id
        id_decl: str = f"id: {node.inst_name};" if node.inst_name else ""

        # open component line
        lines.append(f"{indent_str}{qml_type}{state_suffix} {{")
        child_indent: int = indent + 1
        child_indent_str: LiteralString = "    " * child_indent

        # write id first if exists
        if id_decl:
            lines.append(f"{child_indent_str}{id_decl}")
        # write global var inject if root node
        if indent == 0 and global_var_lines:
            for gl in global_var_lines:
                lines.append(f"{child_indent_str}{gl}")

        # render merged attributes
        all_attrs: OMLAttrDict = merge_style_attrs(node)
        for attr_name, attr_val in all_attrs.items():
            val_text = render_value(attr_val)
            lines.append(f"{child_indent_str}{attr_name}: {val_text};")

        # render child nodes recursively
        for child in node.children:
            child_lines = render_node(child, child_indent)
            lines.extend(child_lines)

        # close brace
        lines.append(f"{indent_str}}}")
        return lines

    # render all top level nodes
    all_lines: list[str] = qml_header
    for top_node in ast.top_nodes:
        node_text: list[str] = render_node(top_node, indent=0)
        all_lines.extend(node_text)
        all_lines.append("")
    return "\n".join(all_lines)

# Top level entry function same naming style as convert_oms_to_qss
def convert_oml_to_qml(oml_source: str) -> QmlString:
    """Main entry: raw OML string -> compiled QML source string"""
    global ERRORS
    token_stream: list[Token] = lexer(oml_source)
    full_ast_tree: AST_Type = ast(token_stream)
    qml_output: QmlString = convert(full_ast_tree)
    return qml_output