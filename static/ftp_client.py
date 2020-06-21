

from socket import *
import time
import sys

# 服务器地址
ADDR = ("127.0.0.1",8888)

# 将具体发送请求的方法封装在类中
class FTPClient:
    def __init__(self,sock):
        self.sock = sock

    # 请求文件列表
    def do_list(self):
        self.sock.send(b"LIST") # 发送请求
        result = self.sock.recv(128).decode() # 等待回复
        if result == 'OK':
            # 接收文件列表
            while True:
                file = self.sock.recv(1024).decode()
                if file == "##":
                    break
                print(file)
        else:
            # 结束
            print("文件库为空")

    # 处理下载
    def do_get(self,filename):
        data = "GET "+filename
        self.sock.send(data.encode()) # 发送请求
        # 等待回复
        result = self.sock.recv(128).decode()
        if result == 'OK':
            # 接收文件
            f = open(filename,'wb')
            while True:
                data = self.sock.recv(1024)
                if data == b"##":
                    break
                f.write(data)
            f.close()
        else:
            print("文件不存在")

    # 处理上传
    def do_put(self,filename):
        # 本地判断，看是否文件存在
        try:
            f = open(filename,'rb')
        except:
            print("要上传的文件不存在")
            return
        # 提取真正的文件名 (原来的filename可能包含路径 ../xxxx.jpg)
        filename = filename.split('/')[-1]

        data = "PUT " + filename
        self.sock.send(data.encode())  # 发送请求
        # 等待回复
        result = self.sock.recv(128).decode()
        if result == 'OK':
            # 读取文件发送
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sock.send(b'##')
                    break
                self.sock.send(data)
            f.close()
        else:
            print("该文件存在")

    # 退出
    def do_exit(self):
        self.sock.send(b"EXIT")
        self.sock.close()
        sys.exit("谢谢使用")


# 网络连接
def main():
    sock = socket()
    sock.connect(ADDR)

    ftp = FTPClient(sock) # 实例化对象

    while True:
        print("=========== 命令选项 =============")
        print("***          list           ***")
        print("***        get file         ***")
        print("***        put file         ***")
        print("***          exit          ***")
        print("=================================")

        cmd = input("请输入命令:")
        if cmd == "list":
            ftp.do_list()
        elif cmd[:3] == "get":
            filename = cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3] == "put":
            filename = cmd.split(' ')[-1]
            ftp.do_put(filename)
        elif cmd == 'exit':
            ftp.do_exit()
        else:
            print("请输入正确命令")


if __name__ == '__main__':
    main()
