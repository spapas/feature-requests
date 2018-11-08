from flask import abort


def get_or_404(model, ident):
    rv = model.query.get(ident)
    if rv is None:
        abort(404)
    return rv