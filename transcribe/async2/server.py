from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketState
import uvicorn
import asyncio
from gcp_asr import transcribe

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def queue_chunks(websocket, chunk_queue):
    print("queue_chunks")
    async for chunk in websocket.iter_bytes():
        # print("got chunk")
        await chunk_queue.put(chunk)
    await chunk_queue.put(None)
    raise Exception("Client disconnected")


async def send_transcriptions(websocket, transcriber):
    print("send_transcriptions")
    async for transcription in transcriber:
        print("got transcription")
        await websocket.send_text(transcription)


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("connected")

    # The queue for the audio chunks
    chunk_queue = asyncio.Queue()

    try:
        await asyncio.gather(
            queue_chunks(websocket, chunk_queue),
            send_transcriptions(websocket, transcribe(chunk_queue)),
        )
    except Exception as e:
        print(e)
    finally:
        print("disconnected")
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close()
        print("closed")


if __name__ == "__main__":
    PORT = 8000
    print(f"AphasiaGTP transcription server is running on http://localhost:{PORT}")
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, log_level="info")
