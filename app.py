import streamlit as st
from transformers import pipeline

# Initialize the text generation pipeline with a smaller model
generator = pipeline('text-generation', model='distilgpt2')

# Define the MARCO chatbot function
def marco_chatbot(prompt):
    response = generator(prompt, max_length=150, num_return_sequences=1, truncation=True, temperature=0.7)
    message = response[0]['generated_text'].strip()
    return message

# Initialize tasks dictionary
tasks = {}

# Function to add a task and generate a note
def add_task(task_name, task_details):
    # Create a prompt that guides the AI to provide a useful note
    prompt = f"Provide a step-by-step guide on how to approach the task: {task_details}. Include useful tips and relevant resources."
    note = marco_chatbot(prompt)
    tasks[task_name] = {'details': task_details, 'note': note, 'completed': False}
    return f"Task '{task_name}' added. Note: {note}"

# Function to list tasks
def list_tasks():
    if not tasks:
        return "No tasks available."
    task_list = "\n".join([f"{name}: {details['details']} - {'Completed' if details['completed'] else 'Pending'}\nNote: {details['note']}" for name, details in tasks.items()])
    return f"Your tasks:\n{task_list}"

# Function to complete a task
def complete_task(task_name):
    if task_name in tasks:
        tasks[task_name]['completed'] = True
        return f"Task '{task_name}' marked as completed."
    else:
        return f"Task '{task_name}' not found."

# Streamlit application interface
st.title("MARCO Chatbot")
st.write("Welcome to MARCO! Here are some commands you can use:")
st.write("""
1. 'add task' - Add a new task.
2. 'list tasks' - List all tasks.
3. 'complete task [task name]' - Mark a task as completed.
4. 'today's tasks' - Add today's tasks.
5. 'exit' - Exit the chatbot.
""")

# Input for user command
user_input = st.text_input("Enter a command:", "")

if user_input:
    if user_input.lower() == "list tasks":
        st.write(list_tasks())
    elif user_input.lower().startswith("add task"):
        task_name = st.text_input("Task Name")
        task_details = st.text_area("Task Details")
        if st.button("Add Task"):
            st.write(add_task(task_name, task_details))
    elif user_input.lower().startswith("complete task"):
        task_name = st.text_input("Task Name to Complete")
        if st.button("Complete Task"):
            st.write(complete_task(task_name))
    elif user_input.lower().startswith("today's tasks"):
        task_name = st.text_input("Task Name for Today")
        task_details = st.text_area("Task Details for Today")
        if st.button("Add Today's Task"):
            st.write(add_task(task_name, task_details))
    else:
        st.write(marco_chatbot(user_input))
