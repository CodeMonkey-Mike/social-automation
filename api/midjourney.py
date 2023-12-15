# import requests
import json
# from .prompt import get_prompt 

import asyncio
import aiohttp

from .config import BaseConfig

class MidjourneyAPI:
    def __init__(self):
        self.BASE_URL = "https://api.mymidjourney.ai/api/v1/midjourney"
        self.headers = {"Authorization": f"Bearer {BaseConfig.MJ_KEY}"}

    async def fetch_data(self, url, **kwargs):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url, **kwargs) as response:
                return await response.text()
    async def post_data(self, url, **kwargs):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, **kwargs) as response:
                return await response.text()

    async def generate_image(self, prompt):
        # Replace these with your API endpoints
        api_url1 = f"{self.BASE_URL}/imagine"
        api_url2 = f"{self.BASE_URL}/message"
        api_url3 = f"{self.BASE_URL}/button"

        # Make the first API request
        payload1 = {
            "prompt": prompt
        }
        if len(prompt) > 0:
          print('start_prompt=====', prompt)
          data1 = await self.post_data(api_url1, data=payload1)
          print(f'Response from API 1=test1: {data1}')
          # Parse the JSON string into a Python dictionary
          data1_dict = json.loads(data1)
          print(f'Response from API 1=test2: {data1_dict.get("messageId")}')

          # Check the 'process' field in data2 until it reaches 100%
          async def check_process():
              # Make the second API request after the first one is completed
              message_id = data1_dict.get("messageId")
              print(f'Response from API 2-message_id: {message_id}')
              
              while True:
                  data2 = await self.fetch_data(f"{api_url2}/{message_id}")
                  data2_dict = json.loads(data2)
                  print(f'Response from API 2: {data2_dict}')
                  # Replace this with the actual field name in your data2 response
                  progress = data2_dict.get('progress', 0)
                  print(f'Process: {progress}%')

                  if progress and progress >= 100:
                      break

                  # Wait for a certain interval (e.g., 5 seconds) before checking again
                  await asyncio.sleep(10)

          check_process_task = asyncio.create_task(check_process())
          # Wait for the check_process task to complete
          await check_process_task

          # Make the third API request after the second one is completed
          print(f'Response from API 3-message-id: {data1_dict.get("messageId")}')
          payload3 = {
            "messageId": data1_dict.get("messageId"),
            "button": "U2"
          }
          data3 = await self.post_data(api_url3, data=payload3)
          data3_dict = json.loads(data3)
          print(f'Response from API 3: {data3}')

          # get final image
          # message_upscale_id = data3_dict.get("messageId")
          # data4 = await self.fetch_data(f"{api_url2}/{message_upscale_id}")
          # print(f'Response from API 4: {data4}')
          # data4_dict = json.loads(data4)
          # image_uri = data4_dict.get('uri')
          final_image = ''
          # Check the 'process' field in data2 until it reaches 100%
          async def check_process_task_get_single_image():
              message_upscale_id = data3_dict.get("messageId")
              print(f'Response from API 4-message_upscale_id: {message_upscale_id}')
              nonlocal final_image
              while True:
                  data4 = await self.fetch_data(f"{api_url2}/{message_upscale_id}")
                  data4_dict = json.loads(data4)
                  print(f'Response from API 4: {data4_dict}')
                  # Replace this with the actual field name in your data2 response
                  progress = data4_dict.get('progress', 0)
                  print(f'Process-4: {progress}%')

                  if progress and progress >= 100:
                      final_image = data4_dict.get('uri')
                      break

                  # Wait for a certain interval (e.g., 5 seconds) before checking again
                  await asyncio.sleep(20)

          get_single_image_task = asyncio.create_task(check_process_task_get_single_image())
          # Wait for the check_process task to complete
          await get_single_image_task

          return final_image
        else:
            None