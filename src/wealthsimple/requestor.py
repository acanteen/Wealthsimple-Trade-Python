import json


class APIRequestor:
    """
    A class to simplify request calls to REST API

    Attributes
    ----------
    session : session
        A requests Session object to be associated with the class
    APIMainURL : str
        Main URL endpoint for API

    Methods
    -------
    makeRequest(method, endpoint, params=None, returnValue=None)
        Make a request to a given API endpoint
    post(URL, params=None)
        Make a POST request to a given API endpoint
    get(URL, params=None)
        Make a GET request to a given API endpoint
    """

    def __init__(self, session, APIMainURL):
        """
        Parameters
        ----------
        session : Session
            A requests Session object to be associated with the class
        APIMainURL : str
            Main URL endpoint for API
        """
        self.session = session
        self.APIMainURL = APIMainURL

    def makeRequest(self, method,  endpoint, useGraph=None, params=None, jsonData=None, returnValue=None):
        """Make a request to a given API endpoint

        Parameters
        ----------
        method : str
            Specify POST or GET request
        endpoint : str
            URL endpoint oof API (Does not include base URL)
        params : dict
            Dictionary of parameters to be passed with request

        Returns
        -------
        Response : Response
            A requests response object
        """
        if(useGraph):
            URL="https://my.wealthsimple.com/graphql"
        else:
            URL = self.APIMainURL + endpoint
        
        print("++++++++++++++++++++++++++++++++++++++++++++",URL)
        if method == "POST":
            return self.post(URL, params=params,jsonData=jsonData)
        elif method == "GET":
            # print(URL)
            return self.get(URL, params)
        else:
            raise Exception(f"Invalid request method: {method}")

    def post(self, URL, params=None,jsonData=None):
        """Make a POST request to a given API endpoint

        Parameters
        ----------
        URL : str
            Full URL endpoint of API
        params : dict
            Dictionary of parameters to be passed with request

        Returns
        -------
        Response : Response
            A requests response object
        """
        print(jsonData)
        try:
            return self.session.post(URL, params,jsonData)
        except Exception as err:
            print(err)

    def get(self, URL, params=None):
        """Make a GET request to a given API endpoint

        Parameters
        ----------
        URL : str
            Full URL endpoint of API
        params : dict
            Dictionary of parameters to be passed with request

        Returns
        -------
        Response : Response
            A requests response object
        """
        auth = self.session.headers["Authorization"]
        response = self.session.get(URL, headers={"Authorization": auth})
        return response
