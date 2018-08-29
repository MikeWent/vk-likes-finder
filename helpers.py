import time
import random

import requests

class VKAPIError(Exception):
    def __init__(self, message):
        self.message = message

class VKAPI:
    def __init__(self, access_token, version="5.80"):
        """Simple vk.com API wrapper
        
        Arguments:
            access_token {str} -- account access token
        
        Keyword Arguments:
            version {str} -- API version (default: "5.80")
        """

        self.url = "https://api.vk.com/method/{}"
        self.required_params = {"access_token": access_token,
                                "v": version}
        
    def method(self, name, **params):
        """Execute method (see vk.com/dev/methods) with passed params
        
        Arguments:
            name {str} -- method name
        
        Raises:
            VKAPIError -- common VK API error
        
        Returns:
            list, dict -- VK API 'response' object
        """

        if params:
            params.update(self.required_params)
        else:
            params = self.required_params
        r = requests.post(self.url.format(name), data=params)
        response = r.json()
        if response.get("error"):
            raise VKAPIError(response["error"]["error_msg"])
        else:
            return response.get("response", None)


def delay():
    """Sleep 0.3-0.5 seconds"""
    try:
        time.sleep(random.randint(3, 5) / 10)
    except KeyboardInterrupt:
        exit()


def token_is_valid(access_token):
    """Check access token by making a test request"""
    try:
        VKAPI(access_token).method("utils.getServerTime")
        return True
    except VKAPIError:
        return False
