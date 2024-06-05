import asyncio
import logging
import websockets

from ocpp.v201 import call
from ocpp.v201 import ChargePoint as cp
from ocpp.v201.enums import RegistrationStatusType, ReportBaseType

# Setting up logging to display information level messages.
logging.basicConfig(level=logging.INFO)

# Define a ChargePoint class inheriting from the OCPP 2.0.1 ChargePoint class.
class ChargePoint(cp):

    # Asynchronous method to send a BootNotification message to the server.
    async def send_boot_notification(self):
        # Create a BootNotification request with the charging station's model and vendor name.
        request = call.BootNotification(
            charging_station={
                'model': 'Wallbox XYZ',
                'vendor_name': 'anewone'
            },
            reason="PowerUp"
        )
        # Send the BootNotification request and wait for a response.
        response = await self.call(request)

        # Check the response status and log whether the connection was successful.
        if response.status == RegistrationStatusType.accepted:
            logging.info("Connected to central system.")
        else:
            logging.error("Failed to connect to central system.")

    # Asynchronous method to send a GetBaseReport message to the server.
    async def send_get_base_report(self):
        # Create a GetBaseReport request with a request ID and report base type.
        request = call.GetBaseReport(
            request_id=12345,
            report_base=ReportBaseType.configuration_inventory
        )
        # Send the GetBaseReport request and wait for a response.
        response = await self.call(request)

        # Log the response received from the server.
        logging.info(f"GetBaseReport response: {response}")

# Main asynchronous function to establish a WebSocket connection and send messages.
async def main():
    async with websockets.connect(
            'ws://localhost:9000/CP_1',  # URL of the WebSocket server.
            subprotocols=['ocpp2.0.1']   # Specify the OCPP 2.0.1 subprotocol.
    ) as ws:
        # Create a ChargePoint instance with an ID and the WebSocket connection.
        cp = ChargePoint('CP_1', ws)

        # Use asyncio.gather to run multiple coroutines concurrently.
        await asyncio.gather(
            cp.start(),  # Start listening for incoming messages.
            cp.send_boot_notification(),  # Send a BootNotification message.
            cp.send_get_base_report()  # Send a GetBaseReport message.
        )

# Entry point of the script.
if __name__ == '__main__':
    # Run the main function to start the client.
    asyncio.run(main())
