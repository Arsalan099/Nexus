"""
NEXUS Exception Hierarchy

All custom exceptions are defined here.
This gives us:
1. Specific error types we can catch precisely
2. Consistent error structure across the entire app
3. Clean separation between user-facing messages and internal details
4. HTTP status codes attached to exceptions at definition time
"""


class NexusBaseException(Exception):
    """
    Root exception for all NEXUS errors.

    Every custom exception inherits from this,
    which means you can catch all NEXUS errors
    with a single except clause when needed.
    """

    def __init__(self, message: str, status_code: int = 500, details: dict | None = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


# ─── Provider Exceptions ──────────────────────────────────────────────────────

class ProviderException(NexusBaseException):
    """Base for all LLM provider errors."""
    pass


class ProviderUnavailableException(ProviderException):
    """
    Raised when a provider cannot be reached.
    Triggers fallback logic in the router.

    Example: Anthropic API is down, timeout on connection.
    """

    def __init__(self, provider_name: str, reason: str = ""):
        super().__init__(
            message=f"Provider '{provider_name}' is unavailable. {reason}".strip(),
            status_code=503,
            details={"provider": provider_name, "reason": reason},
        )


class ProviderAuthException(ProviderException):
    """
    Raised when authentication fails.
    Should NOT trigger fallback — this is a config error, not a transient failure.

    Example: Invalid API key, expired credentials.
    """

    def __init__(self, provider_name: str):
        super().__init__(
            message=f"Authentication failed for provider '{provider_name}'. Check your API key.",
            status_code=401,
            details={"provider": provider_name},
        )


class ProviderRateLimitException(ProviderException):
    """
    Raised when rate limits are hit.
    Should trigger fallback with backoff.

    Example: Too many requests per minute to Anthropic.
    """

    def __init__(self, provider_name: str, retry_after: int | None = None):
        details: dict = {"provider": provider_name}
        if retry_after:
            details["retry_after_seconds"] = retry_after

        super().__init__(
            message=f"Rate limit hit for provider '{provider_name}'.",
            status_code=429,
            details=details,
        )


# ─── Configuration Exceptions ─────────────────────────────────────────────────

class ConfigurationException(NexusBaseException):
    """
    Raised when the app is misconfigured.
    These should surface loudly at startup, not silently at runtime.

    Example: PRIMARY_PROVIDER set to 'gemini' which doesn't exist.
    """

    def __init__(self, setting_name: str, reason: str):
        super().__init__(
            message=f"Configuration error for '{setting_name}': {reason}",
            status_code=500,
            details={"setting": setting_name, "reason": reason},
        )


# ─── Chat Exceptions ──────────────────────────────────────────────────────────

class ChatException(NexusBaseException):
    """Base for chat-level errors."""
    pass


class InvalidMessageException(ChatException):
    """
    Raised when a message fails validation.

    Example: Empty message, message exceeds token limit.
    """

    def __init__(self, reason: str):
        super().__init__(
            message=f"Invalid message: {reason}",
            status_code=422,
            details={"reason": reason},
        )