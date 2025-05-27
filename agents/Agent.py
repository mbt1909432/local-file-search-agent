from typing import List, Optional, Dict, Callable, AnyStr, Any
import json_repair
from generative_model.model import  Generative_Model
from agents.Prompt_Base import PromptTemplate
from py_model import  Message




class Agent:

    def __init__(self, agent_name: str, prompts_template: PromptTemplate,model="deepseek/deepseek-chat"):

        self._agent_name = agent_name
        self.model = Generative_Model(model)#一个agent持有一种模型，不可替换，generative model本身无状态可以换
        self.prompts_template = prompts_template#system prompt
        self._messages:Optional[List[Message]]=None

    def refresh_system(self,**kwargs):
        """若系统记忆需要更新则调用"""
        if self._messages is None:
            self._messages = [Message(role="system", content=self.prompts_template.get_format_system_prompt(**kwargs))]
        else:
            self._messages[0]=Message(role="system", content=self.prompts_template.get_format_system_prompt(**kwargs))

    async def response_with_memory(
        self,
        query,
        **kwargs#system 参数
    ):
        """有list_base 记忆的回复，kwargs为系统所需参数"""

        self.refresh_system(**kwargs)

        if kwargs:
            self.refresh_system(**kwargs)

        self._messages.append(Message(role="user",content=query))

        response = await self.model.generate(self._messages)

        self._messages.append(Message(role="assistant", content=response))

        return response

    async def response_without_memory(
        self,
        query,
        **kwargs
    ):
        """无list_based记忆的回复，kwargs为系统所需参数"""

        self.refresh_system(**kwargs)

        messages= [Message(role="system", content=self.prompts_template.get_format_system_prompt(**kwargs)),
                   Message(role="user", content=query)]
        response = await self.model.generate(messages)

        return response



async def main():
    from agents.prompts.chat import ChatPrompt
    new_agent=Agent("Lab_Agent",ChatPrompt())
    run=await new_agent.response_with_memory("你好，我叫ciro",**{"name":"小狗"})
    print(run)
    run = await new_agent.response_with_memory("我叫什么", **{"name": "小狗"})
    print(run)



if __name__=="__main__":

    import asyncio
    asyncio.run(main())



