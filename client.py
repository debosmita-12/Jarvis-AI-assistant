from openai import OpenAI

client = OpenAI(
  api_key="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"  # Replace with your real key safely
)

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "What is coding?"}
  ]
)

print(completion.choices[0].message.content)