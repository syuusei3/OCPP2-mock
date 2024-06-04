import asyncio
import websockets
import json

async def send_request():
    uri = "ws://localhost:9000/CP1"
    async with websockets.connect(uri, subprotocols=['ocpp2.0.1']) as websocket:
        request = [
            2,     # The first item is MessageTypeId (Call = 2)
            "12345", # The second item is a unique id
            "BootNotification", # The third item is the Action
            {   # The fourth element is a dictionary (Payload) which contains 'chargingStation' and 'reason'
                "chargingStation": {
                    "model": "demo", 
                    "vendorName": "demo" 
                },
                "reason": "PowerUp"
            }       
        ]
        await websocket.send(json.dumps(request))
        response = await websocket.recv()
        print(response)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_request())