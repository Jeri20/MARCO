import streamlit as st
from transformers import pipeline
import requests

# Initialize the text generation pipeline
generator = pipeline('text-generation', model='gpt2')

# Define the MARCO chatbot function
def marco_chatbot(prompt):
    response = generator(prompt, max_length=150, num_return_sequences=1, truncation=True, temperature=0.7)
    message = response[0]['generated_text'].strip()
    return message

# Initialize tasks dictionary
tasks = {}

# Function to add a task
def add_task(task_name, task_details):
    tasks[task_name] = {'details': task_details, 'completed': False}
    return f"Task '{task_name}' added."

# Function to list tasks
def list_tasks():
    if not tasks:
        return "No tasks available."
    task_list = "\n".join([f"{name}: {details['details']} - {'Completed' if details['completed'] else 'Pending'}" for name, details in tasks.items()])
    return f"Your tasks:\n{task_list}"

# Function to complete a task
def complete_task(task_name):
    if task_name in tasks:
        tasks[task_name]['completed'] = True
        return f"Task '{task_name}' marked as completed."
    else:
        return f"Task '{task_name}' not found."

# Function to search the internet
def internet_search(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'AbstractText' in data and data['AbstractText']:
            return data['AbstractText']
        elif 'RelatedTopics' in data and data['RelatedTopics']:
            return data['RelatedTopics'][0]['Text']
        else:
            return "Sorry, I couldn't find any information on that."
    else:
        return "Error: Unable to perform search."

# Function to handle user requests
def handle_request(user_input):
    if user_input.lower().startswith("add task"):
        task_name = st.text_input("Please enter the task name:")
        task_details = st.text_area("Please enter the task details:")
        if st.button("Add Task"):
            return add_task(task_name, task_details)
    elif user_input.lower() == "list tasks":
        return list_tasks()
    elif user_input.lower().startswith("complete task"):
        task_name = user_input[len("complete task "):]
        return complete_task(task_name)
    elif user_input.lower() == "today's tasks":
        task_name = st.text_input("Please enter the task name:")
        task_details = st.text_area("Please enter the task details:")
        if st.button("Add Today's Task"):
            return add_task(task_name, task_details)
    elif user_input.lower().startswith("search"):
        query = user_input[len("search "):]
        return internet_search(query)
    else:
        return marco_chatbot(user_input)

# Streamlit application interface
st.title("MARCO Chatbot")
st.write("Welcome to MARCO! Here are some commands you can use:")
st.write("""
1. 'add task' - Add a new task.
2. 'list tasks' - List all tasks.
3. 'complete task [task name]' - Mark a task as completed.
4. 'today's tasks' - Add today's tasks.
5. 'search [query]' - Search the internet for information.
6. 'exit' - Exit the chatbot.
""")

user_input = st.text_input("You:", "")
if user_input:
    response = handle_request(user_input)
    st.write(f"MARCO: {response}")
