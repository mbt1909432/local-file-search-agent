from typing import List

from openai import AsyncOpenAI

from py_model import Message



class Generative_Model:

    def __init__(self,model:str):

        self._client = AsyncOpenAI(
            api_key="YOUR API KEY",
            base_url="ENDPOINT",
        )
        self.model = model

    async def generate(
        self,
        messages:List[Message],
        model=None
    ):

        response = await self._client.chat.completions.create(
            model=self.model if model is None else model,  # 使用指定的模型
            messages=[ message.model_dump() for message in messages],
        )

        return response.choices[0].message.content


