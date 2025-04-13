<script lang="ts">
    import Assistant from '$lib/components/chat/Assistant.svelte';
    import { onMount } from 'svelte';
    
    // Implement light effect
    onMount(() => {
      // Add mouse light effect for chat page
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

<section class="fixed top-0 left-0 w-full min-h-screen bg-dark">
  <div class="w-full max-w-7xl mx-auto px-4 pt-28">
    <div class="text-center mb-6">
      <h1 class="text-8xl font-bold gradient-text mb-4 glow">GPT Shield</h1>
      <p class="text-2xl text-slate-200 max-w-2xl mx-auto">Your data. Your AI. No Compromises.</p>
    </div>
    
    <div class="relative">
      <Assistant />
    </div>
  </div>
</section> 