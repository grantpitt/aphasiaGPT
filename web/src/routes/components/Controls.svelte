<script lang="ts">
  export let recording: boolean;
  export let onNew: () => void;
  export let onBack: () => void;
  export let onPlayPause: () => void;

  // TODO: Maybe in here we should track how long recording == true and pause after 15 mi
</script>

<div class="flex justify-center my-6">
  <section class="inline-grid grid-cols-3 gap-6">
    <button
      on:click={onNew}
      class="rounded-xl inline-flex flex-col justify-center items-center bg-amber-200 border-2 border-amber-300 cursor-pointer px-12 py-6 hover:bg-amber-300/70 transition-colors"
    >
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
          d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99"
        />
      </svg>
      Start Over
    </button>

    <button
      on:click={onBack}
      class="rounded-xl inline-flex flex-col justify-center items-center bg-pink-200 border-2 border-pink-300 cursor-pointer px-12 py-6 hover:bg-pink-300/60 transition-colors"
    >
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
      Back
    </button>

    <button
      on:click={onPlayPause}
      class="rounded-xl inline-flex flex-col justify-center items-center bg-violet-200 border-2 border-violet-300 cursor-pointer px-12 py-6 hover:bg-violet-300/60 transition-colors"
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
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M15.75 5.25v13.5m-7.5-13.5v13.5"
          />
        </svg>
        Pause
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
        Play
      {/if}
    </button>
  </section>
</div>
