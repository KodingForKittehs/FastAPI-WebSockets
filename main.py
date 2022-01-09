import logging
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

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logging.info(websocket)
    await websocket.accept()
    logging.info(f'accept() {websocket}')
    while True:
        data = await websocket.receive_text()
        logging.info(f'receive_text() {data} {websocket}')
        result = await websocket.send_text(f"Message text was: {data}")
        logging.info(f'send_text() {result} {websocket}')

logging.basicConfig(level=logging.INFO)
uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
