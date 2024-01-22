# Local-Video-Party-Server

Watch downloaded videos together with friends &amp; family

## Steps to run on local machine

-[Prefer Python version 3.6.x]
-[1] Install all required libraries using
     pip install -r requirements.txt
-[2] Run code
     python server_rest.py
## TESTCASES

- [ ] client socket should be deleted when the disconnect server action is called
- [ ] room should be destroyed when there is no one in the room

## CHANGELOG

0.1 websocket server
0.2 rest api
0.3 socket-io
0.4 start video play/pause video
0.5 ssl certificate with nginx as proxy
0.6 chat function added
0.7 video streaming working
0.8 Multipeer streaming done
0.9 Socket reconnection checking
