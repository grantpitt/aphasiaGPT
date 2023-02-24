from transformers import AutoProcessor, WhisperForConditionalGeneration

processor = AutoProcessor.from_pretrained("openai/whisper-tiny.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny.en")

async def transcribe(chunks):
    try:

        for chunk in chunks:
            inputs = processor(chunk, return_tensors="pt")
            input_features = inputs.input_features

            generated_ids = model.generate(inputs=input_features)

            transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            yield transcription

    except Exception as e:
        print(e)
        return
