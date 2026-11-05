from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import ai, movies, recommendations

app = FastAPI()

origins = ["http://127.0.0.1:5173", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router)
app.include_router(recommendations.router)
app.include_router(ai.router)


# @app.get("/")
# async def root():
#     return {"message": "Hello Bigger Applications!"}

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
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                console.log(content)
                messages.appendChild(message)
                console.log(message)
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


@app.get("/")
async def get():
    return "rdha"


from fastapi import WebSocket, WebSocketDisconnect


@app.websocket("/ws")
async def agent_websocket(websocket: WebSocket):
    await websocket.accept()

    try:
        # Send immediately after connection
        await websocket.send_json({
            "type": "search_movie",
            "query": "Batman",
        })

        while True:
            message = await websocket.receive_json()
            print("Received:", message)

    except WebSocketDisconnect:
        print("Client disconnected")
