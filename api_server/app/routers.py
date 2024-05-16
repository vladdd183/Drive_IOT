from os import path, listdir
from blacksheep import Application
from importlib import import_module

root_dir = path.dirname(__file__)


def configure_routers(app: Application, docs):
    [
        [
            import_module(
                f'app.{module}.{file[:-3]}',
                __name__
            ).configure_routes(app, docs)
            for file in listdir(f'{root_dir}/{module}') 
            if file.endswith('Router.py')
        ] 
        for module in listdir(root_dir) if module.endswith('Module')
    ]
