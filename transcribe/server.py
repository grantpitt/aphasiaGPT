from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketState
import uvicorn
import queue
import asyncio
import threading
# from gpt3_translator import translate, predict
from stream import transcribe

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def send_transcriptions(websocket, transcriber):
    async for transcription in transcriber:
        if websocket.client_state == WebSocketState.DISCONNECTED:
            return
        await websocket.send_json(transcription)


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("connected")
    chunk_queue = queue.Queue()
    transcriber = transcribe(chunk_queue)  # can we sperate this from the socket
    thread = threading.Thread(
        target=asyncio.run, args=(send_transcriptions(websocket, transcriber),)
    )
    thread.start()

    try:
        async for chunck in websocket.iter_bytes():
            chunk_queue.put(chunck)
    except Exception as e:
        print(e)
    finally:
        chunk_queue.put(None)
        thread.join()
        print("disconnected")


if __name__ == "__main__":
    PORT = 8000
    print(f"AphasiaGTP transcription server is running on http://localhost:{PORT}")
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, log_level="info")
