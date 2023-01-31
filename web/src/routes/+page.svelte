<script lang="ts">
  import Controls from "./components/Controls.svelte";

  let recording = false;

  function onBack() {
    console.log("back");
  }

  function onPlayPause() {
    console.log("play/pause");
    recording = !recording;
  }
</script>

<header class="p-4 mb-4">
  <h1 class="text-3xl font-semibold my-2">Aphasia GPT</h1>
  <p>
    this is a project to help those with Aphasia by using GTP for cleaning and predicting speech
  </p>
</header>

<Controls {onBack} {onPlayPause} {recording} />


