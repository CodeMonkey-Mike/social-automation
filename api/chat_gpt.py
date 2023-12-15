import json
import aiohttp
from .config import BaseConfig

class ChatGPTAPI:
    def __init__(self):
        self.BASE_URL = "https://api.openai.com/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BaseConfig.CHAT_GPT_KEY}"
        }

    async def fetch_data(self, url, **kwargs):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(f"{self.BASE_URL}{url}", **kwargs) as response:
                return await response.text()
    async def post_data(self, url, **kwargs):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url=f"{self.BASE_URL}{url}", **kwargs) as response:
                return await response.text()

    def get_prompt(self, prompt):
        json_object = {
          "paragraphs": [
            {
              "text": "value",
              "art": "value"
            }
          ]
        }
        return f"""can you write a summary of the following article:\n\n{prompt}\n\n> generate the response in a JSON object\n> summarize this in 4 paragraphs\n> make the final paragraph commentary, as if a commentary is giving his opinion about the summary of the article that he just read out loud. Don't begin the text with, 'After reading this,' just begin the commentary.\n> give me an array of paragraphs, with each element having an attribute called 'text' with the paragraph as the value\n> give me an additional attribute called time, that will contain the total number of seconds that it would take for a person to read it out loud at a rate of 160 words per minute\n> save this to context:\nthe appropriate response should be in the following format: {json_object}\n> Do not include 'commentary'\n> Always use double quotes for JSON\n> Do not deviate from this format\n> for each paragraph, make a description that I could use as a prompt to generate AI Art.  The name of this attribute should be art, and value should be a string\n> Respond with words that would be used when spoken out loud, not by using symbols. For example, an '=' should be changed to 'equals'"""
    
    async def get_summary(self, prompt):
        try:
          if prompt and len(prompt) > 0:
              prompt_temp = self.get_prompt(prompt)
              payload = {
                  "model": "gpt-3.5-turbo",
                  "messages": [
                      {
                          "role": "user",
                          "content": prompt_temp
                      }
                  ]
              }
              response = await self.post_data(url="/chat/completions", data=json.dumps(payload))
              data = json.loads(response)
              org_summary = data["choices"][0]["message"]["content"]
              org_summary_dict = json.loads(org_summary)
              paragraphs = org_summary_dict.get("paragraphs")
              merged_summary = " ".join(paragraph["text"] for paragraph in paragraphs)
              cleanup_summary = merged_summary.replace('\"', "'")
              return paragraphs, cleanup_summary
          else:
              return [], ""
        except Exception as e:
            # Handle the exception here (e.g., log the error message)
            print(f"An error occurred: {str(e)}")
            return [], ""




