from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

import asyncio
import creds
import constants
import queries
import json
import falcon


def json_pprint(input_dict):
    print(highlight(json.dumps(input_dict, indent=2), JsonLexer(), TerminalFormatter()))


def authenticate(transport, session):
    auth_params = {"apiKey": creds.api_key}

    # Execute the query on the transport
    auth_result = session.execute(
        queries.auth_mutation, variable_values=auth_params
    )
    auth_jwt = auth_result["obtainKrakenToken"]["token"]

    return auth_jwt


def query(session, gql_query, gql_params={}):
    result = session.execute(gql_query, variable_values=gql_params)
    return result


def create_session():
    transport = RequestsHTTPTransport(url=constants.OCTOPUS_BASE_URL)

    session = Client(
        transport=transport, fetch_schema_from_transport=False
    )
    auth_jwt = authenticate(transport, session)
    transport.headers.add({"Authorization": auth_jwt})
    viewer = query(session, queries.viewer_query)

    return transport, viewer


class GetRates:
    def __init__(self):
        self._transport, self._viewer = create_session()

    def on_get(self, req, resp):
        account_details = query(
            self._transport,
            queries.account_details_query,
            gql_params={
                "accountNumber": self._viewer["viewer"]["accounts"][0]["number"]
            },
        )
        # json_pprint(account_details)
        resp.status = falcon.HTTP_OK
        resp.text = json.dumps({
            "electricity": {
                "unit_rate": account_details["account"]["electricityAgreements"][0][
                    "tariff"
                ]["unitRate"],
                "standing_charge": account_details["account"]["electricityAgreements"][0]["tariff"]["standingCharge"],
            },
            "gas": {
                "unit_rate": account_details["account"]["gasAgreements"][0]["tariff"][
                    "unitRate"
                ],
                "standing_charge": account_details["account"]["gasAgreements"][0][
                    "tariff"
                ]["standingCharge"],
            },
        })
