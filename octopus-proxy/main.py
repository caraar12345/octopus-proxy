from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

import asyncio
import creds
import constants
import queries
import json


def json_pprint(input_dict):
    print(highlight(json.dumps(input_dict, indent=2), JsonLexer(), TerminalFormatter()))


async def authenticate(transport, session):
    auth_params = {
        "apiKey": creds.api_key
    }

    # Execute the query on the transport
    auth_result = await session.execute(queries.auth_mutation, variable_values=auth_params)
    auth_jwt = auth_result["obtainKrakenToken"]["token"]

    transport.session.headers.add("Authorization", f"JWT {auth_jwt}")
    # print(auth_jwt)
    return transport


async def query(session, gql_query, gql_params={}):
    result = await session.execute(gql_query, variable_values=gql_params)
    return result


async def main():
    transport = AIOHTTPTransport(url=constants.OCTOPUS_BASE_URL)

    async with Client(
        transport=transport,
        fetch_schema_from_transport=False
    ) as session:
        await authenticate(transport, session)
        viewer_result = await query(session, queries.viewer_query)
        # json_pprint(viewer_result)

        account_details = await query(session, queries.account_details_query, gql_params={"accountNumber": viewer_result["viewer"]["accounts"][0]["number"]})
        # json_pprint(account_details)
        print(account_details["account"]["electricityAgreements"][0]["tariff"]["unitRate"])
        print(account_details["account"]["electricityAgreements"][0]["tariff"]["standingCharge"])
        print(account_details["account"]["gasAgreements"][0]["tariff"]["unitRate"])
        print(account_details["account"]["gasAgreements"][0]["tariff"]["standingCharge"])
asyncio.run(main())
