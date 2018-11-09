from flask import abort
import jinja2


def get_or_404(model, ident):
    rv = model.query.get(ident)
    if rv is None:
        abort(404)
    return rv

# Taken from https://stackoverflow.com/a/18900930/119071
_js_escapes = {
        '\\': '\\u005C',
        '\'': '\\u0027',
        '"': '\\u0022',
        '>': '\\u003E',
        '<': '\\u003C',
        '&': '\\u0026',
        '=': '\\u003D',
        '-': '\\u002D',
        ';': '\\u003B',
        u'\u2028': '\\u2028',
        u'\u2029': '\\u2029'
}

_js_escapes.update(('%c' % z, '\\u%04X' % z) for z in range(32))
def escapejs(value):
        retval = []
        for letter in value:
                if _js_escapes.get(letter):
                        retval.append(_js_escapes[letter])
                else:
                        retval.append(letter)

        return jinja2.Markup("".join(retval))
