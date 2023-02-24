<script lang="ts">
  import { onDestroy } from "svelte";
  import { RecordRTCPromisesHandler } from "recordrtc";

  export let record: boolean;
  export let onFail: (message: string) => void;
  export let onChange: (transcript: string) => void;

  let socket: WebSocket | null = null;
  let stream: MediaStream | null = null;
  let recorder: RecordRTCPromisesHandler | null = null;
  let initializingPromise: Promise<void> | null = null;

  $: record ? onRecord() : onStop();
  onDestroy(onStop);

  function onRecord() {
    console.log("Opening connection");
    initializeSocket();
  }

  async function onStop() {
    console.log("stopping");

    // close the socket
    console.log("closing socket", socket);
    socket?.close();
    socket = null;

    if (initializingPromise) {
      console.log("waiting for initialization to finish");
      await initializingPromise;
    }

    // stop the stream
    console.log("stopping stream", stream);
    stream?.getTracks().forEach((track) => track.stop());
    stream = null;

    // stop the recorder
    console.log("stopping recorder", recorder);
    await recorder?.stopRecording();
    await recorder?.destroy();
    recorder = null;
  }

  function initializeSocket() {
    socket = new WebSocket("ws://localhost:8000/");
    socket.onerror = (error) => {
      console.error(error);
      onFail("Could not connect to the transcription server :(");
    };
    socket.onopen = () => {
      console.log("socket opened");
      initializingPromise = initializeRecorder();
    };
    socket.onmessage = (event) => {
      console.log("message received", event.data);
      onChange(event.data);
    };
    socket.onclose = () => {
      if (record) {
        onFail("The transcription server failed :(");
      }
    };
  }

  async function initializeRecorder() {
    console.log("initializing recorder");
    try {
      stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
        video: false,
      });
      recorder = new RecordRTCPromisesHandler(stream, {
        type: "audio",
        mimeType: "audio/webm",
        // TODO: should this be configurable?
        timeSlice: 100,
        ondataavailable: onDataAvailable,
      });
      await recorder.startRecording();
      console.log("DONE initializing recorder");
    } catch (error) {
      console.error(error);
      onFail("Either you don't have a microphone or you denied access to it.");
    }
  }

  function onDataAvailable(audioChunk: Blob) {
    console.log("data available", audioChunk);
    if (audioChunk.size > 0 && socket?.readyState === WebSocket.OPEN) {
      console.log("sending data");
      socket.send(audioChunk);
    }
  }
</script>
