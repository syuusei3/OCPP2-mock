import asyncio
from ocpp.v201 import call
from ocpp.v201 import call_result
from ocpp.v201 import ChargePoint as cp
import websockets
from ocpp.v201.enums import RegistrationStatusType

async def on_connected_charge_point(websocket, path):
    print(f"Connection established: {path}")
    charge_point = ChargePoint(path, websocket)
    await charge_point.start()

class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charging_station={
                'model': 'Wallbox XYZ',
                'vendor_name': 'anewone'
            },
            reason="PowerUp"
        )
        response = await self.call(request)

        if response.status == RegistrationStatusType.accepted:
            print("Connected to central system.")
    async def authorize(self):
        request = call.AuthorizePayload(id_tag="123")
        response = await self.call(request)
        if response.id_token_info["status"] == "Accepted":
            print("Authorized.")
    async def start_transaction(self, connector_id: int, id_tag: str):
        request = call.StartTransactionPayload(connector_id=connector_id, id_tag=id_tag)
        response = await self.call(request)
        return response.transaction_id
    async def stop_transaction(self, transaction_id: str, id_tag: str):
        request = call.StopTransactionPayload(
          transaction_id=transaction_id,
          id_tag=id_tag,
         )
        await self.call(request)
    async def send_heartbeat(self):
        request = call.HeartbeatPayload()
        await self.call(request)
    async def send_base_report(self, report):
        request = call.GetBaseReportPayload(request_id="1", report_base=report)
        await self.call(request)

async def main():
    async with websockets.connect("ws://localhost:9000/CP_1", subprotocols=['ocpp2.0.1']) as ws:
        charge_point = ChargePoint("CP_1", ws)
        
        asyncio.create_task(charge_point.start())
        asyncio.create_task(charge_point.send_boot_notification())
        asyncio.create_task(charge_point.authorize())
        asyncio.create_task(charge_point.start_transaction(1, "123"))
        asyncio.create_task(charge_point.stop_transaction("123", "123"))
        asyncio.create_task(charge_point.send_heartbeat())
        asyncio.create_task(charge_point.send_base_report("my_report"))

if __name__ == '__main__':
    asyncio.run(main())