from google.cloud import speech
import queue

speech_client = speech.SpeechClient.from_service_account_json("text-to-speech-key.json")

speech_config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
    sample_rate_hertz=48000,
    language_code="en-US",
    max_alternatives=1,
    model="latest_long",
    enable_automatic_punctuation=True,
    enable_spoken_punctuation=True,
    # use_enhanced=True,
)

streaming_config = speech.StreamingRecognitionConfig(
    config=speech_config,
    interim_results=True,
    single_utterance=False,
)


def chunk_generator(chunk_queue):
    while True:
        data = []
        chunk = chunk_queue.get()
        if chunk is None:
            return
        data.append(chunk)
        while True:
            try:
                chunk = chunk_queue.get(block=False)
                if chunk is None:
                    return
                data.append(chunk)
            except queue.Empty:
                break
        yield b"".join(data)


# this is an async generator that takes a queue of audio chunks and returns transcriptions
# it needs to handle when GPC times out
async def transcribe(chunk_queue):
    try:
        chunks = chunk_generator(chunk_queue)

        requests = (
            speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in chunks
        )
        responses = speech_client.streaming_recognize(
            config=streaming_config, requests=requests
        )
        for response in responses:
            results = [
                {
                    "transcript": result.alternatives[0].transcript,
                    "is_final": result.is_final,
                    "stability": result.stability,
                }
                for result in response.results
            ]

            print(results)

            yield results

    except Exception as e:
        # TODO: If the exception is the GCP timeout, just try again, is there an easy
        # way to do this? in python
        print(e)
        return
