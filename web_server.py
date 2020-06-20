'''
web server 程序
使用者可以通过类快速搭建web后端服务，用于展示网页

IO多路复用和http训练
'''
import re
import sys
from socket import *
from select import select


class WebServer:
    def __init__(self, host='0.0.0.0',port=8001,html=None):
        self.host = host
        self.port = port
        self.html = html
        self.address = (host, port)

        self._rlist = []  # 只关注监听套接字
        self._wlist = []
        self._xlist = []

        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind(self):
        self.sock.bind((self.host, self.port))


    def start(self):
        try:
            self.sock.listen(5)
            print('Listen to the port %d'%self.port)
            self._rlist.append(self.sock)
            while True:
                rs, ws, xs = select(self._rlist, self._wlist, self._xlist)
                for r in rs:
                    if r is self.sock:
                        connfd, addr = r.accept()
                        connfd.setblocking(False)
                        self._rlist.append(connfd)

                    else:
                        try:
                            self.handle(r)
                        except:
                            r.close()
                            self._rlist.remove(r)


        except KeyboardInterrupt:
            sys.exit('服务端退出')

    def handle(self,connfd):
        request = connfd.recv(1024*10).decode()
        # print(request)
        pattern = '[A-Z]+\s+(?P<info>/\S*)'
        result = re.match(pattern, request)
        if result:
            info = result.group('info')
            self.get_html(connfd,info)
            # print('请求内容：', info)
        else:
            connfd.close()
            self._rlist.remove(connfd)
            return

    def get_html(self, connfd, info):
        if info == '/':
            filename = self.html + '/index.html'

        else:
            filename = self.html + info

        try:
            fd = open(filename, 'rb')

        except:
            response = 'HTTP/1.1 404 Not Fount\r\n'
            response += 'Content-Type:text/html\r\n'
            response += '\r\n'
            response += '<h1>Sorry...</h1>'
            response = response.encode()
        else:
            data = fd.read()
            response = 'HTTP/1.1 200 OK\r\n'
            response += 'Content-Type:text/html\r\n'
            response += 'Content-Length:%d\r\n' % len(data)
            response += '\r\n'
            response = response.encode() + data
            fd.close()
        finally:
            connfd.send(response)




if __name__ == '__main__':
    #用户确定的，传入参数：地址   要展示什么网页


    httpd = WebServer(host='0.0.0.0', port=8001, html='./static')
    httpd.start()