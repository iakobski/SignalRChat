import sys
import logging
from signalrcore.hub_connection_builder import HubConnectionBuilder

def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value

handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)
hub_connection = HubConnectionBuilder()\
    .with_url("https://localhost:7026/chatHub", options={"verify_ssl": False}) \
    .configure_logging(logging.DEBUG, socket_trace=True, handler=handler) \
    .with_automatic_reconnect({
            "type": "interval",
            "keep_alive_interval": 10,
            "intervals": [1, 3, 5, 6, 7, 87, 3]
        }).build()

hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages"))
hub_connection.on_close(lambda: print("connection closed"))

hub_connection.on("ReceiveMessage", print)
hub_connection.on("NeedMoreData", lambda data: provideMoreData(data))
hub_connection.on("FinishedCalculation", lambda data: print(f"Finished calculation, received {data}"))

def provideMoreData(input):
    print("providing more data")
    hub_connection.send("ContinueCalculation", ["new data"])
    print(input)
    

hub_connection.start()
message = None

username='jake'
while message != "exit()":
    message = input(">> ")
    if message is not None and message != "" and message != "exit()":
        hub_connection.send("StartCalculation", [username, message])

hub_connection.stop()
sys.exit(0)
