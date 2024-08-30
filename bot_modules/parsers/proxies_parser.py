
## Built-in modules:
from typing import Union, NoReturn
from typing import Dict, List, Any
from json import JSONDecodeError

## Pip modules:
from requests import get
from requests import Response
from requests.exceptions import ConnectionError
from fake_headers import Headers


class ProxiesParser(object):
    """Proxies parser from open API.

    Args:
        object (class): Basic inheritance class.
    """
    def __init__(
        self,
        protocol: str,
        limit: int = 50,
        page: int = 1,
        sort_by: str = "speed",
        browser: str = None,
        countries_to_ignore: Union[List[str], None] = None
    ) -> None:
        """Initialization the ProxiesParser.

        Args:
            protocol (str): proxies protocol:
                [
                    http,
                    https,
                    socks4,
                    socks5
                ]
            limit (int, optional): Proxies limit to get. Defaults to 50. 
                Min = 50, Max = 500.
            page (int, optional): Proxies page to get. Defaults to 1.
            sort_by (str, optional): Sort type for proxies. Defaults to "speed".
                [
                    speed,
                    lastChecked,
                    upTime,
                    responseTime,
                    county
                ]
            browser (str, optional): Browser name for headers. Defaults to "None".
                [
                    chrome,
                    firefox,
                    opera
                ]
            countries_to_ignore (List[str], optional): Countries that parser will
                be ignore. You need to type there list with str values like:
                [
                    "RU",
                    "ID",
                    "US",
                    "BR",
                    ...
                ]
                Defaults to ignore.
        """
        self.API_URL: str = f"https://proxylist.geonode.com/api/proxy-list?\
            protocols={protocol}&\
            limit={limit}&\
            page={page}&\
            sort_by={sort_by}&\
            sort_type=asc"
        self._headers: Dict[str, Any] = self._generate_headers(browser=browser)
        self.countries_to_ignore: Union[List[str], None] = countries_to_ignore
        self.proxies: List[str] = self._fetch_proxies_from_response()
        
        return None


    @classmethod
    def _generate_headers(
        cls,
        browser: str
    ) -> Dict[str, Any]:
        """Generate fake random headers for parsing API url.

        Returns:
            dict: dictionary with headers.
        """
        headers: Headers = Headers(
            browser=browser,
            os=None,
            headers=True
        )
        
        return headers.generate()


    @staticmethod
    def _check_response_status(response: Response) -> Union[bool, NoReturn]:
        """Check is response status is correct.

        Args:
            response (Response): Response object.

        Returns:
            bool: True/False. True if status is correct. Else - False.
        
        Raises:
            ConnectionError: if status code is uncorrect.
        """
        ## If response status is correct.
        if response.ok:
            return True
        else:
            raise ConnectionError(
                f"""
                An error has occured in ProxiesParser:
                    Can't get information from {response.url}.
                    Request is {response.request}
                    Response status is {response.status_code}.
                """,
                request=response.request,
                response=response,
            )


    def _get_response_from_api(self) -> Union[Response, NoReturn]:
        """Get response from API url and check it's 
        status code.

        Returns:
            Response: Response from  proxies API url.
        """
        response: Response = get(
            url=self.API_URL,
            headers=self._headers
        )
        
        if self._check_response_status(response=response):
            return response


    def _fetch_proxies_from_response(self) -> List[str]:
        """Fetch proxies from response.

        Returns:
            dict: Fetched and structured response.
        """
        response: Response = self._get_response_from_api()
        ## Converting response to json. We'll get structure like this:
        ## data: {
        ##  0: {...},
        ##  1: {...},
        ##  ... 
        ## }
        try:
            json_response: Dict[str, Any] = response.json()
        except JSONDecodeError:
            print(
                """ 
                Can't decode json response from API url.
                Just try to send new request to API url again. This may work.
                """
            )
            return None

        ## Get data from dict.
        DATA_KEY_DICT: str = "data"
        ## Get another structure:
        ## [
        ##  {...},
        ##  {...},
        ##  ... 
        ## ]
        all_proxies: List[Dict[Any]] = json_response.get(DATA_KEY_DICT)
        ## This will be a list with allowed IPs and PORTs.
        acceptable_proxy: List[str] = []
        ## Create variables with dict component names.
        PROXY_IP_KEY: str = "ip"
        PROXY_PORT_KEY: str = "port"
        PROXY_COUNTRY_KEY: str = "country"
        
        for proxy_data in all_proxies:
            proxy_country: str = proxy_data.get(PROXY_COUNTRY_KEY)
            ## Check if country is allowed.
            if proxy_country in self.countries_to_ignore:
                continue
            proxy_ip: str = proxy_data.get(PROXY_IP_KEY)
            proxy_port: str = proxy_data.get(PROXY_PORT_KEY)
            ## Append proxy connection information to the list. 
            acceptable_proxy.append(f"{proxy_ip}:{proxy_port}")
        
        return acceptable_proxy