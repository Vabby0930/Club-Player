import uvicorn;
from Source.Connections.Apis.index import Apis;
from Source.Connections.Pipes.index import Pipes;

def Source( Port ) :
    Application = Apis();
    Pipes( Application );
    uvicorn.run( Application , host="0.0.0.0" , port=Port );