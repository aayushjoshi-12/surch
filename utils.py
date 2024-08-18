import os
import sqlite3
import json


def retrieve_history():
    if not os.path.exists("memory.db"):
        print("No previous history found.")
        return None

    conn = sqlite3.connect("memory.db")
    cur = conn.cursor()

    cur.execute("SELECT session_id, message FROM message_store WHERE id IN (SELECT MIN(id) FROM message_store GROUP BY session_id);")
    outputs = cur.fetchall()
    for output in outputs:
        session_id = output[0]
        message = output[1]
        message = json.loads(message)
        question = message["data"]["content"]
        print(f"{session_id}: {question}")
    
    sid = input("Which chat you want to access, input it's session_id")
    cur.execute(f"SELECT message FROM message_store WHERE session_id = \"{sid}\"")
    messages = cur.fetchall()

    for message in messages:
        msg = json.loads(message[0])
        if msg["type"] == "human":
            print(f"You: {msg["data"]["content"]}")
        else:
            print(f"{msg["data"]["content"]}")

    
    cur.close()
    conn.close()

