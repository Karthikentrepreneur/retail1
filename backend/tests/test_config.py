from app.core.config import settings


def test_settings_defaults():
    assert settings.environment == "dev"
    assert settings.access_token_expire_minutes == 15
