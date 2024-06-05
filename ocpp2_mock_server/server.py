import asyncio
import logging
import websockets
from datetime import datetime

from ocpp.routing import on
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result
from ocpp.v201.enums import RegistrationStatusType, GenericDeviceModelStatusType

logging.basicConfig(level=logging.DEBUG)

class ChargePoint(cp):
    @on('BootNotification')
    async def on_boot_notification(self, charging_station, reason, **kwargs):
        logging.info("Received BootNotification")
        return call_result.BootNotification(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatusType.accepted
        )

    @on('GetBaseReport')
    async def on_get_base_report(self, request_id, report_base, **kwargs):
        try:
            logging.info(f"Received GetBaseReport request with RequestId: {request_id} and ReportBase: {report_base}")

            # Mock response for demonstration purposes
            response = call_result.GetBaseReport(
                status=GenericDeviceModelStatusType.accepted
            )

            logging.info(f"Sending GetBaseReport response: {response}")
            return response
        except Exception as e:
            logging.error(f"Error handling GetBaseReport request: {e}", exc_info=True)
            return call_result.GetBaseReport(
                status=GenericDeviceModelStatusType.rejected
            )

async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint instance and start listening for messages. """
    try:
        requested_protocols = websocket.request_headers['Sec-WebSocket-Protocol']
    except KeyError:
        logging.info("Client hasn't requested any Subprotocol. Closing Connection")
        return await websocket.close()

    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        logging.warning('Protocols Mismatched | Expected Subprotocols: %s,'
                        ' but client supports %s | Closing connection',
                        websocket.available_subprotocols,
                        requested_protocols)
        return await websocket.close()

    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)

    await cp.start()

async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp2.0.1']
    )
    logging.info("WebSocket Server Started")
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
