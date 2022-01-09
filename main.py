# https://websockets.readthedocs.io/en/stable/

#import asyncio
#import websockets
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("wss://Python-WebSockets.grimtalon.repl.co/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

app = FastAPI()

#async def echo(websocket):
#    async for message in websocket:
#        await websocket.send(message)

#async def main():
#    async with websockets.serve(echo, "0.0.0.0", 8765):
#        await asyncio.Future()  # run forever

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
#asyncio.run(main())