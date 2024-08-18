from utils.Plugin import Plugin
from utils.Config import FileConfig

class EchoPlugin(Plugin):
    def __init__(self):
        config = FileConfig("plugins/EchoPlugin/config.json").config
        self.name = "EchoPlugin"
        self.description = "输出收到的消息"
        self.author = "xiaozhou233"
        self.version = "1.0.0"
        self.debugMode = config.get("debugMode")
        

    async def on_message(self, message, ws_client):
        
        if message.get("post_type") == "meta_event":
            self.meta_event_handle(message)
        elif message.get("post_type") == "message":
            self.message_handle(message)
        elif message.get("post_type") == "notice":
            self.notice_handle(message)
        elif message.get("post_type") == "request":
            self.request_handle(message)
        elif message.get("echo") and message.get("echo") == "sent":
            print("[INFO] 已发送消息:", message.get("data").get("message_id"))
        else:
            print("收到未知消息:", message.get("post_type"))
        if self.debugMode:
            print("[Debug]", message)
    
    def meta_event_handle(self, message):
        match message.get("meta_event_type"):
            case "heartbeat":
                pass
            case "lifecycle":
                print("收到生命周期事件:", message.get("sub_type"))
            case _:
                print(f"[META_EVENT] 收到未知元事件: {message.get('meta_event_type')}")

    def message_handle(self, message):
        match message.get("message_type"):
            case "private":
                user_id = message.get("user_id")
                sender_nickname = message.get("sender").get("nickname")
                raw_message = message.get("raw_message")
                print(f"[Private {user_id}] {sender_nickname}> {raw_message}")
            case "group":
                group_id = message.get("group_id")
                sender_nickname = message.get("sender").get("nickname")
                sender_id = message.get("sender").get("user_id")
                raw_message = message.get("raw_message")
                group_role = message.get("sender").get("role")
                print(f"[Group {group_id}] [{group_role}] {sender_nickname}({sender_id})> {raw_message}")
            case _:
                print("[Message] 收到未知消息:", message.get("message_type"))
        
    def notice_handle(self, message):
        match message.get("notice_type"):
            case "group_increase":
                print(f"[Group {message.get('group_id')}] {message.get('user_id')} 加入群聊")
            case "group_decrease":
                print(f"[Group {message.get('group_id')}] {message.get('user_id')} 离开群聊")
            case "group_ban":
                print(f"[Group {message.get('group_id')}] {message.get('user_id')} 被禁言 {message.get('duration')} 秒")
            case "group_admin":
                print(f"[Group {message.get('group_id')}] {message.get('user_id')} 被设置为管理员")
            case "group_upload":
                print(f"[Group {message.get('group_id')}] {message.get('user_id')} 上传了文件 {message.get('file')}")
            case "friend_add":
                print(f"[Friend {message.get('user_id')}] {message.get('user_id')} 添加了好友")
            case "friend_request":
                print(f"[Friend {message.get('user_id')}] {message.get('user_id')} 发起了好友请求")
            case "group_recall":
                print(f"[Group {message.get('group_id')}] {message.get('operator_id')} 撤回了消息 {message.get('message_id')}")
            case "friend_recall":
                print(f"[Friend {message.get('user_id')}] {message.get('operator_id')} 撤回了消息 {message.get('message_id')}")
            case "notice":
                print(f"[Notice] {message.get('notice_type')}")
            case _:
                print("[Notice] 收到未知通知:", message.get("notice_type"))

    def request_handle(self, message):
        match message.get("request_type"):
            case "friend":
                print(f"[Friend Request] {message.get('user_id')}: {message.get('comment')}")
            case "group":
                print(f"[Group Request] {message.get('group_id')}: {message.get('user_id')}: {message.get('comment')}")
            case _:
                print("[Request] 收到未知请求:", message.get("request_type"))

