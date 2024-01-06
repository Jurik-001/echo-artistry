class OpenAIError(Exception):
    """General error in OpenAI Client."""

    pass


class ContentPolicyViolation(OpenAIError):
    """Content policy violation."""

    pass
