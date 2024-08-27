import time

from discordrp import Presence

client_id = "1270540390088441928"  # Replace this with your own client id

try:
    with Presence(client_id) as presence:
        print("Connected")
        presence.set(
            {
                "state": "Editing Image",
                "details": "Test",
                "timestamps": {"start": int(time.time())},
            }
        )
        print("Presence updated")
except Exception as e:
    print("Discord not running")
