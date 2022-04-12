from pyact import render
from .app import app


def main():
    render("root", app())
