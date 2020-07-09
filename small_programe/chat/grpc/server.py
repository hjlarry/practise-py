from concurrent import futures
import time

import grpc

from proto import chat_pb2
from proto import chat_pb2_grpc


class ChatServer(chat_pb2_grpc.ChatServerServicer):
    def __init__(self):
        self.chat_history = []

    # 新连接的客户端是从这里取消息历史的，已连接的客户端也从这里取新的消息
    def ChatStream(self, request_iterator, context):
        lastindex = 0
        while True:
            while len(self.chat_history) > lastindex:
                n = self.chat_history[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request, context):
        self.chat_history.append(request)
        return chat_pb2.Empty()


if __name__ == "__main__":
    # 同时处理10个客户端
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServerServicer_to_server(ChatServer(), server)
    print("start server, Listen...")
    server.add_insecure_port("[::]:11912")
    # 是另一个守护线程执行的，所以主线程需要while True
    server.start()
    while True:
        time.sleep(64 * 64 * 100)
