<script lang="ts">
    // Import any necessary components
    function copyCommand() {
        navigator.clipboard.writeText('bash oneclick.sh');
        // Could add toast notification here
    }
</script>

<section class="fixed top-0 left-0 w-full h-full py-16 px-4">
  <div class="max-w-6xl mx-auto h-full flex flex-col justify-center">
    <div class="text-center mb-12">
      <h1 class="text-8xl font-bold gradient-text mb-4">Layer8 Sandbox</h1>
      <p class="text-2xl text-slate-200 max-w-2xl mx-auto">Get your isolated environment for private LLM</p>
    </div>
    
    <div class="card-blur p-8 w-full">
      <div class="bg-dark bg-opacity-60 rounded-lg p-6 flex flex-col space-y-8">
        <h2 class="font-bold text-center text-slate-100 text-3xl">Getting Started</h2>

        <div class="flex flex-col space-y-4">
          <div class="flex items-center space-x-4">
            <p class="text-slate-200 text-xl">Download this file to get started</p>
          </div>
          <div>
            <a 
              href="https://drive.google.com/uc?export=download&id=1Cs6MMyx7wgqeC32SQ9taF9_KNGO5Esww" 
              class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg inline-flex items-center space-x-2 transition text-xl"
              download
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              <span>Get Sandbox</span>
            </a>
          </div>
        </div>

        <div class="flex flex-col space-y-4 mt-8">
          <p class="text-slate-200 text-xl">After getting the sandbox, run the command:</p>
          <div class="bg-gray-900 p-3 rounded-lg flex justify-between items-center">
            <code class="text-green-400 font-mono text-xl">bash oneclick.sh</code>
            <button 
              on:click={copyCommand}
              class="ml-4 p-2 bg-gray-700 hover:bg-gray-600 rounded"
              title="Copy to clipboard"
              aria-label="Copy command to clipboard"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
