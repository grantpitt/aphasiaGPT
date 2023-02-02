<script lang="ts">
  import Controls from "./components/Controls.svelte";
  import Mic from "./components/Mic.svelte";

  let recording = false;
  let transcript = "";
  let potential = "";

  function onBack() {
    console.log("back");
  }

  function onPlayPause() {
    console.log("play/pause");
    recording = !recording;
  }

  function onFail() {
    recording = false;
  }

  function onNew() {
    recording = false;
    transcript = "";
    potential = "";
  }

  function handleTranscriptChange(newTranscript: string, newPotential: string) {
    transcript += newTranscript;
    potential = newPotential;
  }
</script>

<section class="max-w-3xl mx-auto p-4">
  <header class="mb-4">
    <h1 class="text-3xl font-semibold my-2">Aphasia GPT</h1>
    <p>
      This is a project to help those with Aphasia by using GTP for correcting and predicting speech
    </p>
  </header>
  
  <section class="mb-4">
    <Controls {onBack} {onPlayPause} {recording} {onNew} />
    <Mic record={recording} onChange={handleTranscriptChange} {onFail} />
  
    <h2 class="text-2xl font-semibold my-2">Transcript</h2>
    <p class="text-xl">{transcript} <span class="text-stone-400">{potential}</span></p>
  </section>
</section>
