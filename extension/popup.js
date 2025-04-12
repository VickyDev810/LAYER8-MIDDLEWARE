document.addEventListener('DOMContentLoaded', function() {
  // Extension toggle elements
  const enableToggle = document.getElementById('enableToggle');
  const statusText = document.getElementById('statusText');
  
  // API settings elements
  const apiUrlInput = document.getElementById('apiUrl');
  const saveSettingsBtn = document.getElementById('saveSettings');
  const saveStatus = document.getElementById('saveStatus');
  
  // Load current settings from storage
  chrome.storage.sync.get(['enabled', 'apiUrl'], function(data) {
    // Load extension enabled state
    const isEnabled = data.enabled !== undefined ? data.enabled : true;
    enableToggle.checked = isEnabled;
    updateStatusText(isEnabled);
    
    // Load API URL
    const apiUrl = data.apiUrl || config.API_URL;
    apiUrlInput.value = apiUrl;
  });
  
  // Add toggle event listener
  enableToggle.addEventListener('change', function() {
    const isEnabled = enableToggle.checked;
    
    // Save to storage
    chrome.storage.sync.set({enabled: isEnabled}, function() {
      updateStatusText(isEnabled);
      console.log(`Extension ${isEnabled ? 'enabled' : 'disabled'}`);
    });
  });
  
  // Save API URL settings
  saveSettingsBtn.addEventListener('click', function() {
    const newApiUrl = apiUrlInput.value.trim();
    
    if (!newApiUrl) {
      showSaveStatus('Please enter a valid API URL', false);
      return;
    }
    
    // Validate URL format
    try {
      new URL(newApiUrl);
    } catch (e) {
      showSaveStatus('Please enter a valid URL with http:// or https://', false);
      return;
    }
    
    // Save to storage
    chrome.storage.sync.set({apiUrl: newApiUrl}, function() {
      console.log('API URL saved:', newApiUrl);
      showSaveStatus('Settings saved successfully!', true);
    });
  });
  
  // Update the status text based on enabled state
  function updateStatusText(isEnabled) {
    statusText.textContent = isEnabled ? 'Enabled' : 'Disabled';
    statusText.style.color = isEnabled ? '#10a37f' : '#d9534f';
  }
  
  // Display save status message
  function showSaveStatus(message, success) {
    saveStatus.textContent = message;
    saveStatus.style.color = success ? '#10a37f' : '#d9534f';
    saveStatus.classList.add('show');
    
    setTimeout(() => {
      saveStatus.classList.remove('show');
    }, 3000);
  }
});