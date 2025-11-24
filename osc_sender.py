from pythonosc import udp_client

# TD的默认监听端口（TD同学设置这个）
client = udp_client.SimpleUDPClient("127.0.0.1", 8000)

def send_hand_position(x, y):
    # 发给TD的OSC地址
    client.send_message("/handpos", [x, y])