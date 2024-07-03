from .app.app import DashApp


def run():
    dash_app = DashApp()
    dash_app.run_server()
