from state import State

def send_email_node(state: State):
    print("Sending email...")
    # mock sending logic
    with open("sent_email.txt", "w") as f:
        f.write(f"To: {state.email_to}\nSubject: {state.email_subject}\n\n{state.email_body}")

    print(f"Email sent to {state.email_to} with subject '{state.email_subject}'.")
    print(f"\n\nemail receieved at sent_email.txt")
    return state