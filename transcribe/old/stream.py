from google.cloud import speech
import queue

speech_client = speech.SpeechClient.from_service_account_json("../text-to-speech-key.json")

speech_config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
    sample_rate_hertz=48000,
    language_code="en-US",
    max_alternatives=1,
    model="latest_long",
    enable_automatic_punctuation=False,  # use-case driven
    enable_spoken_punctuation=True,
    # use_enhanced=True,
)

streaming_config = speech.StreamingRecognitionConfig(
    config=speech_config,
    interim_results=True,
    single_utterance=False,
)

def group_results(results):
    groups = []
    group_transcript = ""
    for result in results:
        group_transcript += result.alternatives[0].transcript
        if result.is_final:
            groups.append({"transcript": group_transcript, "is_final": True})
            group_transcript = ""

    if group_transcript != "":
        groups.append({"transcript": group_transcript, "is_final": False})

    return groups


# Basically we want to keep track of the unfinalized transcript that's been sent
def stage_groups(groups):
    prev_transcript = ""
    post_transcript = ""
    next_unfinal_transcript = ""
    is_prev = True

    for group in groups:
        next_unfinal_transcript += group["transcript"]

        if is_prev:
            prev_transcript += group["transcript"]
        else:
            post_transcript += group["transcript"]

        if group["is_final"]:
            is_prev = False

            next_unfinal_transcript = ""

    return prev_transcript, post_transcript, next_unfinal_transcript




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
    # raise Exception("GCP is timing out")
    chunks = chunk_generator(chunk_queue)

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in chunks
    )
    responses = speech_client.streaming_recognize(
        config=streaming_config, requests=requests
    )

    unfinal_transcript = ""
    for response in responses:
        prev_transcript, post_transcript, next_unfinal_transcript = stage_groups(
            group_results(response.results)
        )

        prev_to_send = prev_transcript[len(unfinal_transcript) :]
        transcript = prev_to_send + post_transcript
        unfinal_transcript = next_unfinal_transcript

        yield transcript
