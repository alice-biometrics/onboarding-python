import time
from typing import Any, Callable, Optional

from requests import Response


def timeit(func: Callable[..., Any]) -> Callable[..., Any]:
    def timed(*args: Any, **kwargs: Any) -> Any:
        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()
        if "verbose" in kwargs and kwargs["verbose"]:
            print(f"elapsed time: {te - ts:.2f} s")
            print("=================================\n")
        return result

    return timed


def print_intro(method_name: str, verbose: Optional[bool] = False) -> None:
    if verbose:
        print("=================================")
        print(f"method: {method_name}")


def print_response(response: Response, verbose: Optional[bool] = False) -> None:
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


def print_token(type_token: str, token: str, verbose: Optional[bool] = False) -> None:
    if verbose:
        print(f"{type_token}: {token}")
