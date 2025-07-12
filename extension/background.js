// Background script for the extension

// Store popup window ID for closing
let popupWindowId = null;

// Firefox uses 'browser' API, Chrome uses 'chrome' API
const api = typeof browser !== 'undefined' ? browser : chrome;

// Function to get the configured domain
function getFavoritesDomain(callback) {
  api.storage.sync.get(['favoritesDomain'], function(result) {
    const domain = (result && result.favoritesDomain) || 'minhome.app';
    callback(domain);
  });
}

// Handle browser action click
api.browserAction.onClicked.addListener(function(tab) {
  // Get the current tab's title and URL
  const title = tab.title || tab.url;
  const url = tab.url;

  // Get current window to position popup relative to it
  api.windows.getCurrent(function(currentWindow) {
    // Calculate popup position on the right side of current window
    const popupWidth = 450;
    const popupHeight = 550;
    const left = Math.round(currentWindow.left + currentWindow.width - popupWidth - 20); // 20px margin from edge
    const top = Math.round(currentWindow.top + (currentWindow.height - popupHeight) / 2);

    // Get the configured domain and open popup
    getFavoritesDomain(function(domain) {
      const popupUrl = `https://${domain}/favorites/extension?name=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`;

      if (typeof browser !== 'undefined') {
        // Firefox - uses promises
        api.windows.create({
          url: popupUrl,
          type: 'popup',
          width: popupWidth,
          height: popupHeight,
          left: left,
          top: top,
          focused: true
        }).then(function(window) {
          popupWindowId = window.id;
          console.log('Created popup window:', window.id);
        });
      } else {
        // Chrome - uses callbacks
        api.windows.create({
          url: popupUrl,
          type: 'popup',
          width: popupWidth,
          height: popupHeight,
          left: left,
          top: top,
          focused: true
        }, function(window) {
          popupWindowId = window.id;
          console.log('Created popup window:', window.id);
        });
      }
    });
  });
});

// Add context menu item
api.runtime.onInstalled.addListener(function() {
  api.contextMenus.create({
    id: 'add-to-favorites',
    title: 'Add to Favorites',
    contexts: ['page', 'link']
  });

  console.log('Add to Favorites extension installed');
});

// Handle context menu clicks
api.contextMenus.onClicked.addListener(function(info, tab) {
  if (info.menuItemId === 'add-to-favorites') {
    const title = info.linkText || tab.title || tab.url;
    const url = info.linkUrl || tab.url;

    // Get current window to position popup relative to it
    api.windows.getCurrent(function(currentWindow) {
      // Calculate popup position on the right side of current window
      const popupWidth = 450;
      const popupHeight = 550;
      const left = Math.round(currentWindow.left + currentWindow.width - popupWidth - 20); // 20px margin from edge
      const top = Math.round(currentWindow.top + (currentWindow.height - popupHeight) / 2);

      // Get the configured domain and open popup
      getFavoritesDomain(function(domain) {
        const popupUrl = `https://${domain}/favorites/extension?name=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`;

        if (typeof browser !== 'undefined') {
          // Firefox - uses promises
          api.windows.create({
            url: popupUrl,
            type: 'popup',
            width: popupWidth,
            height: popupHeight,
            left: left,
            top: top,
            focused: true
          }).then(function(window) {
            popupWindowId = window.id;
            console.log('Created popup window from context menu:', window.id);
          });
        } else {
          // Chrome - uses callbacks
          api.windows.create({
            url: popupUrl,
            type: 'popup',
            width: popupWidth,
            height: popupHeight,
            left: left,
            top: top,
            focused: true
          }, function(window) {
            popupWindowId = window.id;
            console.log('Created popup window from context menu:', window.id);
          });
        }
      });
    });
  }
});

// Listen for messages from the popup to close it

api.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  console.log('Background script received message:', request);
  console.log('Current popupWindowId:', popupWindowId);

  if (request.action === 'closePopup') {
    if (popupWindowId) {
      console.log('Attempting to close popup window:', popupWindowId);

      // Firefox uses promises, Chrome uses callbacks
      if (typeof browser !== 'undefined') {
        // Firefox
        api.windows.remove(popupWindowId).then(() => {
          console.log('Closed popup window:', popupWindowId);
          popupWindowId = null;
        }).catch(err => {
          console.error('Failed to close popup:', err);
        });
      } else {
        // Chrome
        api.windows.remove(popupWindowId, function() {
          console.log('Closed popup window:', popupWindowId);
          popupWindowId = null;
        });
      }
    } else {
      console.log('No popup window ID stored');
    }
  }
});
