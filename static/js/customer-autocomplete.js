/* ═══════════════════════════════════════════════════════════
   Lophoro IMS — Customer search-as-you-type for the order form
   ═══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {
  var nameInput = document.getElementById('customer_name');
  var idInput = document.getElementById('customer_id');
  var suggestBox = document.getElementById('customer-suggestions');
  if (!nameInput || !idInput || !suggestBox) return;

  var phoneInput = document.getElementById('customer_phone');
  var emailInput = document.getElementById('customer_email');
  var addressInput = document.getElementById('customer_address');
  var panInput = document.getElementById('customer_pan');
  var searchUrl = nameInput.dataset.searchUrl || '/orders/customers/search/';

  var debounceTimer = null;

  function clearSelection() {
    idInput.value = '';
  }

  function hideResults() {
    suggestBox.style.display = 'none';
    suggestBox.innerHTML = '';
  }

  function selectCustomer(c) {
    idInput.value = c.id;
    nameInput.value = c.name;
    if (phoneInput) phoneInput.value = c.phone || '';
    if (emailInput) emailInput.value = c.email || '';
    if (addressInput) addressInput.value = c.address || '';
    if (panInput) panInput.value = c.buyer_pan || '';
    hideResults();
  }

  function renderResults(results) {
    suggestBox.innerHTML = '';
    if (!results.length) {
      hideResults();
      return;
    }
    results.forEach(function (c) {
      var item = document.createElement('div');
      item.className = 'customer-suggestion-item';
      item.textContent = c.name + (c.phone ? ' · ' + c.phone : '');
      item.addEventListener('mousedown', function (e) {
        e.preventDefault();
        selectCustomer(c);
      });
      suggestBox.appendChild(item);
    });
    suggestBox.style.display = 'block';
  }

  function search(q) {
    fetch(searchUrl + '?q=' + encodeURIComponent(q))
      .then(function (r) { return r.json(); })
      .then(function (data) { renderResults(data.results || []); })
      .catch(function () { hideResults(); });
  }

  function onQueryInput(q) {
    clearSelection();
    clearTimeout(debounceTimer);
    if (q.length < 2) {
      hideResults();
      return;
    }
    debounceTimer = setTimeout(function () { search(q); }, 250);
  }

  nameInput.addEventListener('input', function () {
    onQueryInput(nameInput.value.trim());
  });

  if (phoneInput) {
    phoneInput.addEventListener('input', function () {
      onQueryInput(phoneInput.value.trim());
    });
  }

  document.addEventListener('click', function (e) {
    if (e.target !== nameInput && e.target !== phoneInput && !suggestBox.contains(e.target)) {
      hideResults();
    }
  });
});
