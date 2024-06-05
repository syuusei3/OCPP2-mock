import asyncio
import logging
import websockets

from ocpp.v201 import call
from ocpp.v201 import ChargePoint as cp
from ocpp.v201.enums import RegistrationStatusType, ReportBaseType

logging.basicConfig(level=logging.INFO)

class ChargePoint(cp):

    async def send_boot_notification(self):
        request = call.BootNotification(
            charging_station={
                'model': 'Wallbox XYZ',
                'vendor_name': 'anewone'
            },
            reason="PowerUp"
        )
        response = await self.call(request)

        if response.status == RegistrationStatusType.accepted:
            logging.info("Connected to central system.")
        else:
            logging.error("Failed to connect to central system.")

    async def send_get_base_report(self):
        request = call.GetBaseReport(
            request_id=12345,
            report_base=ReportBaseType.configuration_inventory
        )
        response = await self.call(request)

        logging.info(f"GetBaseReport response: {response}")

async def main():
    async with websockets.connect(
            'ws://localhost:9000/CP_1',
            subprotocols=['ocpp2.0.1']
    ) as ws:
        cp = ChargePoint('CP_1', ws)

        await asyncio.gather(
            cp.start(),
            cp.send_boot_notification(),
            cp.send_get_base_report()
        )

if __name__ == '__main__':
    asyncio.run(main())
