def check_response_status(response):
    """Check if an API response is successful."""
    if response.status_code != 200:
        raise Exception(f"API Request failed with status {response.status_code}: {response.text}")
    return response

