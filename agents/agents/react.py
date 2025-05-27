from agents.prompts.react import ReactPrompt
from tools.local_seach_tools import count_files, find_files
from tools.tools import NAME, tool,fire_skill,ice_skill
from config.config import RichLogger
from agents.Agent import Agent
from typing import List, Dict, Callable,  Any
import json_repair
from py_model import  Message



class ReactAgent(Agent):
    """react agent采取 但user query记忆 缩短上下文"""

    def __init__(self,model="deepseek/deepseek-chat"):

        super().__init__(agent_name="react",prompts_template=ReactPrompt(),model=model)
        self.max_iteration=5
        self.current_iteration=0
        self.tools:Dict[NAME,tool]={}
        self.history:List[Message]=[]


        """其他引入"""
        self.custom_logger = RichLogger(
            name=self._agent_name,
            log_dir=self._agent_name,
            console_level="DEBUG"
        ).get_logger()


    async def think(self,query):
        self.current_iteration+=1
        self.custom_logger.info(f"\n****************\niteration{self.current_iteration}\n********************")
        if self.current_iteration == self.max_iteration:
            self.set_history(step="think中到达最大次数",role="system",content="到达最大次数停止运行")
            return

        query_template=self.prompts_template.get_format_user_prompt(**{"query":query,"history":self.get_history(),"tools":str([ tool.get_tool_info() for tool in self.tools.values()])})
        self.custom_logger.info(f"\n\n******当前prompt模板*******\n\n{query_template}\n\n")
        response=await self.response_without_memory(query_template)
        self.set_history(step="think中根据用户响应生成的response",role="assistant",content=response)
        await self.decide(response,query)
        return response

    async def decide(self,response:str,query:str):
        """

        @param response: 用于下一步解析
        @param query: 传入query后续用于重新思考
        @return:
        """
        try:
            parsed_response = json_repair.loads(response.lower())#输出函数名全小写
            if type(parsed_response) is list:
                parsed_response=parsed_response[1]

            if parsed_response.get("action"):
                action=parsed_response["action"]
                try:
                    tool_name = action["name"].upper()
                    if NAME[tool_name]:  # 不存在会报错
                        self.set_history(step="decide中从enum调用可用工具",role="assistant", content=f"使用tool为:{NAME[tool_name]}")
                        await self.act(NAME[tool_name],query,action["input"])
                    else:
                        self.set_history(step="decide中发现功能不存在",role="assistant", content="功能不存在")
                        await self.think(query)
                except KeyError:
                    self.set_history(step="decide中发现功能不存在",role="assistant", content=f"⚠️ 警告：'{tool_name}' tool不存在，存入记忆重新思考")
                    await self.think(query)
            elif parsed_response.get("answer"):
                self.set_history(step="decide回答最后问题",role="assistant", content=parsed_response.get("answer"))

        except Exception as e:#额外报错，随着优化更新
            self.set_history(step="decide中额外报错",role="assistant", content="报错了,请重新尝试:"+str(e))
            await self.think(query)

    async def act(self,name:NAME,query:str,input:dict):
        """

        @param name: 工具名
        @param query: 用户query
        @param input: 函数调用参数
        @return:
        """
        exist_tool=self.tools.get(name)
        if exist_tool:
            observation=exist_tool.tool_use(**input)
            self.set_history(step="act中工具结果",role="tool_result", content=f" from:{exist_tool.name} result:{observation}")
            await self.think(query)
        else:
            self.set_history(step="act中工具不存在",role="assistant", content=f"{name.name.lower()}不存在！")
            await self.think(query)

    async def execute(self,query:str):
        """
        执行工作流
        @param query:
        @return:
        """

        await self.think(query)
        final_answer="\n\n*********final answer*********:"+self.history[-1].content
        self.custom_logger.info(final_answer)
        return final_answer


#本质是有记忆的 但不是list based的 用的是quey的


    def set_history(self, role: str, content: str,step=""):
        """

        保存重要历史
        @param step: 用于日志判断而已
        @param role:
        @param content:
        @return:
        """
        self.custom_logger.info(f"\n\n---------------------------{step}---------------------\n\n{role}:::\n{content}\n\n------------------------------------------------")
        self.history.append(Message(role=role, content=content))

    def get_history(self):
       """加载重要历史"""
       return "\n".join([f"{message.role}: {message.content}" for message in self.history])


    def set_tool(self,name:NAME,func:Callable[...,Any]):
        self.tools[name]=tool(name,func)

    def use_tool(self):
        pass




async def main_react():
    new_agent=ReactAgent()
    new_agent.set_tool(NAME.COUNT_FILES, count_files)
    new_agent.set_tool(NAME.FIND_FILES, find_files)
    run=await new_agent.execute("上一级文件夹下py")
    print(run)



if __name__=="__main__":

    import asyncio
    asyncio.run(main_react())

