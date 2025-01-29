import reflex as rx
import requests as r
from rxconfig import config


def root():
    return {"message": "hello from reflex"}


url = 'https://backboard.railway.com/graphql/v2'

body = """

    query MyQuery {
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
    response = response = r.post(
        url=url,
        data='{"query":"query { me { name email } }"}',
        headers={
            "Authorization": f'Bearer {config.railway_api_token}',
            'Content-Type': 'application/json',
        })

    print('hey trigger build')
    print(response)
    print(response.content)
    return response.content
