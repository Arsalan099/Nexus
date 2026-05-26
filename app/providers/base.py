"""
NEXUS Base Provider Protocol

Defines the contract every LLM provider must fulfill.
Business logic never imports anthropic or ollama directly —
it only speaks this interface.

This means:
- Providers are swappable without changing business logic
- Testing is easy (mock this interface, not the real APIs)
- Adding new providers requires zero changes to existing code
"""

from typing import Protocol, AsyncGenerator, runtime_checkable
from dataclasses import dataclass


@dataclass
class Message:
    """
    A single message in a conversation.

    role: who sent it — 'user', 'assistant', or 'system'
    content: the text content of the message

    We use a dataclass here (not Pydantic) because this is
    an internal data structure, not an API contract.
    Pydantic is for API boundaries. Dataclasses for internals.
    """
    role: str
    content: str


@dataclass
class LLMResponse:
    """
    A complete response from any LLM provider.

    content: the generated text
    model: which model actually generated this
    provider: which provider was used
    input_tokens: tokens consumed by the prompt
    output_tokens: tokens consumed by the response

    Tracking tokens matters for:
    - Cost calculation (you pay per token)
    - Context window management (models have limits)
    - Usage analytics
    """
    content: str
    model: str
    provider: str
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        """Total tokens consumed by this request."""
        return self.input_tokens + self.output_tokens


@dataclass
class LLMConfig:
    """
    Configuration for a single LLM call.

    These are the knobs you can turn per-request.
    Having them in one object means the provider interface
    stays stable even as we add new configuration options.
    """
    temperature: float = 0.7
    max_tokens: int = 1000
    system_prompt: str = "You are NEXUS, a helpful AI assistant."


@runtime_checkable
class BaseLLMProvider(Protocol):
    """
    The contract every LLM provider must fulfill.

    @runtime_checkable means we can use isinstance() checks:
        isinstance(provider, BaseLLMProvider)
    This is useful in the router for validation.

    Any class that implements these three methods
    automatically qualifies as a BaseLLMProvider —
    no inheritance required.
    """

    @property
    def provider_name(self) -> str:
        """
        Unique identifier for this provider.
        Used in logging, error messages, and LLMResponse.
        Example: 'anthropic', 'ollama'
        """
        ...

    async def complete(
        self,
        messages: list[Message],
        config: LLMConfig | None = None,
    ) -> LLMResponse:
        """
        Generate a complete response and return it all at once.

        Use when: you need the full response before doing anything
        Example: generating structured data you need to parse

        Args:
            messages: conversation history in chronological order
            config: generation parameters (temperature, max_tokens, etc.)

        Returns:
            Complete LLMResponse with content and token usage

        Raises:
            ProviderUnavailableException: if provider cannot be reached
            ProviderAuthException: if authentication fails
            ProviderRateLimitException: if rate limits are hit
        """
        ...

    async def stream(
        self,
        messages: list[Message],
        config: LLMConfig | None = None,
    ) -> AsyncGenerator[str, None]:
        """
        Stream response tokens as they're generated.

        Use when: showing text appearing word-by-word in UI
        Example: chat interface where users see the response build

        Args:
            messages: conversation history in chronological order
            config: generation parameters

        Yields:
            String chunks as they arrive from the model

        Raises:
            ProviderUnavailableException: if provider cannot be reached
            ProviderAuthException: if authentication fails
        """
        ...

    async def health_check(self) -> bool:
        """
        Verify this provider is reachable and functional.

        Used by:
        - The router before deciding which provider to use
        - The /health endpoint to report system status
        - Startup validation

        Returns:
            True if provider is healthy, False otherwise
            Never raises — always returns bool
        """
        ...