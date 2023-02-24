from google.cloud import speech_v1 as speech


def gcp_config():
    client = speech.SpeechAsyncClient.from_service_account_json("text-to-speech-key.json")

    speech_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=48000,
        language_code="en-US",
        max_alternatives=1,
        # model="latest_long",
        enable_automatic_punctuation=False,  # use-case driven
        enable_spoken_punctuation=True,
        # use_enhanced=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=speech_config,
        interim_results=True,
        single_utterance=False,
    )
    return client, streaming_config


async def transcribe(chunks):
    client, streaming_config = gcp_config()
    
    async def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    # Make the request
    print("calling streaming_recognize")
    stream = await client.streaming_recognize(requests=request_generator())
    print("got async response iterator")

    async for transcript in parse(stream):
        yield transcript


async def parse(stream):
    unfinal_transcript = ""
    async for response in stream:
        print(response.results)

        prev_transcript, post_transcript, next_unfinal_transcript = stage_groups(
            group_results(response.results)
        )

        prev_to_send = prev_transcript[len(unfinal_transcript) :]
        transcript = prev_to_send + post_transcript
        unfinal_transcript = next_unfinal_transcript

        yield transcript


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


# # TODO: it needs to handle when GPC times out
# async def transcribe(chunks):
#     # raise Exception("GCP timeout")
#     unfinal_transcript = ""

#     async def request_generator():
#         yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
#         print("yielded initial request")
#         async for chunk in chunks:
#             yield speech.StreamingRecognizeRequest(audio_content=chunk)
#             print("yielded chunk")

#     print("calling streaming_recognize")
#     responses = await speech_client.streaming_recognize(
#         requests=request_generator()
#     )

#     print("got async response iterator")
#     async for response in responses:
#         print(response.results)

#         prev_transcript, post_transcript, next_unfinal_transcript = stage_groups(
#             group_results(response.results)
#         )

#         prev_to_send = prev_transcript[len(unfinal_transcript) :]
#         transcript = prev_to_send + post_transcript
#         unfinal_transcript = next_unfinal_transcript

#         yield transcript








# from google.cloud import speech_v1 as speech


async def sample_streaming_recognize():
    # Create a client
    client = speech.SpeechAsyncClient.from_service_account_json("text-to-speech-key.json")

    speech_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=48000,
        language_code="en-US",
        max_alternatives=1,
        # model="latest_long",
        enable_automatic_punctuation=False,  # use-case driven
        enable_spoken_punctuation=True,
        # use_enhanced=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=speech_config,
        interim_results=True,
        single_utterance=False,
    )


    async def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)

    # Make the request
    print("calling streaming_recognize")
    stream = await client.streaming_recognize(requests=request_generator())
    print("got async response iterator")

    return stream


    # Handle the response
    # async for response in stream:
    #     print(response)


import asyncio

if __name__ == "__main__":

    async def gen():
        yield b""

    asyncio.run(sample_streaming_recognize())

