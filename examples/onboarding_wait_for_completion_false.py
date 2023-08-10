import os
from time import sleep
from typing import Optional

from alice import Config, Onboarding
from alice.onboarding.enums.version import Version

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


def onboarding_example(api_key: str, verbose: Optional[bool] = False) -> None:
    config = Config(
        api_key=api_key,
        verbose=verbose,
    )
    onboarding = Onboarding.from_config(config)

    selfie_media_data = given_any_selfie_image_media_data()

    user_id = onboarding.create_user().unwrap_or_raise()

    onboarding.get_user_status(user_id).unwrap_or_raise()

    # Upload a selfie (Recommended 1-second video)
    onboarding.add_selfie(
        user_id=user_id, media_data=selfie_media_data, wait_for_completion=True
    ).unwrap_or_raise()

    print("Waiting 4 seconds...")
    sleep(4)

    # Generate the report
    report = onboarding.create_report(
        user_id=user_id, version=Version.V1
    ).unwrap_or_raise()

    if verbose:
        print(f"report: {report}")

    href = report.selfies[0].media.get("cropped_face").href
    media = onboarding.download(user_id=user_id, href=href).unwrap_or_raise()
    assert isinstance(media, bytes)


def given_any_selfie_image_media_data() -> bytes:
    with open(f"{RESOURCES_PATH}/selfie.png", "rb") as f:
        return f.read()


if __name__ == "__main__":
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the example"
        )
    print("Running onboarding example...")
    onboarding_example(api_key=api_key, verbose=True)
