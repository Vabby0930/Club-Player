import yt_dlp;
import re as Regx;
import random as Rand;
import string as Str;
from datetime import datetime as Calcs;
from datetime import timedelta as Lapser;
from urllib.parse import urlparse, parse_qs;
from Source.Bases.Sql import Executer , Fetcher;

class Functions :

    async def Create( self , Name , Number , Email , Password ) :
        if bool( Regx.match(r"^[a-z0-9@.]+$", Email) ) :
            User = Fetcher( "SELECT Identifier FROM User WHERE Mail = %s" , ( Email , ) )
            if User['Data'] :
                return {
                    "Success" : False,
                    "Message" : "Email already exists",
                    "Code" : 301
                };
            if len(Password) > 20 :
                return {
                    "Success" : False,
                    "Message" : "Password Must Be 20 Chars or Less",
                    "Code" : 301
                };
            async def Genrator() :
                Code = ''.join( Rand.choices( Str.ascii_uppercase + Str.digits , k=8 ) );
                Exists = Fetcher( "SELECT Identifier FROM User WHERE Code = %s" , ( Code , ));
                if Exists['Data'] :
                    return await Genrator();
                return Code;
            Referral = await Genrator();
            Created = Executer(
                Query = "INSERT INTO User ( Name , Number , Mail , Password , Code ) VALUES (%s, %s, %s, %s, %s)",
                Params = ( Name , Number , Email , Password , Referral ),
            );
            if Created['Success'] :
                return {
                    "Success" : True,
                    "Message" : "Account Created",
                    "Code" : 200
                };
            return {
                "Success" : False,
                "Message" : "Internal Error",
                "Code" : 500
            };
        return {
            "Success" : False,
            "Message" : "Invalid Email Address.",
            "Code" : 301
        };

    async def Sign( self , Email , Password ) :
        if bool( Regx.match(r"^[a-z0-9@.]+$", Email) ) :
            if len(Password) > 20 :
                return {
                    "Success" : False,
                    "Message" : "Password Must Be 20 Chars or Less",
                    "Code" : 301
                };
            Signature = Fetcher(
                Query = "SELECT * FROM User WHERE Mail=%s",
                Params = ( Email , ),
            );
            if Signature['Success'] :
                if len(Signature["Data"]) == 0 :
                    return {
                        "Success" : False,
                        "Message" : "User Not Registered With This Mail",
                        "Code" : 402
                    };
                if Signature['Data'][0]['Password'] == Password :
                    return {
                        "Success" : True,
                        "Message" : "Signature Matched",
                        "Code" : 200
                    };
                return {
                    "Success" : False,
                    "Message" : "Wrong Password",
                    "Code" : 401
                };
            return {
                "Success" : False,
                "Message" : Signature['Error'],
                "Code" : 500
            };
        return {
            "Success" : False,
            "Message" : "Invalid Email Address.",
            "Code" : 301
        };

    async def Detail( self , Email ) :
        if bool( Regx.match(r"^[a-z0-9@.]+$", Email) ) :
            Details = Fetcher(
                Query = "SELECT * FROM User WHERE Mail=%s",
                Params = ( Email , ),
            );
            if Details['Success'] :
                if len(Details["Data"]) == 0 :
                    return {
                        "Success" : False,
                        "Message" : "User Not Registered With This Mail",
                        "Code" : 402
                    };
                return {
                    "Success" : True,
                    "Data" : {
                        "Identifier" : Details["Data"][0]['Identifier'],
                        "Name" : Details["Data"][0]['Name'],
                        "Number" : Details["Data"][0]['Number'],
                        "Email" : Details["Data"][0]['Mail'],
                        "Password" : Details["Data"][0]['Password'],
                        "Profile" : Details["Data"][0]['Profile'],
                        "Code" : Details["Data"][0]['Code'],
                        "Froms" : Details["Data"][0]['Froms'],
                        "Balance" : Details["Data"][0]['Balance'],
                        "Created" : str(Details["Data"][0]['Created']),
                    },
                    "Message" : "Details Found",
                    "Code" : 200
                };
            return {
                "Success" : False,
                "Message" : Details['Error'],
                "Code" : 500
            };
        return {
            "Success" : False,
            "Message" : "Invalid Email Address.",
            "Code" : 301
        };

    async def Upload( self , Email , Name ) :
        if bool( Regx.match(r"^[a-z0-9@.]+$", Email) ) :
            Details = Fetcher(
                Query = "SELECT * FROM User WHERE Mail=%s",
                Params = ( Email , ),
            );
            if Details['Success'] :
                if len(Details["Data"]) == 0 :
                    return {
                        "Success" : False,
                        "Message" : "User Not Registered With This Mail",
                        "Code" : 402
                    };
                Updated = Executer(
                    Query = "UPDATE User SET Profile=%s WHERE Mail=%s",
                    Params = ( Name , Email ),
                );
                if Updated['Success'] :
                    return {
                        "Success" : True,
                        "Message" : "Profile Uploaded",
                        "Data"  : Name,
                        "Code" : 200
                    };
                return {
                    "Success" : False,
                    "Message" : "Internal Error",
                    "Code" : 500
                };
            return {
                "Success" : False,
                "Message" : Details['Error'],
                "Code" : 500
            };
        return {
            "Success" : False,
            "Message" : "Invalid Email Address.",
            "Code" : 301
        };

    async def Referral( self , Email , Code ) :
        if bool( Regx.match(r"^[a-z0-9@.]+$", Email) ) :
            Details = Fetcher(
                Query = "SELECT * FROM User WHERE Mail=%s",
                Params = ( Email , ),
            );
            if Details['Success'] :
                if len(Details["Data"]) == 0 :
                    return {
                        "Success" : False,
                        "Message" : "User Not Registered With This Mail",
                        "Code" : 402
                    };
                Updated = Executer(
                    Query = "UPDATE User SET Froms=%s , Balance=Balance+100 WHERE Mail=%s",
                    Params = ( Code , Email ),
                );
                if Updated['Success'] :
                    def Lapse() :
                        Past = Calcs.strptime( str(Details['Data'][0]['Created']) , "%Y-%m-%d %H:%M:%S" );
                        Now = Calcs.now()
                        Later = Past + Lapser(days=3);
                        if Now <= Later:
                            return 1000
                        else:
                            return 500
                    Amount = Lapse();
                    Reward = Executer(
                        Query = "UPDATE User SET Balance=Balance+%s WHERE Code=%s",
                        Params = ( Amount , Code ),
                    );
                    return {
                        "Success" : True,
                        "Message" : "Referral Created",
                        "Code" : 200
                    };
                return {
                    "Success" : False,
                    "Message" : "Internal Error",
                    "Code" : 500
                };
            return {
                "Success" : False,
                "Message" : Details['Error'],
                "Code" : 500
            };
        return {
            "Success" : False,
            "Message" : "Invalid Email Address.",
            "Code" : 301
        };

    def Extracted( self , URL ) :
        try :
            def Sanitized( URL ) :
                Parsed = urlparse( URL )
                Params = parse_qs( Parsed.query )
                if 'v' in Params :
                    ID = Params['v'][0]
                    return f"https://www.youtube.com/watch?v={ID}"
                return None;
            Link = Sanitized( URL );
            Options = {
                'format': 'best',
                'quiet': True
            };
            with yt_dlp.YoutubeDL (Options ) as Youtube :
                Extracted = Youtube.extract_info( Link , download=False );
                return {
                    "Success" : True,
                    "Message" : "Valid URL",
                    "Data" : Extracted['url'],
                    "Code" : 200
                };
        except :
            return {
                "Success" : False,
                "Message" : "Invalid URL",
                "Code" : 301
            };