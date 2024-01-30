import pytest
from meiga import Error, Result, early_return, isSuccess

from alice import Config, DeviceInfo, Onboarding, UserInfo
from alice.auth.auth_errors import AuthError
from alice.onboarding.enums.onboarding_steps import OnboardingStep, OnboardingStepName


@pytest.mark.unit
def test_should_return_an_error_when_the_api_key_is_not_configured():
    config = Config()
    onboarding = Onboarding.from_config(config)

    result = onboarding.create_flow(
        steps=[OnboardingStep(step=OnboardingStepName.SELFIE)],
        default=True,
        name="test",
    )

    result.assert_failure()


@pytest.mark.unit
def test_should_timeout_when_time_exceeded(given_valid_api_key):
    config = Config(api_key=given_valid_api_key, timeout=0.01)
    onboarding = Onboarding.from_config(config)

    result = onboarding.create_flow(
        steps=[OnboardingStep(step=OnboardingStepName.SELFIE)],
        default=True,
        name="test",
    )
    result.assert_failure(value_is_instance_of=AuthError)
    assert result.value.code == 408


@pytest.mark.unit
def test_should_do_complete_flow_process(given_valid_api_key):
    @early_return
    def do_complete_flow() -> Result[bool, Error]:
        config = Config(api_key=given_valid_api_key)
        onboarding = Onboarding.from_config(config)

        flow_id = onboarding.create_flow(
            steps=[OnboardingStep(step=OnboardingStepName.SELFIE)],
            default=False,
            name="alice-flow-test-onboarding-python",
        ).unwrap_or_return()

        _ = onboarding.retrieve_flow(flow_id=flow_id).unwrap_or_return()

        user_id = onboarding.create_user(
            user_info=UserInfo(first_name="Alice", last_name="Biometrics"),
            flow_id=flow_id,
            device_info=DeviceInfo(device_platform="Android"),
        ).unwrap_or_return()

        _ = onboarding.get_user_flow(
            user_id=user_id,
        ).unwrap_or_return()

        _ = onboarding.update_flow(
            flow_id=flow_id,
            steps=[
                OnboardingStep(step=OnboardingStepName.SELFIE),
                OnboardingStep(step=OnboardingStepName.IDCARD),
            ],
            default=False,
            name="alice-flow-test-onboarding-python-updated",
        ).unwrap_or_return()

        _ = onboarding.retrieve_flows().unwrap_or_return()

        onboarding.delete_flow(flow_id).unwrap_or_return()
        onboarding.delete_user(user_id).unwrap_or_return()

        return isSuccess

    result = do_complete_flow()

    result.assert_success()
