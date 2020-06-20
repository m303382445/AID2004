from socket import *

# 创建tcp套接字
s = socket()
s.bind(('0.0.0.0',8000))
s.listen(5)

c,addr = s.accept()  # 浏览器作为客户端会链接我
print("Connect from",addr)

# 接收消息
data = c.recv(4096)  # 接收到浏览器的http请求
print(data.decode())

# 发送给浏览器一些内容，让他显示
# 按照响应格式组织
response = "HTTP/1.1 200 OK\r\n"  # 响应行
response += "Content-Type:text/html\r\n" # 响应头 一个
response += "\r\n" #空行

with open('python.html') as f:
    response +=f.read() # 响应体


c.send(response.encode())

c.close()
s.close()
