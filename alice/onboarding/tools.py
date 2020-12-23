import time

from requests import Response


def timeit(func):
    def timed(*args, **kw):
        ts = time.time()
        result = func(*args, **kw)
        te = time.time()
        if "verbose" in kw and kw["verbose"]:
            print("elapsed time: {:.2f} s".format(te - ts))
            print("=================================\n")
        return result

    return timed


def print_intro(method_name: str, verbose: bool = False):
    if verbose:
        print("=================================")
        print(f"method: {method_name}")


def print_response(response: Response, verbose: bool = False):
    if verbose:
        headers = response.headers
        content_type = headers["Content-Type"]
        if "image" in content_type or "video" in content_type:
            print(f"response {response.status_code} -> {content_type}")
        else:
            text = response.text
            if text[-1:] == "\n":
                text = text[:-1]
            if text == "":
                print(f"response {response.status_code} -> {content_type}")
            else:
                print(f"response {response.status_code} -> {content_type} \n{text}")


def print_token(type_token: str, token: str, verbose: bool = False):
    if verbose:
        print(f"{type_token}: {token}")
