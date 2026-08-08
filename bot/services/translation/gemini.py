from config import ANN_TRANSLATION_PROMPT
from google import genai
from google.genai import types


async def translate_to_english(message: str) -> str:
    client = genai.Client()

    try:
        response = await client.aio.models.generate_content(
            model="gemini-3.6-flash",
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=ANN_TRANSLATION_PROMPT,
            ),
        )

        return response.text

    finally:
        await client.aio.aclose()
