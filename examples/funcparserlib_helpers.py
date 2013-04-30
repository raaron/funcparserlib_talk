from funcparserlib.parser import some, a, skip, finished, many, maybe
import token
from StringIO import StringIO
from tokenize import generate_tokens, NL


class Token(object):
    def __init__(self, code, value, start=(0, 0), stop=(0, 0), line=''):
        self.code = code
        self.value = value
        self.start = start
        self.stop = stop
        self.line = line

    @property
    def type(self):
        return token.tok_name[self.code]

    def __unicode__(self):
        pos = '-'.join('%d,%d' % x for x in [self.start, self.stop])
        return "%s %s '%s'" % (pos, self.type, self.value)

    def __repr__(self):
        return 'Token(%r, %r, %r, %r, %r)' % (
            self.code, self.value, self.start, self.stop, self.line)

    def __eq__(self, other):
        return (self.code, self.value) == (other.code, other.value)

# Well known functions
const = lambda x: lambda _: x
unarg = lambda f: lambda x: f(*x)

# Semantic actions and auxiliary functions
tokval = lambda tok: tok.value


def make_number(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def make_string(s):
    return str(s)


@unarg
def eval_expr(z, list):
    return reduce(lambda s, (f, x): f(s, x), list, z)


@unarg
def make_list(first, rest):
    if len(rest) == 0:
        return [first]
    else:
        items = list(rest)
        items.insert(0, first)
        return items


def make_maybe_empty_list(arg):
    if arg is None:
        return []
    else:
        return make_list(arg)


def tokenize(s):
    'str -> [Token]'
    # print list(unicode(Token(*t))
    #     for t in generate_tokens(StringIO(s).readline)
    #     if t[0] not in [NL, token.NEWLINE])
    return list(Token(*t)
        for t in generate_tokens(StringIO(s).readline)
        if t[0] not in [NL, token.NEWLINE])

# Primitives
number = (
    some(lambda tok: tok.code == token.NUMBER)
    >> tokval
    >> make_number)

string = (
    some(lambda tok: tok.code == token.STRING)
     >> tokval
     >> (lambda s: s[1:-1]))

op = lambda s: a(Token(token.OP, s)) >> tokval
op_ = lambda s: skip(op(s))
rawname = (some(lambda tok: tok.code == token.NAME) >> tokval)

kw = lambda s: skip(a(Token(token.NAME, s)))

newline = skip(a(Token(token.NEWLINE, '\n')))
indent = skip(a(Token(token.INDENT, '    ')))
dedent = skip(a(Token(token.DEDENT, '')))

comma = op_(',')
semicolon = op_(';')
dot = op_('.')
colon = op_(':')
dbl_quote = op_('"')
assign = colon + op_('=')

openparen = op_('(')
closeparen = op_(')')
inparens = lambda s: openparen + s + closeparen

opencurlyparen = op_('{')
closecurlyparen = op_('}')
incurlyparens = lambda s: opencurlyparen + s + closecurlyparen

openbracket = op_('[')
closebracket = op_(']')
inbrackets = lambda s: openbracket + s + closebracket

listof = lambda s: (s + many(comma + s)) >> make_list
maybe_empty_listof = lambda s: maybe(s + many(comma + s)) >> make_maybe_empty_list

endmark = a(Token(token.ENDMARKER, ''))
end = skip(endmark + finished)
