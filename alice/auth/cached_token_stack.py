import sys
from collections import OrderedDict
from typing import Union

from alice.auth.token_tools import is_valid_token
from alice.onboarding.tools import timeit


class CachedTokenStack:
    _data: OrderedDict  # type: ignore

    def __init__(self, max_size: int = 5000):
        self._data = OrderedDict()
        self._max_size = max_size

    def __repr__(self) -> str:
        size = len(self._data)
        memory = sys.getsizeof(self._data)
        return f"CachedTokenStack: [size={size} tokens | memory = {memory} bytes]"

    def add(self, user_id: str, token: str) -> None:
        self._data[user_id] = token

    def get(self, user_id: str) -> Union[str, None]:
        token = self._data.get(user_id)

        if token:
            # If token exists take advantage of the saved time and clear expired tokens and keep max size.
            self._clear_expired_tokens()
            self._clear_if_max_size_has_been_exceeded()
        return token  # type: ignore

    def __len__(self) -> int:
        return len(self._data)

    def show(self) -> None:
        print(self.__repr__())
        print(
            "-----------------------------------      CachedTokenStack     -----------------------------------------"
        )
        for user_id, token in self._data.items():
            print(f"{user_id} (valid={is_valid_token(token)}): {token} ")
        print(
            "-------------------------------------------------------------------------------------------------------"
        )

    @timeit
    def _clear_expired_tokens(self) -> None:
        num_data = len(self._data)

        if num_data > 0:
            latest_expired_token = None
            for i, token in enumerate(reversed(list(self._data.values()))):
                if not is_valid_token(token):
                    latest_expired_token = token
                    break

            if latest_expired_token:
                exist_expired_tokens = True

                while exist_expired_tokens:
                    _, token = self._data.popitem(last=False)
                    if token == latest_expired_token:
                        exist_expired_tokens = False

    def _clear_if_max_size_has_been_exceeded(self) -> None:
        num_items = len(self._data)

        if num_items > self._max_size:
            num_to_delete = num_items - self._max_size
            for _ in range(num_to_delete):
                self._data.popitem(last=False)

            num_items = len(self._data)
