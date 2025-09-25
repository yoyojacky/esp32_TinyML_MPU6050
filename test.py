from openai import OpenAI


question = input("请输入问题: ")

client = OpenAI(
    base_url="http://localhost:11434/v1",  # 本地 Ollama API
    api_key="ollama"                       # 随便填个 key
)

response = client.chat.completions.create(
    model="deepseek-R1:8b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question}
    ]
)
print(response.choices[0].message.content)
