from openai import OpenAI

from utils.config import (
    OPENAI_API_KEY,
    MODEL_NAME
)

client = OpenAI(
    api_key=OPENAI_API_KEY
)

def ask_llm(system_prompt,user_prompt):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role":"system",
                "content":system_prompt
            },
            {
                "role":"user",
                "content":user_prompt
            }
        ]
    )

    return response.choices[0].message.content