import asyncio
import logging
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result
from ocpp.routing import on
import websockets

logging.basicConfig(level=logging.INFO)

class ChargePoint(cp):
    @on('BootNotification')
    async def on_boot_notification(self, charging_station, reason, **kwargs):
        return call_result.BootNotificationPayload(
            current_time='2022-01-01T00:00:00Z',
            interval=10,
            status='Accepted'
        )

    @on('Authorize')
    async def on_authorize(self, id_token, **kwargs):
        return call_result.AuthorizePayload(
            id_token_info={
                'status': 'Accepted'
            }
        )

    @on('StartTransaction')
    async def on_start_transaction(self, remote_start_id, **kwargs):
        return call_result.StartTransactionPayload(
            transaction_id='123',
            id_token_info={
                'status': 'Accepted'
            }
        )

    @on('StopTransaction')
    async def on_stop_transaction(self, transaction_id, **kwargs):
        return call_result.StopTransactionPayload(
            id_token_info={
                'status': 'Accepted'
            }
        )

    @on('Heartbeat')
    async def on_heartbeat(self, **kwargs):
        return call_result.HeartbeatPayload(
            current_time='2022-01-01T00:00:00Z'
        )

    @on('GetBaseReport')  # Added handler for GetBaseReport
    async def on_get_base_report(self, request_id, report_base, **kwargs):
        # As GetBaseReport is not a standard OCPP method,
        # I'll return a simple confirmation message for simplicity.
        print(f"Received GetBaseReport: {request_id} - {report_base}")
        return {"status": "Received"}

async def on_connect(websocket, path):
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)
    await cp.start()

if __name__ == '__main__':
    server = websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp2.0.1']
    )
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()