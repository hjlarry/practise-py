
1. 编写chat.proto

2. 生成grpc相关
```
pip3 install grpcio grpc-tools
python3 -m grpc_tools.protoc -I=proto/ --python_out=proto/ --grpc_python_out=proto/ proto/chat.proto
```

3. 启动服务端，在其他多个shell中启动客户端