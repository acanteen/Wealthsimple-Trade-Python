from .requestor import APIRequestor
import cloudscraper
import os
import json
from datetime import date

class WSTrade:
    """
    Wealthsimple Trade API wrapper

    Attributes
    ----------
    session : session
        A requests Session object to be associated with the class
    APIMainURL : str
        Main URL endpoint for API
    TradeAPI : APIRequester
        APIRequester object to handle API calls

    Methods
    -------
    login(email=None, password=None, two_factor_callback=None)
        Login to Wealthsimple Trade account
    get_accounts()
        Get Wealthsimple Trade accounts
    get_account_ids()
        Get Wealthsimple Trade account ids
    get_account(id)
        Get a Wealthsimple Trade account given an id
    get_account_history(id, time="all")
        Get Wealthsimple Trade account history
    get_activities()
        Get Wealthsimple Trade activities
    get_orders(symbol=None)
        Get Wealthsimple Trade orders
    get_security(symbol)
        Get information about a security
    get_positions(id)
        Get positions
    get_person()
        Get Wealthsimple Trade person object
    get_me()
        Get Wealthsimple Trade user object
    get_bank_accounts():
        Get list of bank accounts tied to Wealthsimple Trade account
    get_deposits()
        Get list of deposits
    get_forex()
        Get foreign exchange rate
    """

    def __init__(self, email: str, password: str, two_factor_callback: callable = None ):
        """
        Parameters
        ----------
        email : str
            Wealthsimple Trade login email
        password : str
            Wealthsimple Trade login password
        two_factor_callback: function
            Callback function that returns user input for 2FA code
        """
        self.session = cloudscraper.create_scraper()
        self.APIMAIN = "https://trade-service.wealthsimple.com/"
        self.TradeAPI = APIRequestor(self.session, self.APIMAIN)
        self.login(email, password, two_factor_callback=two_factor_callback)

    def login(
        self,
        email: str = None,
        password: str = None,
        two_factor_callback: callable = None,
    ) -> None:
        """Login to Wealthsimple Trade account

        Parameters
        ----------
        email : str
            Wealthsimple Trade account email
        password : str
            Wealthsimple Trade account password
        two_factor_callback: function
            Callback function that returns user input for 2FA code

        Returns
        -------
        None
        """
        if email and password:

            # Login credentials to pass in request
            data = [
                ("email", email),
                ("password", password),
            ]

            response = self.TradeAPI.makeRequest("POST", "auth/login", params=data)

            # Check if account requires 2FA
            if "x-wealthsimple-otp" in response.headers:
                if two_factor_callback == None:
                    raise Exception(
                        "This account requires 2FA. A 2FA callback function must be provided"
                    )
                else:
                    # Obtain 2FA code using callback function
                    MFACode = two_factor_callback()
                    # Add the 2FA code to the body of the login request
                    data.append(("otp", MFACode))
                    # Make a second login request using the 2FA code
                    response = self.TradeAPI.makeRequest(
                        "POST", "auth/login", params=data)

            if response.status_code == 401:
                raise Exception("Invalid Login")

            # Update session headers with the API access token
            self.session.headers.update(
                {"Authorization": response.headers["X-Access-Token"]}
            )
        else:
            raise Exception("Missing login credentials")

    def get_accounts(self) -> list:
        """Get Wealthsimple Trade accounts

        Returns
        -------
        list
            A list of Wealthsimple Trade account dictionary objects
        """
        response = self.TradeAPI.makeRequest("GET", "account/list")
        response = response.json()
        response = response["results"]
        return response

    def get_account_ids(self) -> list:
        """Get Wealthsimple Trade account ids

        Returns
        -------
        list
            A list of Wealthsimple Trade account ids
        """
        userAccounts = self.get_accounts()
        accountIDList = []
        for account in userAccounts:
            accountIDList.append(account["id"])
        return accountIDList

    def get_account(self, id: str) -> dict:
        """Get a Wealthsimple Trade account given an id

        Parameters
        ----------
        id : str
            Wealthsimple Trade account id

        Returns
        -------
        dict
            A dictionary containing the Wealthsimple Trade account
        """
        userAccounts = self.get_accounts()
        for account in userAccounts:
            if account["id"] == id:
                return account
        raise NameError(f"{id} does not correspond to any account")

    def get_account_history(self, id: str, time: str = "all") -> dict:
        """Get Wealthsimple Trade account history

        Parameters
        ----------
        id : str
            Wealthsimple Trade account id
        time : str
            String containing time interval for history

        Returns
        -------
        dict
            A dictionary containing the historical Trade account data
        """
        response = self.TradeAPI.makeRequest(
            "GET", f"account/history/{time}?account_id={id}"
        )
        response = response.json()
        if "error" in response:
            if response["error"] == "Record not found":
                raise NameError(f"{id} does not correspond to any account")

        return response

    def get_activities(self) -> list:
        """Get Wealthsimple Trade activities

        Returns
        -------
        list
            A list of dictionaries containing Wealthsimple Trade activities
        """
        response = self.TradeAPI.makeRequest("GET", "account/activities")
        response = response.json()
        return response["results"]

    def get_orders(self, symbol: str = None) -> list:
        """Get Wealthsimple Trade orders

        Parameters
        ----------
        symbol : str
            Symbol for security to filter orders on

        Returns
        -------
        list
            A list containing Wealthsimple Trade order dictionaries
        """
        response = self.TradeAPI.makeRequest("GET", "orders")
        response = response.json()
        # Check if order must be filtered:
        if symbol:
            filteredOrders = []
            for order in response["results"]:
                if order["symbol"] == symbol:
                    filteredOrders.append(order)
            return filteredOrders
        else:
            return response

    def get_security(self, id: str) -> dict:
        """Get information about a security

        Parameters
        ----------
        id : str
            Wealthsimple Security ID to search on

        Returns
        -------
        dict
            Dictionary containing information for security
        """

        response = self.TradeAPI.makeRequest("GET", f"securities/{id}")
        response = response.json()
        return response

    def get_securities_from_ticker(self, symbol: str) -> list:
        """Get information about a securitys with matching ticker symbols

        Parameters
        ----------
        symbol : str
            Symbol for security to search on

        Returns
        -------
        list
            A list containing matching securities
        """
        response = self.TradeAPI.makeRequest(
            "GET", f"securities?query={symbol}")
        response = response.json()
        return response["results"]

    def get_positions(self, id: str) -> list:
        """Get positions

        Parameters
        ----------
        id : str
            Wealthsimple Trade account id

        Returns
        -------
        list
            A list containing positions
        """
        response = self.TradeAPI.makeRequest(
            "GET", f"account/positions?account_id={id}"
        )
        response = response.json()
        return response["results"]

    def get_person(self) -> dict:
        """Get Wealthsimple Trade person object

        Returns
        -------
        dict
            A dictionary containing a person object
        """
        response = self.TradeAPI.makeRequest("GET", "person")
        return response.json()

    def get_me(self) -> dict:
        """Get Wealthsimple Trade user object

        Returns
        -------
        dict
            A dictionary containing a user object
        """
        response = self.TradeAPI.makeRequest("GET", "me")
        return response.json()

    def get_bank_accounts(self) -> list:
        """Get list of bank accounts tied to Wealthsimple Trade account

        Returns
        -------
        list
            A list of dictionaries containing bank account objects
        """
        response = self.TradeAPI.makeRequest("GET", "bank-accounts")
        response = response.json()
        return response["results"]

    def get_deposits(self) -> list:
        """Get list of deposits

        Returns
        -------
        list
            A list of dictionaries containing deposit objects
        """
        response = self.TradeAPI.makeRequest("GET", "deposits")
        response = response.json()
        return response["results"]

    def get_forex(self) -> dict:
        """Get foreign exchange rate

        Returns
        -------
        dict
            A dictionary containing foreign exchange rates
        """
        response = self.TradeAPI.makeRequest("GET", "forex")
        return response.json()

    def get_activitiesAllActivities(self, bookmark=None, limit=None, filters = None) -> list:
        """Get Wealthsimple Trade activities

        Returns
        -------
        list
            A list of dictionaries containing Wealthsimple Trade activities
        """
        mainList = []
        response = self.TradeAPI.makeRequest(
            "GET", f"account/activities?limit={limit}{filters}&bookmark={bookmark}")
        # https://trade-service.wealthsimple.com/account/activities?account_ids=&limit=20&type=buy&type=sell&type=dividend
        response = response.json()
        mainList.append(response)
        return response

    def getGraphQl(self) -> dict:
        accountIds = self.get_account_ids()
        today = str(date.today())

        payload = json.dumps({
        "operationName": "FetchActivityFeedItems",
        "variables": {
            "orderBy": "OCCURRED_AT_DESC",
            "condition": {
            "accountIds": accountIds,
            "endDate": today
            },
            "first": 10000        },
        "query": "query FetchActivityFeedItems($first: Int, $cursor: Cursor, $condition: ActivityCondition, $orderBy: [ActivitiesOrderBy!] = OCCURRED_AT_DESC) {\n  activityFeedItems(\n    first: $first\n    after: $cursor\n    condition: $condition\n    orderBy: $orderBy\n  ) {\n    edges {\n      node {\n        ...Activity\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Activity on ActivityFeedItem {\n  accountId\n  aftOriginatorName\n  aftTransactionCategory\n  aftTransactionType\n  amount\n  amountSign\n  assetQuantity\n  assetSymbol\n  canonicalId\n  currency\n  eTransferEmail\n  eTransferName\n  externalCanonicalId\n  identityId\n  institutionName\n  occurredAt\n  p2pHandle\n  p2pMessage\n  spendMerchant\n  securityId\n  billPayCompanyName\n  billPayPayeeNickname\n  redactedExternalAccountNumber\n  opposingAccountId\n  status\n  subType\n  type\n  strikePrice\n  contractType\n  expiryDate\n  chequeNumber\n  provisionalCreditAmount\n  primaryBlocker\n  interestRate\n  frequency\n  counterAssetSymbol\n  rewardProgram\n  counterPartyCurrency\n  counterPartyCurrencyAmount\n  counterPartyName\n  fxRate\n  fees\n  reference\n  __typename\n}"
        })
        
        print(payload)
        
        response = self.TradeAPI.makeRequest("POST", useGraph=True , endpoint="", jsonData=payload)
        print(response)
        return response


    
    