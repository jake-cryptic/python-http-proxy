from bottle import route, run, request
from urllib.parse import unquote, urlparse
from requests import Session
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from socket import getaddrinfo


s = Session()
s.mount('http://', HTTPAdapter(max_retries=1))
s.mount('https://', HTTPAdapter(max_retries=1))


def uri_validator(x):
    try:
        # This will fail if not a valid URL
        result = urlparse(x)

        # This will fail if DNS hostname does not exist
        dns = getaddrinfo(result.hostname, result.port)

        return all([result.scheme, result.netloc])
    except:
        return False


# https://stackoverflow.com/questions/15445981/how-do-i-disable-the-security-certificate-check-in-python-requests
def make_req(url):
    auth = None
    if request.auth is not None:
        print(f'Added HTTP auth: {request.auth}')
        auth = HTTPBasicAuth(request.auth[0], request.auth[1])

    return s.request(
        method=request.method,
        url=url,
        verify=False,
        auth=auth
    )


@route('/<url:re:.+>')
def proxy(url):
    safe_url = unquote(url)

    if not uri_validator(safe_url):
        print(f'Not getting URL: {safe_url}')
        return f'Failed request, {safe_url} is not valid or contactable'
    else:
        print(f'Request {request.method} to {safe_url}')

    try:
        resp = make_req(safe_url)
    except:
        return f'Failed request {request.method} to {safe_url}'

    return resp.text


run(host='localhost', port=8080)
