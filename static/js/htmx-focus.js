(function() {
  let focusedInputId = null;

  document.body.addEventListener('htmx:beforeSwap', function(evt) {
    const activeElement = document.activeElement;
    // Only save focus if the request was triggered by the input itself
    // (e.g. typing triggered a swap), not by clicking something else
    const requestElt = evt.detail.requestConfig && evt.detail.requestConfig.elt;
    if (activeElement && activeElement.tagName === 'INPUT' && activeElement.id) {
      const target = evt.detail.target;
      if (target.contains(activeElement) && activeElement === requestElt) {
        focusedInputId = activeElement.id;
      }
    }
  });

  document.body.addEventListener('htmx:afterSwap', function(evt) {
    if (focusedInputId) {
      const input = document.getElementById(focusedInputId);
      if (input) {
        input.focus({ preventScroll: true });
        input.setSelectionRange(input.value.length, input.value.length);
      }
      focusedInputId = null;
    }
  });
})();
