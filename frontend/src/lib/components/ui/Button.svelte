<script lang="ts">
    export let text: string;
    export let className: string = "";
    export let onClick: () => void;
  </script>
  
  <button
    class="px-6 py-3 rounded-md text-white transition hover:opacity-80 {className}"
    on:click={onClick}
  >
    {text}
  </button>
  