import tkinter as tk
import socket
from tcp_by_size import send_with_size, recv_by_size

# Create a socket
cli_s = socket.socket()
cli_s.connect(("127.0.0.1", 33445))

# List of commands and their corresponding inputs
commands = [
    {"label": "Time manager", "action": "UPDUSR", "inputs": ["id", "name", "password", "email", "address", "phone"]},
    {"label": "Set timer for a break", "action": "INSUSR", "inputs": ["name", "password", "email", "address", "phone"]},
    {"label": "Website blocking", "action": "DLTUSR", "inputs": ["customer_id"]},
    {"label": "Send a message to your kid", "action": "CUSLST", "inputs": []},
    {"label": "Exit", "action": "RULIVE", "inputs": []}
]

# Function to execute a command
def execute_command(command_data, input_entries, result_label):
    action = command_data["action"]
    inputs = input_entries
    data = action

    # Construct the data string with input values
    for input_entry in inputs:
        data += "|" + input_entry.get()

    # Send the command data to the server
    send_with_size(cli_s, data.encode())
    response = recv_by_size(cli_s).decode()
    response = response[7:]  # Get just the output
    result_label.config(text="Output:\n" + response)

# Function to create a window for a specific command
def create_command_window(command_data):
    command_window = tk.Toplevel(root)
    command_window.title(command_data["label"])

    input_entries = []
    for input_label in command_data["inputs"]:
        tk.Label(command_window, text=input_label + ":").pack()
        entry = tk.Entry(command_window)
        entry.pack()
        input_entries.append(entry)

    result_label = tk.Label(command_window, text="Output:")
    result_label.pack()

    submit_button = tk.Button(command_window, text="Submit",
                              command=lambda: execute_command(command_data, input_entries, result_label))
    submit_button.pack()

# Function to create a window for creating a new user
def create_user_window():
    user_window = tk.Toplevel(root)
    user_window.title("Create User")

    input_entries = []
    for input_label in commands[1]["inputs"]:  # Use inputs from "Create new customer" command
        tk.Label(user_window, text=input_label + ":").pack()
        entry = tk.Entry(user_window)
        entry.pack()
        input_entries.append(entry)

    result_label = tk.Label(user_window, text="Output:")
    result_label.pack()

    submit_button = tk.Button(user_window, text="Create", command=lambda: create_new_user(input_entries, result_label))
    submit_button.pack()

# Function to create a new user
def create_new_user(input_entries, result_label):
    user_name = input_entries[0].get()

    # Check if user_name contains "--"
    if "--" in user_name:
        result_label.config(text="Invalid name, names cannot contain '--'")
        return

    # If user_name is valid, proceed to execute the command
    execute_command(commands[1], input_entries, result_label)

# Function to handle the login process
def handle_login():
    name = name_entry.get()
    password = password_entry.get()
    user_id = id_entry.get()
    if "--" in name:
        response = "no"
    else:
        # Send login data to the server for validation
        login_data = f"LOGINN|{name}|{password}|{user_id}"
        send_with_size(cli_s, login_data.encode())

        # Receive the server's response
        response = recv_by_size(cli_s).decode()
        response = response[8:]

    if response == "yes":
        # Close the login window and create the child selection window
        login_window.destroy()
        create_child_selection_window()
    else:
        # Display an error message for invalid login
        login_error_label.config(text="Invalid login, please try again")

# Function to create a window for selecting a child
def create_child_selection_window():
    global root
    root = tk.Tk()
    root.title("Select Child")

    selected_child = tk.StringVar()
    selected_child.set("")  # Default value

    # Sample list of children
    children = ["Child1", "Child2", "Child3"]

    # Create buttons for each child
    for child in children:
        tk.Radiobutton(root, text=child, variable=selected_child, value=child).pack()

    # Button to confirm selection
    confirm_button = tk.Button(root, text="Confirm", command=lambda: open_main_window(selected_child.get()))
    confirm_button.pack()

    root.mainloop()

# Function to open the main command window after selecting a child
def open_main_window(selected_child_name):
    root.destroy()  # Close the child selection window

    # Create the main command window
    create_main_window(selected_child_name)

# Function to create the main command window
def create_main_window(selected_child_name):
    global root
    root = tk.Tk()
    root.title("Commands")

    # Create buttons for each command
    for command_data in commands:
        tk.Button(root, text=command_data["label"], command=lambda cmd=command_data: create_command_window(cmd)).pack()

    # You can use the selected_child_name as needed in your application
    print("Selected Child:", selected_child_name)

    root.mainloop()

# Create the login window
login_window = tk.Tk()
login_window.title("Login")

# Name entry
tk.Label(login_window, text="Name:").pack()
name_entry = tk.Entry(login_window)
name_entry.pack()

# Password entry
tk.Label(login_window, text="Password:").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

# ID entry
tk.Label(login_window, text="ID:").pack()
id_entry = tk.Entry(login_window)
id_entry.pack()

# Login button
login_button = tk.Button(login_window, text="Login", command=handle_login)
login_button.pack()

# Create User button
create_user_button = tk.Button(login_window, text="Create User", command=create_user_window)
create_user_button.pack()

# Login error label
login_error_label = tk.Label(login_window, text="")
login_error_label.pack()

login_window.mainloop()