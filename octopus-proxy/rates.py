import json
import os

import falcon

import utils
import queries
import sys

sys.path.append("octopus-proxy/")


class RatesResource:
    def on_get(self, req, resp):
        auth_jwt = utils.authenticate()
        account_details = utils.query(
            queries.account_details_query,
            auth_jwt,
            {"accountNumber": os.getenv("OCTOPUS_ACCOUNT_NUMBER")},
        ).json()
        account_details = account_details["data"]
        resp.status = falcon.HTTP_OK
        resp.text = json.dumps(
            {
                "electricity": {
                    "unit_rate": account_details["account"]["electricityAgreements"][0][
                        "tariff"
                    ]["unitRate"],
                    "standing_charge": account_details["account"][
                        "electricityAgreements"
                    ][0]["tariff"]["standingCharge"],
                },
                "gas": {
                    "unit_rate": account_details["account"]["gasAgreements"][0][
                        "tariff"
                    ]["unitRate"],
                    "standing_charge": account_details["account"]["gasAgreements"][0][
                        "tariff"
                    ]["standingCharge"],
                },
            }
        )
        return
