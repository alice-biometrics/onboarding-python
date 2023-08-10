import os
import secrets
from typing import Optional

from meiga.assertions import assert_success

from alice import Config, Webhook, Webhooks

RESOURCES_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../resources"


def configure_webhooks(api_key: str, verbose: Optional[bool] = False) -> None:
    config = Config(api_key=api_key, verbose=verbose)
    webhooks_client = Webhooks.from_config(config)

    # Check Available events
    subscriptable_events = webhooks_client.get_subscriptable_events().unwrap_or_raise()
    selected_event = subscriptable_events[0]

    # Create a new Webhook
    webhook = Webhook(
        active=True,
        post_url="http://google.com",
        api_key="b0b905d6-228f-44bf-a130-c85d7aecd765",
        event_name=selected_event.get("name"),
        event_version=selected_event.get("version"),
        secret=str(secrets.token_hex(20)),
    )
    webhook_id = webhooks_client.create_webhook(webhook).unwrap_or_raise()

    # Update an existent Webhook
    webhook_to_update = Webhook(
        webhook_id=webhook_id,  # Needed if we want to update
        active=False,
        post_url="http://alicebiometrics.com",
        api_key="b0b905d6-228f-44bf-a130-c85d7aecd765",
        event_name="user.created",
        event_version="1",
        algorithm="sha512",
        secret=str(secrets.token_hex(20)),
    )
    webhooks_client.update_webhook(webhook_to_update).unwrap_or_raise()

    # Update the activation of a Webhook
    webhooks_client.update_webhook_activation(webhook_id, True)
    retrieved_webhook = webhooks_client.get_webhook(webhook_id).unwrap_or_raise()
    assert retrieved_webhook.active

    # Send a ping using configured webhook
    result = webhooks_client.ping_webhook(webhook_id)

    # Retrieve an existent Webhook
    retrieved_webhook = webhooks_client.get_webhook(webhook_id).unwrap_or_raise()
    assert retrieved_webhook.active
    breakpoint()
    assert retrieved_webhook.post_url == "http://alicebiometrics.com"

    # Retrieve all configured webhooks
    retrieved_webhooks = webhooks_client.get_webhooks().unwrap()

    # Delete a configured webhook
    result = webhooks_client.delete_webhook(webhook_id)
    assert_success(result)

    # Retrieve all webhook results of a specific webhook
    webhook_results = webhooks_client.get_webhook_results(webhook_id).unwrap_or_raise()

    # Retrieve las webhook result of a specific webhook
    last_webhook_result = webhooks_client.get_last_webhook_result(
        webhook_id
    ).unwrap_or_raise()


if __name__ == "__main__":
    api_key = os.environ.get("ONBOARDING_API_KEY")
    if api_key is None:
        raise AssertionError(
            "Please configure your ONBOARDING_API_KEY to run the example"
        )
    print("Running webhook configuration...")

    configure_webhooks(api_key=api_key, verbose=True)
