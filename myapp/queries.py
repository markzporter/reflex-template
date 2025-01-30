from .models import DashApp
from rxconfig import config
import requests as r
import json
url = 'https://backboard.railway.com/graphql/v2'


# GQL Query Strings


DEPLOYMENTS_QUERY = """
query MyQuery($projectId: String!) {
  project(id: $projectId) {
    deployments {
      edges {
        node {
          id
          url
          createdAt
          serviceId
          staticUrl
          environment {
            name
            id
          }
          service {
            name
          }
          status
        }
      }
    }
  }
}
"""


CREATE_DASHAPP_SERVICE: str = """
mutation serviceCreate($projectId: String!, $repository: String) {
  serviceCreate(
    input: {
      projectId: $projectId
      source: { repo: $repository}
    }
  ) {
    id
  }
}
"""

UPDATE_DASHAPP_SERVICE: str = """
mutation MyMutation($serviceId: String!, $environmentId: String!) {
serviceInstanceUpdate(
    input: {startCommand: "gunicorn app:server"}
    serviceId: $serviceId
)
serviceDomainCreate(
    input: {environmentId: $environmentId, serviceId: $serviceId}
) {
    id
}
}
"""

DEPLOY_DASHAPP_SERVICE: str = """
mutation MyMutation($serviceId: String!, $environmentId: String!) {
  serviceInstanceDeploy(serviceId: $serviceId, environmentId: $environmentId)
}
"""


DELETE_DASHAPP_SERVICE: str = """
mutation MyMutation($serviceId: String!) {
  serviceDelete(id: $serviceId)
}
"""


def query_server(graphql_query_str: str, variables: dict):

    json_data = {
        "query": graphql_query_str,
        "variables": variables,
    }
    response = r.post(
        url=url,
        json=json_data,
        headers={
            "Authorization": f"Bearer {config.railway_api_token}",
            "Content-Type": "application/json",
        },
    )
    print(response, response.content)
    response.raise_for_status()
    return response.content


def unpack_dashapps(data) -> list[DashApp]:
    dashapps = []
    for item in data:
        name = item.get('service', {}).get('name', '')
        url = item.get('staticUrl', '')  # you could also check item.get('url', '')
        app_id = item.get('id', '')
        created_at = item.get('createdAt', '')
        deployment_status = item.get('status', '')

        # Create an instance of DashApp and append it to the list
        dashapp = DashApp(app_name=name,
                          url=url, id=app_id,
                          created_at=created_at,
                          deployment_status=deployment_status)
        dashapps.append(dashapp)

    return dashapps


def get_active_dash_deployments() -> list[DashApp]:
    variables = {
        "projectId": config.project_id,
    }
    ret = query_server(DEPLOYMENTS_QUERY, variables)
    deployments_dict: dict = json.loads(ret.decode())
    # print(deployments_dict)
    deployments = deployments_dict['data']['project']['deployments']['edges']

    success_deployments = [
        deployment['node'] for deployment in deployments if
        (deployment['node']['service']['name'] != 'Reflex')
    ]

    dashapps: list[DashApp] = unpack_dashapps(success_deployments)

    return dashapps


def create_dash_service(repository) -> str:
    create_variables = {
        "projectId": config.project_id,
        "repository": repository
    }
    ret = query_server(CREATE_DASHAPP_SERVICE, create_variables)
    print(ret)
    service_dict = json.loads(ret.decode())
    service_id = service_dict['data']['serviceCreate']['id']
    return service_id


def configure_dash_service(service_id: str):
    variables = {
        "serviceId": service_id,
        "environmentId": config.environment_id,
    }
    query_server(UPDATE_DASHAPP_SERVICE, variables=variables)


def deploy_dash_service(service_id: str):
    variables = {
        "serviceId": service_id,
        "environmentId": config.environment_id,
    }
    query_server(DEPLOY_DASHAPP_SERVICE, variables=variables)


def create_dash_app(repository: str) -> str:
    service_id = create_dash_service(repository=repository)
    configure_dash_service(service_id=service_id)
    deploy_dash_service(service_id=service_id)
    return service_id


def delete_dash_app(service_id: str):
    variables = {
        "serviceId": service_id
    }
    ret = query_server(DELETE_DASHAPP_SERVICE, variables=variables)
    
    


