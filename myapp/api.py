import reflex as rx
import requests as r
from rxconfig import config


def root():
    return {"message": "hello from reflex"}


url = 'https://backboard.railway.com/graphql/v2'

PROJECT_QUERY = """

    query {
    projects {
        edges {
        node {
            id
        }
        }
    }
    }
"""


def test():
    print('waht is happening')
    return "HEYYY"
