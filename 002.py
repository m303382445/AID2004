"""
web server 程序
完成一个类，提供给使用者
使用可通过这个类可以快速搭建web 后端服务，用于展示自己的网页
aswddasasddasasdasdddddddddddgewsrgefrfsdgfdsfsdsdfg
IO多路复用和http训练
"""
from socket import *
from select import select
import re


class WebServer:
    def __init__(self, host="0.0.0.0", port=8001, html=None):
        self.host = host
        self.port = port
        self.html = html
        self.address = (host, port)
        # IO多路复用准备工作
        self._rlist = []
        self._wlist = []
        self._xlist = []
        # 创建套接字
        self.create_socket()
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    # 绑定地址
    def bind(self):
        self.sock.bind((self.host, self.port))

    # 启动函数，启动整个服务 --> 客户端可以发起链接
    def start(self):
        self.sock.listen(5)
        print("Listen to the port %d" % self.port)
        # IO 多路复用
        self._rlist.append(self.sock)  # 关注监听套接字
        while True:
            rs, ws, xs = select(self._rlist, self._wlist, self._xlist)
            for r in rs:
                if r is self.sock:
                    # 有浏览器链接
                    connfd, add = r.accept()
                    connfd.setblocking(False)
                    self._rlist.append(connfd)  # 添加关注
                else:
                    # 处理客户端的具体请求
                    try:
                        self.handle(r)
                    except:
                        r.close()
                        self._rlist.remove(r)

    # 具体业务处理
    def handle(self, connfd):
        request = connfd.recv(1024*10).decode()  # 接收HTTP请求
        # print(request)
        # 解析请求 --> 解析出请求内容  请求行的第二部分
        pattern = "[A-Z]+\s+(?P<info>/\S*)"
        result = re.match(pattern, request)  # 匹配到得到match对象 匹配不要None
        if result:
            # 提取请求内容
            info = result.group("info")
            self.get_html(connfd, info)  # 判定网页是否存在，给客户端发送
        else:
            # 配有匹配到则断开客户端
            connfd.close()
            self._rlist.remove(connfd)
            return

    # 组织数据给客户端回复
    def get_html(self, connfd, info):
        if info == "/":
            filename = self.html + "/index.html"
        else:
            filename = self.html + info

        try:
            fd = open(filename, 'rb')
        except:
            # 请求的网页不存在
            response = "HTTP/1.1 404 Not Fount\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry...</h1>"
            response = response.encode() # 转换为字节串
        else:
            # 请求的网页存在
            data = fd.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "Content-Length:%d\r\n" % len(data)
            response += "\r\n"
            response = response.encode() + data
            fd.close()
        finally:
            connfd.send(response)  # 发送响应结果给客户端


if __name__ == '__main__':
    # 使用者应该怎么用我这个类

    # 什么东西应该是用户确定的，通过参数传入
    # 地址  要展示什么网页

    httpd = WebServer(host="0.0.0.0", port=8001, html="./static")
    httpd.start()
