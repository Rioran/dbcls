from kaa.theme import Style
from kaa import doc_re
from kaa.syntax_highlight import Span, SingleToken, Tokenizer, Keywords, Token


sql_editor_themes = {
    'basic': [
        Style('string', 'Green', None, bold=True),
        Style('number', 'Yellow', None, bold=True),
    ]
}

class CaseInsensitiveKeywords(Keywords):
    def re_start(self) -> str:
        tokens = []
        for token in self._tokens:
            new_token = ''
            token = doc_re.escape(token)
            for char in token:
                if char.lower() != char.upper():
                    new_token += '[' + char.lower() + char.upper() + ']'
                    continue
                new_token = new_token + char
            if new_token:
                tokens.append(new_token)

        return rf'\b({"|".join(tokens)})\b'


class NonSqlComment(Span):
    pass


KEYWORDS = [
    'SELECT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'COLUMN', 'USE',
    'FROM', 'JOIN', 'OUTER', 'INNER', 'LIMIT', 'ORDER BY', 'AS',
    'SHOW', 'FROM', 'WHERE', 'DESC', 'TABLES', 'CREATE', 'TABLE',
    'SET', 'IS', 'NOT', 'NULL', 'ON', 'IN', 'LIKE', 'ILIKE', 'AND',
    'OR', 'INSERT', 'INTO', 'VALUES', 'INTERVAL', 'GROUP', 'BY',
    'HAVING', 'GRANT', 'LEFT', 'RIGHT', 'FULL', 'CROSS'
]


def sqleditor_tokens() -> list[tuple[str, Token]]:
    return [
        ('comment1', Span('comment', r'--', '$')),
        ('comment2', NonSqlComment('comment', r'\#', '$')),
        ("string1", Span('string', '"', '"', escape='\\')),
        ("string2", Span('string', "'", "'", escape='\\')),
        ("number", SingleToken('number', [r'\b[0-9]+(\.[0-9]*)*\b', r'\b\.[0-9]+\b'])),
        ("keyword", CaseInsensitiveKeywords('keyword', KEYWORDS)),
    ]


def make_tokenizer() -> Tokenizer:
    return Tokenizer(tokens=sqleditor_tokens())
