from discordrp import Presence
import time

client_id = "1270540390088441928"  # Replace this with your own client id

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
