import os
from typing import Optional

from alice import Config, Onboarding

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


def onboarding_configure_flows(api_key: str, verbose: Optional[bool] = False) -> None:
    config = Config(api_key=api_key, verbose=verbose)
    onboarding = Onboarding.from_config(config)

    flows = onboarding.retrieve_flows().unwrap_or_raise()
    print(f"{flows=}")

    flow_id = flows[0].get("id")

    flow = onboarding.retrieve_flow(flow_id).unwrap_or_raise()
    print(f"{flow=}")

    default_flow = onboarding.retrieve_flow().unwrap_or_raise()
    print(f"{default_flow=}")


if __name__ == "__main__":
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the example"
        )
    print("Running configure flows example...")
    onboarding_configure_flows(api_key=api_key, verbose=True)
