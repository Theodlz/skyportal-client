import requests

def api_skyportal(method: str, url: str, endpoint: str, data=None, token=None):
    """Make an API call to a SkyPortal instance
    :param method:
    :param endpoint:
    :param data:
    :return:
    """
    method = method.lower()

    if endpoint is None:
        raise ValueError("Endpoint not specified")
    if method not in ["head", "get", "post", "put", "patch", "delete"]:
        raise ValueError(f"Unsupported method: {method}")

    if method == "get":
        response = requests.request(
            method,
            url+endpoint,
            params=data,
            headers={"Authorization": f"token {token}"} if token else None,
        )
    else:
        response = requests.request(
            method,
            url+endpoint,
            json=data,
            headers={"Authorization": f"token {token}"} if token else None,
        )

    return response

def get_followup_request(followup_request_id, url, token):
        response = api_skyportal("get", url, f"/api/followup_request/{followup_request_id}", token=token)
        if response.status_code != 200:
                raise ValueError(f"Error: {response.status_code} {response.text}")
        return response.json()['data']

def get_obsplan(obsplan_id, url, token):
        response = api_skyportal("get", url, f"/api/observation_plan/{obsplan_id}", token=token)
        if response.status_code != 200:
                raise ValueError(f"Error: {response.status_code} {response.text}")
        return response.json()['data']
