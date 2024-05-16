from blacksheep.server import Application


def configure_cors(app: Application):
    app.use_cors(
        allow_methods="*", #"GET POST DELETE WS",
        allow_origins="*",
        allow_headers="* Authorization",
        max_age=300,
    )
