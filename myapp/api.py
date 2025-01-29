import reflex as rx
import requests as r


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

    response = response = r.post(
        url=url,
        data='{"query":"query { me { name email } }"}',
        headers={
            "Authorization": 'Bearer 81335197-ccd2-484a-bf80-2edb17cdbcee',
            'Content-Type': 'application/json',
        })

    return response
