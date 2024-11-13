import json
import os
import requests
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import List, Any, Dict

@dataclass
class StinkinessResponse:
    rating: float
    factors: List[str]
    poem: str

@dataclass
class ClientResponse:
    choices: List[Dict[str, Any]]
    created: int
    id: str
    model: str
    object: str
    usage: Dict[str, int]
    message: StinkinessResponse


# Payload for the request
payload = {
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "I am an API that returns a structured response indicating whether Denver, CO smells like Greeley, CO. I search for these factors\n\nHere are three key factors that contribute to when and how intensely this odor reaches Denver:\n\n    Wind Direction: Northeasterly winds carry odors from Greeley's cattle and feedlot operations directly toward Denver. When these winds shift toward this direction, it often means Denver is downwind of Greeley's agricultural areas.\n\n    Precipitation Patterns: Before snowstorms, upslope conditions and colder temperatures trap odors closer to the ground, making the smell more noticeable as it is pushed up against the mountains around Denver. This setup frequently occurs in the winter months.\n\n    Air Pressure and Humidity: Low-pressure systems and higher humidity levels can also intensify odors. Low-pressure systems enhance airflow from Greeley, and the moisture in the air holds and amplifies the smell, making it stronger in Denver when these conditions align.\n\nI provide a response as a JSON string with this structure:\n{\n  \"rating\": // rating,\n   \"factors\": [\n    // factor 1\n    // factor 2\n    // factor 3\n  ]\n}\nAn example response is\n{\n  \"rating\": 0.5,\n  \"factors\": [\n    \"Winds in Denver are coming from the west.\",\n    \"The air is relatively dry today.\",\n    \"The temperature is mild.\"\n  ],   \"poem\": \"Roses are red\nViolets are mealy\nToday Denver smells\nJust like Greeley\"\n}\nThe \"rating\" value will always be a number between 0 and 1, with 0 being no smell and 1 being the strongest smell Denver has ever experienced. The \"factors\" value will always be a list of strings, each of which explains how the current conditions factor into the rating.\n The \"poem\" value will always be a short poem describing the stinkiness level.\nIf prompted with a date and time, the values for \"rating\" and \"factors\" will represent the conditions on that date and at that time. If I am prompted without a date and time, the values for \"rating\" and \"factors\" will represent the conditions for the current date and time."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "\n"
        }
      ]
    }
  ],
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 800
}

default_poem = "In the air, a mystery lingers,\nYet truth eludes our searching fingers.\nWith scents that twist and twirl along,\nWe pause and sigh, for something went wrong."


class StinkClient:
    def __init__(self, api_key, endpoint):
        self._api_key = api_key
        self._endpoint = endpoint

    @property
    def default_poem(self):
        return default_poem

    @property
    def error_response(self):
        return StinkinessResponse(
            rating=0,
            factors=[],
            poem=default_poem
        )

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
             "api-key": self._api_key,
        }

    def request_stinkiness(self) -> StinkinessResponse:
        try:
            response = requests.post(self._endpoint, headers=self.headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            client_response = self._parse_client_response(response.json())
            return client_response.message
        except requests.RequestException as e:
            raise Exception(f"Failed to make the request. Error: {e}")

    def _parse_stinkiness_response(self, response_json):
      return StinkinessResponse(
          rating=1 - response_json['rating'],
          factors=response_json['factors'],
          poem=response_json['poem']
      )

    def _parse_client_response(self, response_json: dict) -> ClientResponse:
      # Extract the message content and parse it as a StinkinessResponse
      content_json = response_json['choices'][0]['message']['content']
      print("Response content:" + content_json)
      message_content = json.loads(content_json)
      message = self._parse_stinkiness_response(message_content)
    
      return ClientResponse(  
          choices=response_json.get('choices', []),
          created=response_json.get('created', 0),
          id=response_json.get('id', ''),
          model=response_json.get('model', ''),
          object=response_json.get('object', ''),
          usage=response_json.get('usage', {}),
          message=message
      )

def initialize_client() -> StinkClient:
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    ENDPOINT = os.getenv("ENDPOINT")
    return StinkClient(API_KEY, ENDPOINT)
