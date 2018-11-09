import click
from flask import Flask
from core import app, db
from core.models import Client, ProductArea


@app.cli.command()
def init_data():
    db.session.add(Client("Client n1"))
    db.session.add(Client("Client n2"))
    db.session.add(ProductArea("ProductArea n1"))
    db.session.add(ProductArea("ProductArea n2"))
    db.session.commit()


if __name__ == '__main__':
    init_data()
