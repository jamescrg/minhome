// Content script to handle closing the popup from the webpage
console.log('Content script loaded');

// Listen for messages from the webpage
window.addEventListener('message', function(event) {
  console.log('Content script received message:', event.data);

  if (event.data.action === 'closePopup') {
    console.log('Forwarding close request to background script');

    // Forward the message to the background script
    if (typeof browser !== 'undefined' && browser.runtime) {
      browser.runtime.sendMessage({action: 'closePopup'});
    } else if (typeof chrome !== 'undefined' && chrome.runtime) {
      chrome.runtime.sendMessage({action: 'closePopup'});
    }
  }
});

// Inject a function into the page to send messages to this content script
const script = document.createElement('script');
script.textContent = `
  window.closeExtensionPopup = function() {
    console.log('Sending close message to content script');
    window.postMessage({action: 'closePopup'}, '*');
  };
`;
document.documentElement.appendChild(script);
script.remove();
