from pydantic import Field
from pydantic_settings import BaseSettings

from authentication.models import User
from common.logger_level import LoggerLevel


class Config(BaseSettings):
    # Pydantic-settings in pydantic v2 automatically fetch config settings from env-variables
    ENVIRONMENT: str = "local"

    # Logging
    LOGGER_LEVEL: LoggerLevel = Field(default=LoggerLevel.INFO)
    APPINSIGHTS_CONSTRING: str | None = None

    # Database
    MONGODB_USERNAME: str = "dummy"
    MONGODB_PASSWORD: str = "dummy"  # noqa: S105
    MONGODB_HOSTNAME: str = "db"
    MONGODB_DATABASE: str = "test"
    MONGODB_PORT: int = 27017

    # Access control
    APPLICATION_ADMIN: str = "admin"
    APPLICATION_ADMIN_ROLE: str = "admin"

    # Authentication
    SECRET_KEY: str | None = None
    AUTH_ENABLED: bool = False
    JWT_SELF_SIGNING_ISSUER: str = "APPLICATION"  # Which value will be used to sign self-signed JWT's
    TEST_TOKEN: bool = False  # This value should only be changed at runtime by test setup
    OAUTH_WELL_KNOWN: str | None = None
    OAUTH_TOKEN_ENDPOINT: str = ""
    OAUTH_AUTH_ENDPOINT: str = ""
    OAUTH_CLIENT_ID: str = ""
    OAUTH_AUTH_SCOPE: str = ""
    OAUTH_AUDIENCE: str = ""
    MICROSOFT_AUTH_PROVIDER: str = "login.microsoftonline.com"

    @property
    def log_level(self) -> str:
        """Returns LOGGER_LEVEL as a (lower case) string."""
        return str(self.LOGGER_LEVEL.value).lower()


config = Config()

if config.AUTH_ENABLED and not all((config.OAUTH_AUTH_ENDPOINT, config.OAUTH_TOKEN_ENDPOINT, config.OAUTH_WELL_KNOWN)):
    raise ValueError("Authentication was enabled, but some auth configuration parameters are missing")

if not config.AUTH_ENABLED:
    print("\n")
    print("################ WARNING ################")
    print("#       Authentication is disabled      #")
    print("################ WARNING ################\n")

default_user: User = User(
    user_id="nologin",
    full_name="Not Authenticated",
    email="nologin@example.com",
)
