<script lang="ts">
    // Import any necessary components
    import { onMount } from 'svelte';
    
    // Function to handle extension link clicks
    function handleExtensionClick(browser: string) {
        // In the future, this could redirect to the actual store page
        // For now, just show an alert
        alert(`${browser} extension coming soon!`);
    }

    // Text state management for encryption/decryption
    let encrypted = false;
    let animating = false;
    let displayText = "Hi GPT, I'm building a Privacy Extension. My name is Aditya, email aditya@gmail.com, phone 9876543210, credit card 5326 9854 1234 6789 CVV 666, issued by Axis Bank. My PAN is BZTPM1234A and my address is 14, MG Road, Bengaluru, 560001.";
    let targetText = "";
    let currentText = "";

    const encryptedText = "Hi GPT, I'm building a Privacy Extension. My name is ___PERSON_21a6a129___, email ___EMAIL_6030cb23___, phone ___PHONE_c260e284___260e284___, credit card ___CREDIT_CARD_5e63af8a___ATE_c523728c___, issued by ___ORGANIZATION_edb13c56___. My ___ORGANIZATION_77bf4737___ is ___ORGANIZATION_0fa94d84___ and my address is ___LOCATION_dd51cb3a___, ___PIN_3854f798___.";
    const originalText = "Hi GPT, I'm building a Privacy Extension. My name is Aditya, email aditya@gmail.com, phone 9876543210, credit card 5326 9854 1234 6789 CVV 666, issued by Axis Bank. My PAN is BZTPM1234A and my address is 14, MG Road, Bengaluru, 560001.";

    function toggleEncryption() {
        if (animating) return;
        
        animating = true;
        targetText = encrypted ? originalText : encryptedText;
        encrypted = !encrypted;
        
        let index = 0;
        currentText = "";
        
        const interval = setInterval(() => {
            if (index < targetText.length) {
                currentText = targetText.substring(0, index + 1);
                index++;
            } else {
                clearInterval(interval);
                displayText = targetText;
                animating = false;
            }
        }, 20); // Adjust speed as needed
    }
</script>

<section class="fixed inset-0 py-16 px-4 min-h-screen mt-12">
  <div class="max-w-6xl mx-auto">
    <div class="text-center mb-12">
      <h1 class="text-8xl font-bold gradient-text mb-4">Browser Extension</h1>
      <p class="text-2xl text-purple-200 max-w-2xl mx-auto">Lightweight, Fast, User Friendly Privacy</p>
    </div>

    <div class="flex justify-center gap-6 mb-8">
      <button
        on:click={() => {
          alert('Downloading Chrome extension!');
          const link = document.createElement('a');
          link.href = '/extension/Layer8_Extension.zip';
          link.download = 'Layer8_Extension.zip';
          link.click();
        }}
        class="text-2xl inline-block px-6 py-3 bg-neon-purple bg-opacity-20 hover:bg-opacity-40 border border-neon-purple text-neon-purple rounded-full transition-all cursor-pointer"
      >
        Chrome Extension
      </button>


      <button 
        on:click={() => handleExtensionClick('Firefox')}
        class="text-2xl inline-block px-6 py-3 bg-neon-blue bg-opacity-20 hover:bg-opacity-40 border border-neon-blue text-neon-blue rounded-full transition-all cursor-pointer"
      >
        Firefox Add-on
      </button>
    </div>
    
    <div class="card-blur w-full text-2xl">
      <div class="text-center px-8 pt-8">
        <p class="text-purple-200 mb-6">Install our browser extension to access powerful development tools directly in your browser.</p>
      </div>
      <div class="border border-solid border-white border-opacity-20 max-h-96"></div>
      <div class="p-8 relative ">
        <div class="h-44 overflow-hidden flex items-center mb-6">
          <p class="text-purple-200">
            {animating ? currentText : displayText}
          </p>
        </div>
        <div class="py-10 px-10">
          <button 
            on:click={toggleEncryption}
            class="absolute right-0 bottom-2 px-4 py-2 mr-8 mb-5 font-medium transition-colors duration-300 rounded-full cursor-pointer bg-opacity-20 hover:bg-opacity-40 border"
            class:bg-neon-green={!encrypted}
            class:bg-neon-red={encrypted}
            class:border-neon-green={!encrypted}
            class:border-neon-red={encrypted}
            class:text-neon-green={!encrypted}
            class:text-neon-red={encrypted}
          >
            {encrypted ? "Decrypt" : "Encrypt"}
          </button>
        </div>
       
      </div>
    </div>
  </div>
</section> 