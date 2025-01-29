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
    
    response = r.post(url=url,
                  json={
                      "query": body,
                      "authorization": 'Bearer: 81335197-ccd2-484a-bf80-2edb17cdbcee'
                  })
        
    return response
