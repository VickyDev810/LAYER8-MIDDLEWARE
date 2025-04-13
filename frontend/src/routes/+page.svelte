<script lang="ts">
    // Import any components you need
    import { onMount } from 'svelte';
    
    // Implement light effect
    onMount(() => {
      // Add mouse light effect for home page
      const existingLights = document.querySelectorAll('.mouse-light');
      if (existingLights.length === 0) {
        const mouseLight = document.createElement('div');
        mouseLight.className = 'mouse-light';
        // Ensure the mouse light is positioned behind content but visible
        mouseLight.style.zIndex = '-1';
        document.body.appendChild(mouseLight);
        
        // Initial position at center
        let mouseX = window.innerWidth / 2;
        let mouseY = window.innerHeight / 2;
        let currentX = mouseX;
        let currentY = mouseY;
        let prevX = mouseX;
        let prevY = mouseY;
        let isMoving = false;
        let movementTimer: ReturnType<typeof setTimeout> | undefined;
        
        // Smoothing factor (0-1, lower = smoother)
        const smoothFactor = 0.15;
        
        // Update light position on mouse move
        document.addEventListener('mousemove', (e) => {
          mouseX = e.clientX;
          mouseY = e.clientY;
          
          // Set moving flag
          isMoving = true;
          clearTimeout(movementTimer);
          
          // Reset flag after movement stops
          movementTimer = setTimeout(() => {
            isMoving = false;
          }, 100);
        });
        
        // For touch devices, update on touch move
        document.addEventListener('touchmove', (e) => {
          if (e.touches && e.touches[0]) {
            mouseX = e.touches[0].clientX;
            mouseY = e.touches[0].clientY;
            
            // Set moving flag
            isMoving = true;
            clearTimeout(movementTimer);
            
            // Reset flag after movement stops
            movementTimer = setTimeout(() => {
              isMoving = false;
            }, 100);
          }
        });
        
        // Smooth animation using requestAnimationFrame
        function animateLight() {
          // Save previous position to calculate movement
          prevX = currentX;
          prevY = currentY;
          
          // Calculate the distance to move
          currentX += (mouseX - currentX) * smoothFactor;
          currentY += (mouseY - currentY) * smoothFactor;
          
          // Calculate movement speed/distance
          const dx = currentX - prevX;
          const dy = currentY - prevY;
          const speed = Math.sqrt(dx * dx + dy * dy);
          
          // Only update color if the mouse is moving (performance optimization)
          if (isMoving) {
            // Adjust color based on movement speed
            const hue = 275; // Base purple hue
            const saturation = Math.min(100, 70 + speed * 2); // Increase saturation with speed
            const brightness = Math.min(60, 45 + speed); // Increase brightness with speed
            
            // Update the light color (subtle effect)
            mouseLight.style.background = `radial-gradient(circle, 
              hsla(${hue}, ${saturation}%, ${brightness}%, 0.6) 0%, 
              hsla(${hue - 10}, ${saturation - 10}%, ${brightness - 10}%, 0.2) 30%, 
              rgba(18, 8, 47, 0) 70%)`;
          }
          
          // Update the light position
          mouseLight.style.left = `${currentX}px`;
          mouseLight.style.top = `${currentY}px`;
          
          // Continue animation
          requestAnimationFrame(animateLight);
        }
        
        // Start animation
        animateLight();
      }
    });
</script>

<!-- Main container with fixed height and no scrolling -->
<div class="fixed top-0 left-0 h-screen w-full overflow-hidden">
  
  <!-- Background Video with Fixed Position -->
  <div class="absolute inset-0 z-0">
    <video class="w-full h-full object-cover" autoplay loop muted playsinline>
      <source src="/planet.webm" type="video/webm">
      Your browser does not support the video tag.
    </video>
  </div>
  
  <!-- Centered Title Text (overlaid on video) -->
  <div class="absolute w-full top-24 z-10 text-center">
    <h1 class="text-4xl md:text-9xl font-bold text-slate-100 mb-4" style="text-shadow: 0 0 5px #a855f7, 0 0 10px #a855f7, 0 0 100px #a855f7, 0 0 40px #a855f7;">Layer8</h1>

    <p class="text-xl text-white max-w-2xl mx-auto">Privacy Middleware Between You and AI</p>
  </div>
  
  <!-- Blurry Container for Cards (positioned at bottom) -->
  <div class="absolute bottom-[135px] left-0 right-0 z-10 backdrop-blur-md bg-purple-950 bg-opacity-[40%] py-12 px-4">
    <div class="max-w-6xl mx-auto">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- AI Assistant Card -->
        <div class="card-blur p-6 flex flex-col h-full text-center transition-all duration-300 hover:shadow-[0_0_15px_rgba(168,85,247,0.7)] hover:border-purple-500">
          <div class="mb-4">
            <h2 class="text-2xl font-semibold text-neon-purple mb-2">AI Assistant</h2>
            <p class="text-slate-300">Get intelligent answers to your programming questions with our AI-powered chat assistant.</p>
          </div>
          <div class="mt-auto pt-4">
            <a href="/chat" class="inline-block px-6 py-2 bg-neon-purple bg-opacity-20 hover:bg-opacity-40 border border-neon-purple text-neon-purple rounded-full transition-all">
              Get Started
            </a>
          </div>
        </div>
        
        <!-- Sandbox Card -->
        <div class="card-blur p-6 flex flex-col h-full text-center transition-all duration-300 hover:shadow-[0_0_15px_rgba(59,130,246,0.7)] hover:border-blue-500">
          <div class="mb-4">
            <h2 class="text-2xl font-semibold text-neon-blue mb-2">Sandbox</h2>
            <p class="text-slate-300">Experiment with code snippets in an isolated environment to test ideas quickly.</p>
          </div>
          <div class="mt-auto pt-4">
            <a href="/sandbox" class="inline-block px-6 py-2 bg-neon-blue bg-opacity-20 hover:bg-opacity-40 border border-neon-blue text-neon-blue rounded-full transition-all">
              Open Sandbox
            </a>
          </div>
        </div>
        
        <!-- Extension Card -->
        <div class="card-blur p-6 flex flex-col h-full text-center transition-all duration-300 hover:shadow-[0_0_15px_rgba(236,72,153,0.7)] hover:border-pink-500">
          <div class="mb-4">
            <h2 class="text-2xl font-semibold text-neon-pink mb-2">Extension</h2>
            <p class="text-slate-300">Enhance your development workflow with our powerful browser extension.</p>
          </div>
          <div class="mt-auto pt-4">
            <a href="/extension" class="inline-block px-6 py-2 bg-neon-pink bg-opacity-20 hover:bg-opacity-40 border border-neon-pink text-neon-pink rounded-full transition-all">
              Get Extension
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Crypto Video -->
<!-- <div class="w-full">
  <video class="w-full h-auto" autoplay loop muted playsinline>
    <source src="/crypto.webm" type="video/webm">
    Your browser does not support the video tag.
  </video>
</div> -->
  