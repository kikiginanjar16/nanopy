import httpx
from pydantic import BaseModel

class ChatMessage(BaseModel):
    role: str
    content: str


class ProviderError(Exception):
    pass

class OpenAICompatProvider:
    def __init__(self, api_key, base_url, model):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def chat(self, messages):
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": [m.model_dump() for m in messages],
            "temperature": 0.3,
        }

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                r = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                r.raise_for_status()
                data = r.json()
        except httpx.HTTPStatusError as e:
            detail = e.response.text.strip()
            detail = detail[:300] if detail else "no response body"
            raise ProviderError(
                f"HTTP {e.response.status_code} from provider at {self.base_url}: {detail}"
            ) from e
        except httpx.RequestError as e:
            raise ProviderError(f"Network error while contacting provider: {e}") from e

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as e:
            raise ProviderError("Provider returned an unexpected response format.") from e
