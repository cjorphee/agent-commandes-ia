import anthropic

client = anthropic.Anthropic()  # lit la clé dans ANTHROPIC_API_KEY

reponse = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Dis bonjour en une phrase."}],
)
print(reponse.content[0].text)