import logging
import requests
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class PostRequester:
    """
    PostRequester is responsible for sending multiple POST requests to a specified API endpoint
    with a given authorization token and list of payloads. It logs the success or failure of each request,
    and processes the response to provide feedback on plant and device registration status.

    Attributes:
        url (str): The API endpoint where POST requests will be sent.
        token (str): The bearer token used for authorization.
        payloads (List[Dict]): A list of dictionaries to be sent as JSON in each POST request.
        logger (logging.Logger): Logger instance used for logging results and errors.

    Methods:
        send_post_requests():
            Sends each payload in the payload list to the API using a POST request.
            Logs errors for failed requests and passes successful responses to be handled.

        _handle_response(result: Dict, payload: Dict):
            Parses the API response to check whether plant and device information was saved correctly.
            Logs messages based on the presence or absence of certain keys and values in the response.
    """

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
                    self.logger.error(f"[ERROR_MESSAGE]: HTTP {response} - Failed to send data.")

                    continue

                self._handle_response(response.json(), payload)

            except Exception as e:
                self.logger.error(f"[EXCEPTION]: Error sending payload: {e}")

    def _handle_response(self, result: Dict, payload: Dict):
        results = result.get("data", {}).get("results", [])

        if any("id_plant" in item for item in results):
            self.logger.info(f"Plant information saved: {payload.get('ID_PLANT')}")
        else:
            self.logger.error(f"[ERROR]: Plant information not saved (missing 'id_plant'): {payload.get('ID_PLANT')}")

        for item in results:
            if item.get("status") == "error" and "id_device" in item:
                self.logger.error(f"[ERROR]: Device {item['id_device']} - {item.get('message', 'Unknown error')}")
