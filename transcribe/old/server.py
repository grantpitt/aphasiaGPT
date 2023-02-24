from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketState
import uvicorn
import queue
import asyncio
import threading
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


async def receive_chunks(websocket, chunk_queue, failer):
    print("hello from receive_chunks")
    async for chunk in websocket.iter_bytes():
        print("checking if disconnected")
        if failer["died"]:
            break
        print("received chunk")
        chunk_queue.put(chunk)
    chunk_queue.put(None)
    print("done receiving chunks")


async def send_transcriptions(websocket, transcriber):
    async for transcription in transcriber:
        if websocket.client_state == WebSocketState.DISCONNECTED:
            return
        await websocket.send_text(transcription)


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    print("HERE1")
    await websocket.accept()

    # await 4 seconds to make sure the client is ready
    #print("HERE2")
    await asyncio.sleep(0.01)

    print("HERE3")
    # set up a queue to hold audio chunks
    chunk_queue = queue.Queue()

    # flag to tell the thread to stop
    # failer = {"died": False}

    print("HERE4")

    transcriber = transcribe(chunk_queue)


    thread = threading.Thread(
        target=asyncio.run, args=(send_transcriptions(websocket, transcriber),)
    )
    thread.start()
    # start a thread to receive audio chunks and put them in the queue
    # run with run_coroutine_threadsafe
    # loop = asyncio.get_event_loop()
    # my_coroutine = receive_chunks(websocket, chunk_queue, failer)
    # reciever = asyncio.run_coroutine_threadsafe(my_coroutine, loop)

    # await asyncio.sleep(0.1)

    print("HERE5")

    # transcribe the audio chunks and respond to the client
    try:

        async for chunk in websocket.iter_bytes():
            chunk_queue.put(chunk)
        
        chunk_queue.put(None)
        # transcriber = transcribe(chunk_queue)
        # async for transcription in transcriber:
        #     if websocket.client_state == WebSocketState.DISCONNECTED:
        #         break
        #     await websocket.send_text(transcription)

    except Exception as e:
        print(e)

    finally:

        print("TRYING TO CLOSE THREAD")

        # set flag to True to
        # failer["died"] = True

        # close the thread
        print("closing thread")
        # await reciever.result()
        print("thread closed")

        # close the websocket (if it's not already closed)
        if websocket.client_state != WebSocketState.DISCONNECTED:
            print("closing websocket")
            await websocket.close()

        print("socket closed")

    # transcriber = transcribe(chunk_queue)
    # thread = threading.Thread(
    #     target=asyncio.run, args=(send_transcriptions(websocket, transcriber),)
    # )
    # thread.start()

    # try:
    #     async for chunck in websocket.iter_bytes():
    #         chunk_queue.put(chunck)
    # except Exception as e:
    #     print(e)
    # finally:
    #     chunk_queue.put(None)
    #     thread.join()
    #     if websocket.client_state != WebSocketState.DISCONNECTED:
    #         await websocket.close()


if __name__ == "__main__":
    PORT = 8000
    print(f"AphasiaGTP transcription server is running on http://localhost:{PORT}")
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, log_level="info")
