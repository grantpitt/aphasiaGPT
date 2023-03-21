<script lang="ts">
  import Controls from "./components/Controls.svelte";
  import Mic from "./components/Mic.svelte";
  import { throttle } from "lodash";

  let recording = false;
  let transcript = "";
  let gtp_transcripts: string[] | null = null;

  function onBack() {
    console.log("back");
  }

  function onPlayPause() {
    console.log("play/pause");
    recording = !recording;

    if (!recording) {
      throttledProcessTranscript.cancel();
      processTranscript();
    }
  }

  function onFail(message: string) {
    recording = false;
    alert(message);
  }

  function onNew() {
    transcript = "";
    gtp_transcripts = null;
    throttledProcessTranscript.cancel();
  }

  function handleTranscriptChange(newTranscript: string) {
    transcript += newTranscript;
    throttledProcessTranscript();
  }

  async function processTranscript() {
    const words = transcript.split(" ");
    const minCleanWordCount = 2;
    const maxCleanWordCount = 10;
    console.log(`transcript "${transcript}" words ${words.length}`);
    if (words.length < minCleanWordCount) {
      return;
    }
    const recentTranscript = words.slice(-maxCleanWordCount).join(" ");
    const response = await fetch("/api/gpt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: recentTranscript }),
    });
    const data = await response.json();
    gtp_transcripts = data.texts;
  }

  const throttledProcessTranscript = throttle(processTranscript, 250);
</script>

<section class="max-w-3xl mx-auto p-4">
  <header class="mb-4">
    <h1 class="text-3xl font-semibold my-2">Aphasia GPT</h1>
    <p>
      This is a project to help those with Aphasia by using GPT for correcting and predicting speech
    </p>
  </header>

  <section class="mb-4">
    <Controls {onBack} {onPlayPause} {recording} {onNew} />
    <Mic {recording} onChange={handleTranscriptChange} {onFail} />

    <h2 class="text-2xl font-semibold my-2">Prediction</h2>
    <div class="min-h-[3rem]">
      {#if gtp_transcripts === null}
        <p class="text-xl text-stone-400">No prediction yet</p>
      {:else}
        {#each gtp_transcripts as gtp_transcript}
          <p class="text-xl text-stone-600">
            {gtp_transcript}
          </p>
        {/each}
      {/if}
    </div>

    <h2 class="text-2xl font-semibold my-2">Transcript</h2>
    <p class="text-xl text-stone-400">
      {transcript || "Click play and begin speaking..."}
    </p>
  </section>
</section>
