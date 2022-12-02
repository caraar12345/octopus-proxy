import os
import queries
import requests
import constants
import json


def authenticate():
    auth_params = {"apiKey": os.getenv("OCTOPUS_API_KEY")}

    # Execute the query on the transport
    auth_result = query(
        gql_query=queries.auth_mutation, auth_jwt=None, gql_params=auth_params
    )
    auth_jwt = auth_result.json()["data"]["obtainKrakenToken"]["token"]

    return auth_jwt


def query(gql_query, auth_jwt, gql_params={}):
    session = requests.Session()
    request = requests.Request(
        "POST",
        url=constants.OCTOPUS_BASE_URL,
        headers={"Content-Type": "application/json"},
    )

    prepped_req = session.prepare_request(request)

    if auth_jwt is not None:
        prepped_req.headers["Authorization"] = f"JWT {auth_jwt}"

    if gql_params == {}:
        prepped_req.body = json.dumps({"query": gql_query.strip()})
    else:
        prepped_req.body = json.dumps(
            {"query": gql_query.strip(), "variables": gql_params}
        )

    prepped_req.headers["Content-Length"] = len(prepped_req.body)

    return session.send(prepped_req)
