import json
from utils.Plugin import Plugin
from utils.Config import FileConfig
import requests

class MinecraftServer(Plugin):
    def __init__(self):
        config = FileConfig("plugins/MinecraftServer/config.json").config
        self.name = "MinecraftServer"
        self.description = "查询MC服务器信息"
        self.author = "xiaozhou233"
        self.version = "1.0.0"
        self.config = config

        

    async def on_message(self, message, ws_client):
        if message.get("raw_message") and "/mc" in message.get("raw_message"):
            for group in self.config.get("server"):
                if group.get("group_id") == message.get("group_id"):
                    server_info = await self.get_server_info(group.get("server_ip"))
                    await ws_client.send_group_msg(message.get("group_id"), server_info)
                    return
            else:
                await ws_client.send_group_msg(message.get("group_id"), "本群似乎没有配置MC服务器信息哦~")
            
                    
    
    async def get_server_info(self, server_ip):
        status = "离线"
        players = 0
        motd = ""
        response = requests.get("https://uapis.cn/api/mcserver?server=" + server_ip, timeout=15)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            if response_dict.get("code") == 200:
                if response_dict.get("status") == "online":
                    status = "在线"
                    players = response_dict.get("players")
                    motd = f"{response_dict.get('motd1')}\n{response_dict.get('motd2')}"
            elif response_dict.get("code") == 500:
                status = "服务器IP错误"
        else:
            status = "请求失败"
        return  "服务器IP: {}\n服务器状态： {}\n在线玩家： {}\n\n服务器信息： {}".format(server_ip,status, players, motd)
        