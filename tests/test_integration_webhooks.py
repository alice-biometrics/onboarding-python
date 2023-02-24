import os
import secrets
from time import sleep

import pytest
from meiga.assertions import assert_failure, assert_success

from alice import Config, Webhook, Webhooks


@pytest.mark.unit
def test_should_return_an_error_when_the_api_key_is_not_configured():

    config = Config()
    webhooks_client = Webhooks.from_config(config)

    result = webhooks_client.get_webhooks()

    assert_failure(result)


@pytest.mark.unit
def test_should_execute_all_webhook_lifecycle(given_valid_api_key):
    config = Config(api_key=given_valid_api_key)
    webhooks_client = Webhooks.from_config(config)

    # Check Available events
    result = webhooks_client.get_available_events()
    assert_success(result, value_is_instance_of=list)
    selected_event = result.value[0]

    # Create a new Webhook
    webhook = Webhook(
        active=True,
        post_url="http://google.com",
        api_key="b0b905d6-228f-44bf-a130-c85d7aecd765",
        event_name=selected_event.get("name"),
        event_version=selected_event.get("version"),
        secret=str(secrets.token_hex(20)),
    )
    webhook_id = webhooks_client.create_webhook(webhook=webhook).unwrap_or_return()

    # Update an existent Webhook
    new_post_url = "http://alicebiometrics.com"
    webhook_to_update = Webhook(
        webhook_id=webhook_id,  # Needed if we want to update
        active=False,
        post_url=new_post_url,
        api_key="b0b905d6-228f-44bf-a130-c85d7aecd765",
        event_name="user_created",
        event_version="1",
        algorithm="sha512",
        secret=str(secrets.token_hex(20)),
    )
    result = webhooks_client.update_webhook(webhook_to_update)
    assert_success(result)
    retrieved_webhook = webhooks_client.get_webhook(webhook_id).unwrap()
    assert retrieved_webhook.post_url == new_post_url
    assert not retrieved_webhook.active

    # Update Webhook activation
    result = webhooks_client.update_webhook_activation(webhook_id, True)
    assert_success(result)
    retrieved_webhook = webhooks_client.get_webhook(webhook_id).unwrap()
    assert retrieved_webhook.active

    # Send a ping using configured webhook
    result = webhooks_client.ping_webhook(webhook_id)
    assert_success(result)

    # Retrieve an existent Webhook
    retrieved_webhook = webhooks_client.get_webhook(webhook_id).unwrap()
    assert retrieved_webhook.active
    assert retrieved_webhook.post_url == "http://alicebiometrics.com"

    # Retrieve all configured webhooks
    result = webhooks_client.get_webhooks()
    assert_success(result, value_is_instance_of=list)

    sleep(2.0)

    # Retrieve las webhook result of an specific webhook
    result = webhooks_client.get_last_webhook_result(webhook_id)
    assert_success(result, value_is_instance_of=dict)

    # Retrieve all webhook results of an specific webhook
    result = webhooks_client.get_webhook_results(webhook_id)
    assert_success(result, value_is_instance_of=list)
    assert len(result.value) > 0

    # Retrieve all webhook results of an specific webhook
    result = webhooks_client.get_webhook_results(webhook_id)
    assert_success(result, value_is_instance_of=list)

    # Delete a configured webhook
    result = webhooks_client.delete_webhook(webhook_id)
    assert_success(result)

    sleep(3.0)

    assert_webhook_results_status(webhooks_client, webhook_id)


def assert_webhook_results_status(webhooks_client: Webhooks, webhook_id: str):
    if os.getenv("CONCURRENT_TESTING", False):
        webhooks_client.get_webhook_results(webhook_id)
    else:
        # Expected not found error when Retrieve all webhook results of an deleted webhook
        result = webhooks_client.get_webhook_results(webhook_id)
        assert_failure(result)
