import requests

# URL of your running server
url = "http://localhost:8000"

# The prompt you want to test
data = {"prompt": "Hello, can you summarize AI in one setntence? Explain like a russian hacker. and use # to start every word."}

# Send POST request to generate response
response = requests.post(f"{url}/v1/completions", json=data)

# Print the model output
print(response.json())
