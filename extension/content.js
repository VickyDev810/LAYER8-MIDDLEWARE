console.log("AI Prompt Privacy Protector content script loaded.");

// EXTENSION CHECK
chrome.storage.sync.get("enabled", function (data) {
  const isEnabled =
    data.enabled !== undefined ? data.enabled : config.defaults.enabled;

  if (isEnabled) {
    console.log("AI Prompt Privacy Protector is enabled and running.");
    initializeExtension();
  } else {
    console.log("AI Prompt Privacy Protector is disabled.");
  }
});

// START EXTESNION

function initializeExtension() {
  const API_URL = config.API_URL;

  // Detect which AI
  const isGemini = window.location.hostname.includes(config.platforms.GEMINI);
  const isChatGPT = window.location.hostname.includes(config.platforms.CHATGPT);
  const isGrok = window.location.hostname.includes(config.platforms.GROK);

  console.log(
    `Detected AI platform: ${
      isGemini ? "Gemini" : isChatGPT ? "ChatGPT" : isGrok ? "Grok" : "Unknown"
    }`
  );

  /**
   * Process a prompt by sending it to the API
   * @param {string} prompt - The original user prompt
   * @returns {Object}
   */

  // PROCESS PROMPT AND API

  async function processPrompt(prompt) {
    try {
      // URL encode the prompt text
      const encodedPrompt = encodeURIComponent(prompt);
      // Add the correct /anonymize/ path
      const requestUrl = `${API_URL}/anonymize/${encodedPrompt}`;

      console.log("Making API request to:", requestUrl);

      const response = await fetch(requestUrl, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error(`API returned status ${response.status}`);
      }

      const result = await response.json();
      console.log("API response:", result);

      return {
        encryptedPrompt: result.anonymized_text || prompt,
        originalData: result.sensitivity_report || {},
      };
    } catch (error) {
      console.error(`Error calling API: ${error.message}`);
      return { encryptedPrompt: prompt, originalData: {} };
    }
  }

  // SET UP EXTENSION BUTTON
  function setupPromptListener() {
    if (isGemini) {
      setupGeminiInterface();
    } else if (isChatGPT) {
      setupChatGPTInterface();
    } else if (isGrok) {
      setupGrokInterface();
    }
  }

  // FOR CHATGPT UI
  function setupChatGPTInterface() {
    const promptTextarea = document.getElementById("prompt-textarea");
    if (!promptTextarea) return;

    console.log("ChatGPT prompt textarea found");

    // Create encrypt button with styling
    const encryptButton = createEncryptButton();

    // Find the parent container and add the button
    attachButtonToChatGPTInterface(promptTextarea, encryptButton);

    // Set up event listeners and button behavior
    setupButtonBehavior(promptTextarea, encryptButton);

    // Initial check for existing content
    updateButtonVisibility(promptTextarea, encryptButton);

    // We found the textarea, no need to keep observing
    observer.disconnect();
  }

  // FOR GEMINI UI
  function setupGeminiInterface() {
    // Gemini uses a contentEditable div inside rich-textarea
    const promptTextarea = document.querySelector(
      '.ql-editor[contenteditable="true"][data-placeholder="Ask Gemini"]'
    );
    if (!promptTextarea) return;

    console.log("Gemini prompt textarea found");

    // Create encrypt button with styling adjusted for Gemini
    const encryptButton = createEncryptButton(true);

    // Find the parent container and add the button
    attachButtonToGeminiInterface(promptTextarea, encryptButton);

    // Set up event listeners and button behavior
    setupButtonBehavior(promptTextarea, encryptButton);

    // Initial check for existing content
    updateButtonVisibility(promptTextarea, encryptButton);

    // We found the textarea, no need to keep observing
    observer.disconnect();
  }

  // FOR GROK UI
  function setupGrokInterface() {
    // Grok uses a textarea inside a query-bar class
    const promptTextarea = document.querySelector(
      '.query-bar textarea[aria-label="Ask Grok anything"]'
    );
    if (!promptTextarea) return;

    console.log("Grok prompt textarea found");

    // Create encrypt button with styling adjusted for Grok
    const encryptButton = createEncryptButton(false, true);

    // Find the parent container and add the button
    attachButtonToGrokInterface(promptTextarea, encryptButton);

    // Set up event listeners and button behavior
    setupButtonBehavior(promptTextarea, encryptButton);

    // Initial check for existing content
    updateButtonVisibility(promptTextarea, encryptButton);

    observer.disconnect();
  }

  // STYLING FOR ENCRYPT BUTTON

  /**
   * Creates and styles the encrypt button
   * @param {boolean} isGemini - Whether this button is for Gemini interface
   * @param {boolean} isGrok - Whether this button is for Grok interface
   */
  function createEncryptButton(isGemini = false, isGrok = false) {
    const encryptButton = document.createElement("button");
    encryptButton.textContent = "Encrypt";
    encryptButton.id = "encrypt-button";
    encryptButton.type = "button";
    encryptButton.className = "encrypt-button";

    if (isGemini) {
      // Gemini-specific styling
      encryptButton.style.cssText = `
        display: inline-flex;
        height: 32px;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        background-color: transparent;
        color: rgb(26, 232, 150);
        font-size: 14px;
        font-weight: 500;
        padding: 0 12px;
        margin-right: 8px;
        cursor: pointer;
        transition: all 0.2s;
      `;

      // Hover effects for Gemini
      encryptButton.onmouseover = () => {
        encryptButton.style.backgroundColor = "rgba(26, 232, 174, 0.1)";
      };
      encryptButton.onmouseout = () => {
        encryptButton.style.backgroundColor = "transparent";
      };
    } else if (isGrok) {
      // Grok-specific styling - matches the Grok UI theme
      encryptButton.style.cssText = `
        display: inline-flex;
        height: 36px;
        align-items: center;
        justify-content: center;
        border-radius: 18px;
        border: 1px solid var(--toggle-border, rgba(0, 0, 0, 0.1));
        background-color: transparent;
        color: rgb(26, 232, 150);
        font-size: 14px;
        font-weight: 500;
        padding: 0 14px;
        margin-right: 6px;
        cursor: pointer;
        transition: all 0.2s;
      `;

      // Hover effects for Grok
      encryptButton.onmouseover = () => {
        encryptButton.style.backgroundColor = "rgba(26, 232, 174, 0.1)";
      };
      encryptButton.onmouseout = () => {
        encryptButton.style.backgroundColor = "transparent";
      };
    } else {
      // ChatGPT styling (default)
      encryptButton.style.cssText = `
        display: inline-flex;
        height: 28px;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        border: 1px solid rgba(0,0,0,0.1);
        background-color: transparent;
        color: #10a37f;
        font-size: 13px;
        font-weight: 500;
        padding: 0 12px;
        margin-right: 6px;
        cursor: pointer;
        transition: all 0.2s;
      `;

      // Hover effects for ChatGPT
      encryptButton.onmouseover = () => {
        encryptButton.style.backgroundColor = "rgba(16, 163, 127, 0.1)";
      };
      encryptButton.onmouseout = () => {
        encryptButton.style.backgroundColor = "transparent";
      };
    }

    return encryptButton;
  }

  // ATtachs the button to GPT interface

  function attachButtonToChatGPTInterface(promptTextarea, encryptButton) {
    // Look for the toolbar where other buttons are located
    const toolbar =
      document.querySelector(".flex.items-center.gap-2.overflow-x-auto") ||
      document.querySelector(".flex.items-center");

    if (toolbar) {
      // Insert our button at the beginning of the toolbar
      toolbar.insertBefore(encryptButton, toolbar.firstChild);
      return;
    }
  }

  // Attaches the button to the Gemini interface

  function attachButtonToGeminiInterface(promptTextarea, encryptButton) {
    // Alternative: add near the mic/send buttons
    const actionsWrapper = document.querySelector(".trailing-actions-wrapper");
    if (actionsWrapper) {
      // Create a container similar to other Gemini buttons
      const buttonContainer = document.createElement("div");
      buttonContainer.style.cssText = `
        display: inline-flex;
        margin-right: 8px;
      `;
      buttonContainer.appendChild(encryptButton);
      actionsWrapper.insertBefore(buttonContainer, actionsWrapper.firstChild);
      return;
    }
  }

  // Attaches the button to the Grok interface

  function attachButtonToGrokInterface(promptTextarea, encryptButton) {
    // Try to find the buttons container in Grok's UI
    const buttonsContainer = promptTextarea
      .closest(".query-bar")
      ?.querySelector(".flex.gap-1\\.5.max-w-full");

    if (buttonsContainer) {
      // Insert our button at the beginning of the toolbar
      buttonsContainer.insertBefore(encryptButton, buttonsContainer.firstChild);
      return;
    }

    // Find the DeepSearch button to place ours next to it
    const deepSearchButton = document.querySelector(
      'button[aria-label="DeepSearch"]'
    );
    if (deepSearchButton && deepSearchButton.parentNode) {
      deepSearchButton.parentNode.insertBefore(encryptButton, deepSearchButton);
      return;
    }
  }

  // TEXT AREA EVENTLISTENERS

  function setupButtonBehavior(promptTextarea, encryptButton) {
    // Function to update button visibility based on textarea content
    const updateVisibility = () =>
      updateButtonVisibility(promptTextarea, encryptButton);

    // Add event listeners for both typing and pasting
    promptTextarea.addEventListener("input", updateVisibility);
    promptTextarea.addEventListener("paste", () =>
      setTimeout(updateVisibility, 10)
    );

    // Platform-specific event handling
    if (isGemini) {
      promptTextarea.addEventListener("blur", updateVisibility);
      promptTextarea.addEventListener("focus", updateVisibility);
    } else if (isGrok) {
      // Add specific event listeners for Grok if needed
      promptTextarea.addEventListener("blur", updateVisibility);
      promptTextarea.addEventListener("focus", updateVisibility);
    }

    // ENCRYPT BUTTON HANDLE SUBMIT AND
    encryptButton.addEventListener("click", async (event) => {
      event.preventDefault();
      event.stopPropagation();

      let originalPrompt;

      if (isGemini) {
        originalPrompt = promptTextarea.textContent || "";
      } else if (isGrok) {
        originalPrompt = promptTextarea.value || "";
      } else {
        originalPrompt =
          promptTextarea.value || promptTextarea.textContent || "";
      }

      if (!originalPrompt) return;

      const result = await processPrompt(originalPrompt);

      if (result && Object.keys(result.originalData).length > 0) {
        if (isGemini) {
          // Replace the content for Gemini
          promptTextarea.textContent = result.encryptedPrompt;

          // Trigger input event for Gemini
          const inputEvent = new InputEvent("input", {
            bubbles: true,
            cancelable: true,
          });
          promptTextarea.dispatchEvent(inputEvent);
        } else if (isGrok) {
          // Replace textarea content for Grok
          promptTextarea.value = result.encryptedPrompt;

          // Trigger input event for Grok
          const inputEvent = new InputEvent("input", {
            bubbles: true,
            cancelable: true,
            composed: true,
          });
          promptTextarea.dispatchEvent(inputEvent);

          // Force resize of textarea if needed
          if (promptTextarea.style.height) {
            promptTextarea.style.height = "auto";
            promptTextarea.style.height = promptTextarea.scrollHeight + "px";
          }
        } else {
          // Replace textarea content with encrypted version for ChatGPT
          promptTextarea.value = result.encryptedPrompt;
          promptTextarea.textContent = result.encryptedPrompt;

          // Trigger input event to update ChatGPT's internal state
          setTimeout(() => {
            const inputEvent = new InputEvent("input", {
              bubbles: true,
              cancelable: true,
              composed: true,
              inputType: "insertText",
            });
            promptTextarea.dispatchEvent(inputEvent);
          }, 10);
        }
      }
    });
  }

  // ONLY SHOW BUTTON WHEN TEXT PRESENT IN THE TEXTAREA

  function updateButtonVisibility(promptTextarea, encryptButton) {
    let hasContent;

    if (isGemini) {
      // For Gemini, check the textContent
      hasContent = (promptTextarea.textContent || "").trim().length > 0;
      // Check if the div only contains a <br> but no actual text
      if (
        (hasContent && promptTextarea.innerHTML.trim() === "<br>") ||
        promptTextarea.innerHTML.trim().includes("data-placeholder")
      ) {
        hasContent = false;
      }
    } else if (isGrok) {
      // For Grok, check the textarea value
      hasContent = (promptTextarea.value || "").trim().length > 0;
    } else {
      // For ChatGPT check both value and textContent
      hasContent =
        (promptTextarea.value || promptTextarea.textContent || "").trim()
          .length > 0;
    }

    encryptButton.style.display = hasContent ? "block" : "none";
  }

  // Create a Mutation Observer to find the textarea when it loads
  const observer = new MutationObserver(() => {
    setupPromptListener();
  });

  observer.observe(document.body, { childList: true, subtree: true });

  // Intercept fetch requests to anonymize data before sending to API
  const originalFetch = window.fetch;
  window.fetch = async (...args) => {
    const url = args[0];
    const options = args[1] || {};

    // Process ChatGPT API requests
    if (
      isChatGPT &&
      url.includes("chatgpt.com/backend-api/conversation") &&
      typeof options.body === "string"
    ) {
      try {
        const parsedBody = JSON.parse(options.body);

        // Handle direct prompts
        if (parsedBody && typeof parsedBody.prompt === "string") {
          const { encryptedPrompt, originalData } = await processPrompt(
            parsedBody.prompt
          );
          if (Object.keys(originalData).length > 0) {
            parsedBody.prompt = encryptedPrompt;
            options.body = JSON.stringify(parsedBody);
          }
        }
        // Handle message arrays
        else if (parsedBody && Array.isArray(parsedBody.messages)) {
          for (const message of parsedBody.messages) {
            if (message && typeof message.content === "string") {
              const { encryptedPrompt, originalData } = await processPrompt(
                message.content
              );
              if (Object.keys(originalData).length > 0) {
                message.content = encryptedPrompt;
                options.body = JSON.stringify(parsedBody);
                break;
              }
            }
          }
        }
      } catch (e) {
        console.error("Error processing ChatGPT fetch request:", e);
      }
    }

    // Process Gemini API requests
    if (
      isGemini &&
      (url.includes("generativelanguage.googleapis.com") ||
        url.includes("gemini.google.com/api"))
    ) {
      try {
        // Only process if it's a POST request with body
        if (options.method === "POST" && options.body) {
          const bodyContent =
            typeof options.body === "string"
              ? JSON.parse(options.body)
              : options.body;

          // Check for common Gemini API structures
          if (bodyContent.contents) {
            // Handle array of contents
            for (const content of bodyContent.contents) {
              if (content.parts) {
                for (const part of content.parts) {
                  if (part.text) {
                    const { encryptedPrompt, originalData } =
                      await processPrompt(part.text);
                    if (Object.keys(originalData).length > 0) {
                      part.text = encryptedPrompt;
                      options.body = JSON.stringify(bodyContent);
                    }
                  }
                }
              }
            }
          } else if (bodyContent.prompt && bodyContent.prompt.text) {
            // Handle direct text prompts
            const { encryptedPrompt, originalData } = await processPrompt(
              bodyContent.prompt.text
            );
            if (Object.keys(originalData).length > 0) {
              bodyContent.prompt.text = encryptedPrompt;
              options.body = JSON.stringify(bodyContent);
            }
          }
        }
      } catch (e) {
        console.error("Error processing Gemini fetch request:", e);
      }
    }

    // Process Grok API requests
    if (
      isGrok &&
      (url.includes("api.x.ai") ||
        url.includes("grok.x.ai/api") ||
        url.includes("grok.com/api"))
    ) {
      try {
        // Only process if it's a POST request with body
        if (options.method === "POST" && options.body) {
          const bodyContent =
            typeof options.body === "string"
              ? JSON.parse(options.body)
              : options.body;

          // Check for common Grok API structures (may need adjusting based on actual API)
          if (bodyContent.message) {
            const { encryptedPrompt, originalData } = await processPrompt(
              bodyContent.message
            );
            if (Object.keys(originalData).length > 0) {
              bodyContent.message = encryptedPrompt;
              options.body = JSON.stringify(bodyContent);
            }
          } else if (
            bodyContent.messages &&
            Array.isArray(bodyContent.messages)
          ) {
            // Handle message array structure
            for (const message of bodyContent.messages) {
              if (message && typeof message.content === "string") {
                const { encryptedPrompt, originalData } = await processPrompt(
                  message.content
                );
                if (Object.keys(originalData).length > 0) {
                  message.content = encryptedPrompt;
                  options.body = JSON.stringify(bodyContent);
                  break;
                }
              }
            }
          } else if (bodyContent.prompt) {
            // Handle prompt property
            const { encryptedPrompt, originalData } = await processPrompt(
              bodyContent.prompt
            );
            if (Object.keys(originalData).length > 0) {
              bodyContent.prompt = encryptedPrompt;
              options.body = JSON.stringify(bodyContent);
            }
          }
        }
      } catch (e) {
        console.error("Error processing Grok fetch request:", e);
      }
    }

    return originalFetch.apply(this, args);
  };
}
