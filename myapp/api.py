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


response = r.post(url=url,
                  json={
                      "query": body,
                      "authorization": 'Bearer: 81335197-ccd2-484a-bf80-2edb17cdbcee'
                  })
print("response status code: ", response.status_code)
if response.status_code == 200:
    print("response : ", response.content)


def test():
    return requests
