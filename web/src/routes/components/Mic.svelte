<script lang="ts">
  import { onDestroy } from "svelte";
  import { RecordRTCPromisesHandler } from "recordrtc";

  export let record: boolean;
  export let onFail: () => void;
  export let onChange: (transcript: string, interm: string) => void;

  let socket: WebSocket | null = null;
  let stream: MediaStream | null = null;
  let recorder: RecordRTCPromisesHandler | null = null;

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

    // stop the recorder
    console.log("stopping recorder", recorder);
    await recorder?.stopRecording();
    await recorder?.destroy();

    // stop the stream
    console.log("stopping stream", stream);
    stream?.getTracks().forEach((track) => track.stop());
  }

  function initializeSocket() {
    socket = new WebSocket("ws://localhost:8000/");
    socket.onerror = (error) => {
      console.error(error);
      onFail();
      alert("Could not connect to the transcription server :(");
    };
    socket.onopen = initializeRecorder;
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleTranscriptAvailable(data);
    };
    socket.onclose = () => {
      if (record) {
        onFail();
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
        timeSlice: 100,
        ondataavailable: onDataAvailable,
      });
      recorder.startRecording();
    } catch (error) {
      console.error(error);
      onFail();
      alert("Either you don't have a microphone or you denied access to it.");
    }
  }

  function onDataAvailable(audioChunk: Blob) {
    if (audioChunk.size > 0 && socket?.readyState === WebSocket.OPEN) {
      // TODO: Send user and time?
      socket.send(audioChunk);
    }
  }

  function handleTranscriptAvailable(event: any) {
    let transcript = "";
    let potential = "";
    for (const result of event) {
      if (result.is_final) {
        transcript += result.transcript;
      } else {
        potential += result.transcript;
      }
    }
    onChange(transcript, potential);
  }
</script>
