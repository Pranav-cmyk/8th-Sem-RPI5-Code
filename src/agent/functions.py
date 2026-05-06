import os

import requests
from dotenv import load_dotenv
from google.genai import Client, types
from livekit.agents import Agent, RunContext, function_tool
from prompts import instructions

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=instructions)
        self.client = Client(api_key=os.getenv("GOOGLE_API_KEY"))

    async def getLatestBase64Frame(self):
        uri = "http://10.24.218.177:8000/frame"
        print("Sending request to", uri)

        response = requests.get(uri)
        return (response.json()).get("image")

    @function_tool
    async def viewLatestFrame(self, context: RunContext):
        """

        views the latest frame from the camera. Use this to get a visual representation of the camera's current frame
        whenever the user asks what the camera is seeing.

        """
        image_base64 = await self.getLatestBase64Frame()

        print("Received image_base64, Sending to model...")
        image = types.Part.from_bytes(data=image_base64, mime_type="image/jpg")
        response = await self.client.aio.models.generate_content(
            model="gemini-3-flash-preview",
            contents=["What is this image? Provide a brief description.", image],
        )
        print(response.text)
        return response.text
