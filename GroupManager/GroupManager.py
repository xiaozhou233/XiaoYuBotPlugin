from utils.Plugin import Plugin
from utils.Config import FileConfig
from utils.File import File

class GroupManager(Plugin):
    def __init__(self):
        config = FileConfig("plugins/GroupManager/config.json").config
        super().__init__(config)
        self.name = "GroupManager"
        self.description = "群管理插件"
        self.author = "xiaozhou233"
        self.version = "1.0.0"
        self.config = config

    async def on_message(self, message, ws_client):
        message_info = message.get("message")
        if message_info:
            if message_info[0].get("type") == "at" and message_info[0].get("data").get("qq") == str(message.get("self_id")):
                if len(message_info) == 2:
                    message_text = message_info[1].get("data").get("text")
                else:
                    message_text = None
                if message_text:
                    await self.handle(message_text, ws_client, message)
                
    async def handle(self, raw_message, ws_client, message):
        raw_message_without_space = raw_message.replace(" ", "")
        group_config = File(f"plugins/GroupManager/groups/{message.get('group_id')}.json").config
        if group_config:
            is_admin = message.get("sender").get("user_id") in group_config.get("admin")
            if raw_message_without_space == "/群管理":
                if  is_admin:
                    await ws_client.send_group_msg(message.get("group_id"), "你是群管理")
                else:
                    await ws_client.send_group_msg(message.get("group_id"), "你不是群管理")
            elif raw_message_without_space.startswith("/添加关键词"):
                if is_admin:
                    await self.add_keywords(raw_message, ws_client, message)
                else:
                    await ws_client.send_group_msg(message.get("group_id"), "你不是群管理")
            elif raw_message_without_space.startswith("/删除关键词"):
                if is_admin:
                    await self.delete_keywords(raw_message, ws_client, message)
                else:
                    await ws_client.send_group_msg(message.get("group_id"), "你不是群管理")
            elif raw_message_without_space.startswith("/关键词列表"):
                await self.show_keywords(raw_message, ws_client, message)
            else:
                for keyword in group_config.get("keywords"):
                    if keyword.get("enble"):
                        if raw_message_without_space == keyword.get("keyword"):
                            await ws_client.send_group_msg(message.get("group_id"), keyword.get("reply"))
        else:
            await ws_client.send_group_msg(message.get("group_id"), "群配置文件不存在，请联系管理员添加~")

    async def add_keywords(self, raw_message, ws_client, message):
        slipt_message = raw_message.split(" ")
        for i in range(len(slipt_message)):
            if slipt_message[i] == "/添加关键词":
                keyword = slipt_message[i+1]
                reply = slipt_message[i+2]
                print(keyword, reply)
                break
        group_config = File(f"plugins/GroupManager/groups/{message.get('group_id')}.json").config
        if group_config:
            group_config.get("keywords").append({"keyword": keyword, "reply": reply, "enble": True})
            File(f"plugins/GroupManager/groups/{message.get('group_id')}.json").write_config(group_config)
            await ws_client.send_group_msg(message.get("group_id"), "添加成功")

    async def delete_keywords(self, raw_message, ws_client, message):
        slipt_message = raw_message.split(" ")
        for i in range(len(slipt_message)):
            if slipt_message[i] == "/删除关键词":
                keyword = slipt_message[i+1]
                break
        group_config = File(f"plugins/GroupManager/groups/{message.get('group_id')}.json").config
        if group_config:
            for keyword_config in group_config.get("keywords"):
                if keyword_config.get("keyword") == keyword:
                    group_config.get("keywords").remove(keyword_config)
                    File(f"plugins/GroupManager/groups/{message.get('group_id')}.json").write_config(group_config)
                    await ws_client.send_group_msg(message.get("group_id"), "删除成功")
                    break
            else:
                await ws_client.send_group_msg(message.get("group_id"), "关键词不存在")

    async def show_keywords(self, raw_message, ws_client, message):
        group_config = File(f"plugins/GroupManager/groups/{message.get('group_id')}.json").config
        if group_config:
            keywords = group_config.get("keywords")
            if len(keywords) == 0:
                await ws_client.send_group_msg(message.get("group_id"), "暂无关键词")
            else:
                await ws_client.send_group_msg(message.get("group_id"), "关键词列表：\n" + "\n".join([f"{keyword.get('keyword')}: {keyword.get('reply')}" for keyword in keywords]))
                


        
            