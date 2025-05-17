import logging
import requests
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class PostRequester:
    url: str
    token: str
    payloads: List[Dict]
    logger: logging.Logger

    def send_post_requests(self):
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        for payload in self.payloads:
            try:
                response = requests.post(self.url, json=payload, headers=headers)

                if response.status_code != 200:
                    self.logger.error(f"[ERROR]: HTTP {response.status_code} - Failed to send data.")
                    continue

                self._handle_response(response.json(), payload)

            except Exception:
                self.logger.error(f"[EXCEPTION]: Error sending payload: {payload}")

    def _handle_response(self, result: Dict, payload: Dict):
        results = result.get("data", {}).get("results", [])

        if any("id_plant" in item for item in results):
            self.logger.info(f"Plant information saved: {payload.get('ID_PLANT')}")
        else:
            self.logger.error(f"[ERROR]: Plant information not saved (missing 'id_plant'): {payload.get('ID_PLANT')}")

        for item in results:
            if item.get("status") == "error" and "id_device" in item:
                self.logger.error(f"[ERROR]: Device {item['id_device']} - {item.get('message', 'Unknown error')}")
