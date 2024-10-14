from openai import OpenAI
client = OpenAI(api_key="",)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named siri skilled in general task like Alexa and Google cloud."},
        {
            "role": "user",
            "content": "What is coding."
        }
    ]
)

print(completion.choices[0].message.content)

