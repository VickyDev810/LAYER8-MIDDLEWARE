<script lang="ts">
    import '../app.css'; // Import Tailwind styles
    import { onMount } from 'svelte';
    
    onMount(() => {
      // Add mouse light effect
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
    });
  </script>
  
  <!-- Detached Navbar -->
  <div class="fixed top-4 left-0 right-0 z-40 flex justify-center">
    <nav class="navbar-blur py-3 px-8 rounded-full mx-auto shadow-xl border border-purple-700 border-opacity-30 max-w-3xl">
      <div class="flex justify-between items-center">
        <div class="flex items-center space-x-2">
        </div>
        <div class="flex space-x-8">
          <a href="/" class="text-purple-200 hover:text-neon-purple transition-colors">Home</a>
          <a href="/chat" class="text-purple-200 hover:text-neon-purple transition-colors">Chat</a>
          <a href="/sandbox" class="text-purple-200 hover:text-neon-purple transition-colors">Sandbox</a>
          <a href="/extension" class="text-purple-200 hover:text-neon-purple transition-colors">Extension</a>
          <a href="/about" class="text-purple-200 hover:text-neon-purple transition-colors">About</a>
        </div>
      </div>
    </nav>
  </div>
  
  <main class="pt-24">
    <slot />
  </main>
  