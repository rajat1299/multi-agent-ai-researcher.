import streamlit as st
from phi.assistant import Assistant
from phi.tools.hackernews import HackerNews
from phi.llm.ollama import Ollama

# Initialize the Ollama client and ensure the model is pulled
def initialize_model():
    client = Ollama(model="llama3", max_tokens=1024)
    try:
        client.pull_model()  # Assuming there's a method to pull the model
    except AttributeError:
        # Handle the case where the pull_model method does not exist
        print("Ensure the model llama3 is available and pulled.")

initialize_model()


st.title("Multi-Agent AI Researcher using Llama-3")
st.caption("This app allows you to research top stories and users on HackerNews and write blogs, reports, and social posts.")

story_researcher = Assistant(
    name="HackerNews Story Researcher",
    role="Researches HackerNews stories and users.",
    tools=[HackerNews()],
    llm=Ollama(model="llama3", max_tokens=1024)
)

user_researcher = Assistant(
    name="HackerNews User Researcher",
    role="Reads articles from URLs.",
    tools=[HackerNews()],
    llm=Ollama(model="llama3", max_tokens=1024)
)

hn_assistant = Assistant(
    name="HackerNews Team",
    team=[story_researcher, user_researcher],
    llm=Ollama(model="llama3", max_tokens=1024)
)

query = st.text_input("Enter your report query")

if query:
    response = hn_assistant.run(query, stream=False)
    st.write(response)
