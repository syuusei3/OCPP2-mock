# OCPP2 Mock Client and Server

This project includes a mock Open Charge Point Protocol (OCPP) version 2.0.1 client and server implemented in Python.

## Prerequisites

This project requires Python 3.7+ and the following Python packages:

- `websockets`
- `ocpp`

You can install these packages using pip:
```
pip install websockets ocpp
```

## Running the Server

To start the server, run the `server.py` script:

```
python server.py
```

The server will start listening for connections on port 9000.

## Running the Client

To start the client, run the `client.py` script:
```
python client.py
```

The client will connect to the server via WebSocket on port 9000, send a `BootNotification` request to the server, and print the server's response.

## Overview of the Client and Server Scripts

### Client.py

The client script connects to the server via WebSocket and sends a `BootNotification` request. The request payload includes a `chargingStation` object (with `model` and `vendorName` properties) and a `reason` property. The client prints the server's response.

### Server.py

The server script waits for connections from clients. When a client connects, the server creates a new instance of the `ChargePoint` class. This class includes methods for handling various OCPP actions (`BootNotification`, `Authorize`, `StartTransaction`, `StopTransaction`, `Heartbeat`, and `GetBaseReport`), most of which return a dummy response. The `GetBaseReport` method prints the received request and returns a simple confirmation message.

The server script uses the websockets and ocpp libraries to facilitate the WebSocket and OCPP communication.

## Note

This project is intended for testing purposes. The server and client scripts do not implement full OCPP compliance and should not be used in production without further development.
