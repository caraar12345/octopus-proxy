auth_mutation = """
    mutation krakenTokenAuthentication($apiKey: String!) {
      obtainKrakenToken(input: {APIKey: $apiKey}) {
        token
      }
    }
"""

viewer_query = """
    query viewer {
      viewer {
        fullName
        accounts {
          number
        }
      }
    }
    """

account_details_query = """
    query accountDetails($accountNumber: String!) {
      account(accountNumber: $accountNumber) {
        number
        status
        id
        balance
        accountType
        electricityAgreements {
          tariff {
            ... on StandardTariff {
              productCode
              unitRate
              standingCharge
              preVatUnitRate
              preVatStandingCharge
            }
          }
        }
        gasAgreements {
          tariff {
            tariffCode
            unitRate
            standingCharge
            preVatUnitRate
            preVatStandingCharge
          }
        }
      }
    }
    """
