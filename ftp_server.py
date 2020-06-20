import sys, os
from socket import *
from threading import Thread
import time


HOST='0.0.0.0'
PORT=8888
ADDR=(HOST,PORT)

FTP = '/home/tarena/FTP/'


class FTPServer(Thread):
    def __init__(self,connfd):
        self.connfd = connfd
        super().__init__()


    def do_list(self):
        file_list = os.listdir(FTP)
        if not file_list:
            self.connfd.send(b'FAIL')
            return

        else:
            self.connfd.send(b"OK")
            time.sleep(0.1)
            data = "\n".join(file_list)  # 将文件拼接
            self.connfd.send(data.encode())
            time.sleep(0.1)
            self.connfd.send(b"##")

    def do_get(self,filename):
        try:
            f = open(FTP+filename, 'rb')
        except:
            self.connfd.send(b'FAIL')
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.connfd.send(b'##')
                    break
                self.connfd.send(data)
            f.close()

    def do_put(self,filename):
        if os.path.exists(FTP+filename):
            self.connfd.send(b'FAIL')
            return
        else:
            self.connfd.send(b'OK')
            f = open(FTP+filename,'wb')
            while True:
                data = self.connfd.recv(1024)
                if data == b'##':
                    break
                f.write(data)
            f.close()

    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            if not data or data == 'EXIT':
                self.connfd.close()
                return
            elif data == 'LIST':
                self.do_list()
            elif data[:3] == 'GET':
                filename = data.split(' ')[-1]
                self.do_get(filename)
            elif data [:3] =='PUT':
                filename = data.split(' ')[-1]
                self.do_put(filename)

def main():
    sock= socket()
    sock.bind(ADDR)
    sock.listen(5)

    print('Listen the port %d' % PORT)

    while True:
        try:
            connfd,addr=sock.accept()
            print('客户端地址:',addr)
        except KeyboardInterrupt:
            sock.close()
            sys.exit('服务端退出')

        t=FTPServer(connfd)
        t.start()

if __name__ == '__main__':
    main()