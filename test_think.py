from ollama import chat

response = chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "user",
            "content": "What skills are required for a Python developer? Give only the final answer."
        }
    ],
    think=True,
    options={
        "num_predict": 1000,
        "temperature": 0
    }
)

print("CONTENT:")
print(response.message.content)

print("\nTHINKING:")
print(response.message.thinking)

print("\nDONE REASON:")
print(response.done_reason)