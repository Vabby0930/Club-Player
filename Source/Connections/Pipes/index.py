import socketio as Socket;

def Pipes( Application ) :
    Server = Socket.AsyncServer(async_mode="asgi", cors_allowed_origins="*");
    Pipe = Socket.ASGIApp( Server , Application );
    
    @Server.event
    async def connect(sid, environ):
        print(f"Client {sid} connected")
        await Server.emit("messages", {"msg": "Welcome to the Socket.IO server!"}, to=sid)
        
    @Server.event
    async def request(sid, data):
        print(f"Message from {sid}: {data}")
        await Server.emit("response", {"msg": f"Server received: {data}"}, to=sid)
        
    @Server.event
    async def disconnect(sid):
        print(f"Client {sid} disconnected")
        
    Application.mount("/", Pipe);