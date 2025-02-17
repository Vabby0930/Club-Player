import os as System;
from fastapi import FastAPI as Api;
from fastapi import Request , File;
from fastapi.responses import JSONResponse as Response;
from fastapi.responses import FileResponse as Files;
from fastapi import UploadFile as Uploader;
from datetime import datetime as Calcs;
from starlette.exceptions import HTTPException as StarletteHTTPException
from Source.Functions.index import Functions;

System.makedirs( "Data/User" , exist_ok=True );
System.makedirs( "Data/Banner" , exist_ok=True );

def Apis() :
    Application = Api();
    Worker = Functions();

    @Application.get("/favicon.ico")
    def Favicon() :
        return Files("Source/favicon.ico");

    @Application.post('/Create')
    async def Create(Request : Request) :
        Data = await Request.json();
        Name = Data['Name'];
        Number = Data['Number'];
        Email = Data['Email'];
        Password = Data['Password'];
        Res = await Worker.Create( Name , Number , Email , Password );
        return Response( Res , status_code=Res['Code'] );

    @Application.post('/Sign')
    async def Sign(Request : Request) :
        Data = await Request.json();
        Email = Data['Email'];
        Password = Data['Password'];
        Res = await Worker.Sign( Email , Password );
        return Response( Res , status_code=Res['Code'] );

    @Application.get('/Details')
    async def Details(Request : Request) :
        Data = Request.query_params;
        Mail = Data['Email'];
        Res = await Worker.Detail( Mail , );
        return Response( Res , status_code=Res['Code'] );

    @Application.put('/Referral')
    async def Details(Request : Request) :
        Data = await Request.json();
        Mail = Data['Email'];
        Code = Data['Code'];
        Res = await Worker.Referral( Mail , Code );
        return Response( Res , status_code=Res['Code'] );

    @Application.put('/Profile-Upload')
    async def Profile ( Request : Request , File : Uploader = File(...) ) :
        try :
            Extention = File.filename.split(".")[-1];
            Name = f"CP-USR-{Calcs.now().strftime('%Y%m%d%H%M%S')}.{Extention}";
            Path = System.path.join( "Data/User" , Name );
            with open( Path , "wb") as X :
                X.write( await File.read() );
            Data = Request.query_params;
            Mail = Data['Email'];
            Res = await Worker.Upload( Mail , Name );
            return Response( Res , status_code=Res['Code'] );
        except Exception as E :
            return Response(
                {
                    "Success" : False,
                    "Message" : "Internal Error",
                    "Error" : str(E)
                }, 500
            );

    @Application.get("/Secure/Profile")
    def Profile(Request: Request):
        Data = Request.query_params
        if len(Data) == 0 :
            return Files("Data/User/Def.png");
        Profile = Data['Profile']
        if not Profile :
            return Files("Data/User/Def.png");
        Path = f"Data/User/{Profile}"
        if not System.path.exists(Path):
            Path = "Data/User/Def.png"
        return Files(Path);

    @Application.get('/Link')
    def Link(Request : Request) :
        Data = Request.query_params;
        Link = Data['Link'];
        Res = Worker.Extracted( Link );
        return Response( Res , status_code=Res['Code'] );

    @Application.exception_handler( StarletteHTTPException )
    async def not_found_handler(Request: Request, exception: StarletteHTTPException):
        if exception.status_code == 404:
            return Response(
                content={
                    "Success": False,
                    "Message": "Route Not Found",
                    "Code": 404
                },
                status_code=404
            )
        return Response(
            content={
                "Success": False,
                "Message": str(exception.detail),
                "Code": exception.status_code
            },
            status_code=exception.status_code
        )

    return Application;