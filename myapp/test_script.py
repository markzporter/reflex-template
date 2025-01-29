import requests as r

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


response = r.post(
    url=url,
    data='{"query":"query { me { name email } }"}',
    headers={
        "Authorization": 'Bearer 81335197-ccd2-484a-bf80-2edb17cdbcee',
        'Content-Type': 'application/json',
    }
)

print(response)
print(response.content)
