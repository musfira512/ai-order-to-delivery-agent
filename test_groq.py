import os
from groq import Groq

client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Explain AI business process automation in one simple sentence."
        }
    ]
)

print(response.choices[0].message.content)
