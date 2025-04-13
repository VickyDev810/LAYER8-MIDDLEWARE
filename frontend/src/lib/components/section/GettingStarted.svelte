<script lang="ts">
    import Button from '$lib/components/ui/Button.svelte';
    import Navbar from '$lib/components/ui/Navbar.svelte';
  
    export let securityImage: string = 'src/assets/images/aiImage.svg';
    export let onClickHandler: () => void;
  </script>
  
  <section class="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#05102a] to-[#0b0f28] text-white px-6 py-16">
    <div class="w-[90%] bg-[radial-gradient(at_top_right,_#120143,_#183b88)] rounded-2xl shadow-lg p-8 md:p-12 flex flex-col gap-10">
      
      <Navbar />
  
      <div class="flex flex-col md:flex-row items-center gap-10">
        <!-- Text Content -->
        <div class="flex-1 text-center md:text-left space-y-6">
          <h1 class="text-4xl sm:text-5xl font-bold leading-tight text-white drop-shadow-md">
            Layer8 <span class="text-blue-400">MIDDLEWARE</span>
          </h1>
          <p class="text-gray-400 font-[500] text-base sm:text-2xl max-w-md">
            AI Without Compromise – Secure Your Data, Empower Your Intelligence
          </p>
          <div class="mb-24"></div>
          <div class="flex justify-center md:justify-start">
            <Button
              text="GET STARTED"
              className="bg-blue-500 hover:bg-blue-400 text-gray-900 font-bold px-8 py-3 rounded-lg shadow-md transition"
              onClick={onClickHandler}
            />
          </div>
        </div>
  
        <!-- Image -->
        <div class="flex-1 flex justify-center">
          <img
            src={securityImage}
            alt="Data Protection Illustration"
            class="w-full max-h-[250px] md:max-h-[600px] lg:max-h-[650px] drop-shadow-xl"
          />
        </div>
      </div>
    </div>
  </section>
  