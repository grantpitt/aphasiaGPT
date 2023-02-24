from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketState
import uvicorn
import asyncio

# from gpt3_translator import translate, predict
# from gcp_asr import transcribe
from hello import transcribe

# from whisper_asr import transcribe

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def chunk_generator(chunk_queue):
    while True:
        data = []
        chunk = await chunk_queue.get()
        if chunk is None:
            return
        data.append(chunk)
        while True:
            try:
                chunk = chunk_queue.get_nowait()
                if chunk is None:
                    return
                data.append(chunk)
            except asyncio.QueueEmpty:
                break
        yield b"".join(data)


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

    # thread = threading.Thread(
    #     target=asyncio.run, args=(process_chunks(websocket, chunk_queue),)
    # )
    # thread.start()

    # read the audio chunks from the websocket
    # Could create sperate threads, but makes it harder to handle errors

    chunks = chunk_generator(chunk_queue)

    # async for chunk in chunks:
    #     print("consuming chunk")

    transcriber = transcribe(chunks)

    try:
        # await queue_chunks(websocket, chunk_queue)
        await asyncio.gather(
            queue_chunks(websocket, chunk_queue),
            send_transcriptions(websocket, transcriber),
        )
    except Exception as e:
        print("error in websocket_endpoint", e)
    finally:
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close()
        print("closing queue")
        # await chunk_queue.join()
        print("disconnected")

    # try:
    #     async for transcription in transcriber:
    #         await websocket.send_text(transcription)
    # except Exception as e:
    #     print("error in websocket_endpoint")
    #     print(e)
    # finally:
    #     print("in finally")
    #     thread.join()
    #     if websocket.client_state != WebSocketState.DISCONNECTED:
    #         await websocket.close()
    #     print("disconnected")


if __name__ == "__main__":
    PORT = 8000
    print(f"AphasiaGTP transcription server is running on http://localhost:{PORT}")
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, log_level="info")
