import httpx

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.60"
}

def http_get(url):
    with httpx.Client(headers=headers) as client:
        r = client.get(url, follow_redirects=True)
        return r.text if r.status_code == httpx.codes.OK else None
