import app.libs.debug as debughelpers


def setup_routes(app):

    app.get('/echo/{something}')(debughelpers.echo)
    app.post('/echo/')(debughelpers.echo)
