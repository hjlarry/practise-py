from concurrent import futures
import time

import grpc

from proto import chat_pb2
from proto import chat_pb2_grpc


class ChatServer(chat_pb2_grpc.ChatServerServicer):
    def __init__(self):
        self.chats = []

    def ChatStream(self, request_iterator, context):
        lastindex = 0
        while True:
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request, context):
        self.chats.append(request)
        return chat_pb2.Empty()


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServerServicer_to_server(ChatServer(), server)
    print("start server, Listen...")
    server.add_insecure_port("[::]:11912")
    server.start()

    while True:
        time.sleep(64 * 64 * 100)
