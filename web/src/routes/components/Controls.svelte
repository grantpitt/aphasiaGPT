<script lang="ts">
  export let recording: boolean;
  export let onBack: () => void;
  export let onPlayPause: () => void;

  // TODO: Maybe in here we should track how long recording == true and pause after 15 mi
</script>

<section class="flex justify-center gap-6">
  <button on:click={onBack} class="rounded-xl bg-pink-200 border-2 border-pink-300 cursor-pointer inline-block px-12 py-6 hover:bg-pink-300/60 transition-colors">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.75"
      stroke="currentColor"
      class="w-12 h-12 mr-1 -ml-1"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 9.75L14.25 12m0 0l2.25 2.25M14.25 12l2.25-2.25M14.25 12L12 14.25m-2.58 4.92l-6.375-6.375a1.125 1.125 0 010-1.59L9.42 4.83c.211-.211.498-.33.796-.33H19.5a2.25 2.25 0 012.25 2.25v10.5a2.25 2.25 0 01-2.25 2.25h-9.284c-.298 0-.585-.119-.796-.33z"
      />
    </svg>
  </button>

  <button
    on:click={onPlayPause}
    class="rounded-xl bg-violet-200 border-2 border-violet-300 cursor-pointer inline-block px-12 py-6 hover:bg-violet-300/60 transition-colors"
  >
    {#if recording}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.75"
        stroke="currentColor"
        class="w-12 h-12"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 5.25v13.5m-7.5-13.5v13.5" />
      </svg>
    {:else}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.75"
        stroke="currentColor"
        class="w-12 h-12"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.348a1.125 1.125 0 010 1.971l-11.54 6.347a1.125 1.125 0 01-1.667-.985V5.653z"
        />
      </svg>
    {/if}
  </button>
</section>
