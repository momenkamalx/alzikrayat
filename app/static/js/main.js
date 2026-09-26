
(function () {
  const switcher = document.getElementById('layoutSwitcher');
  const grid = document.getElementById('photoGrid');
  if (!switcher || !grid) return;
  switcher.addEventListener('click', function (e) {
    const btn = e.target.closest('button[data-cols]');
    if (!btn) return;
    const colClass = 'col-md-' + btn.dataset.cols;
    grid.querySelectorAll('.gallery-item').forEach(item => {
      item.className = item.className.replace(/col-md-\d+/, colClass) + ' gallery-item';
      item.classList.add(colClass);
    });
    switcher.querySelectorAll('button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
})();

// Login / Register 
(function () {
  const loginForm = document.getElementById('loginForm');
  const regForm = document.getElementById('registerForm');
  const title = document.getElementById('formTitle');
  const sub = document.getElementById('formSub');
  const toReg = document.getElementById('switchLoginToReg');
  const toLogin = document.getElementById('switchRegToLogin');
  if (!loginForm || !regForm) return;

  function showRegister() {
    loginForm.classList.add('d-none');
    regForm.classList.remove('d-none');
    toReg.classList.add('d-none');
    toLogin.classList.remove('d-none');
    title.textContent = 'Create your account';
    sub.textContent = 'Join Alzikrayat in a few seconds.';
  }
  function showLogin() {
    regForm.classList.add('d-none');
    loginForm.classList.remove('d-none');
    toLogin.classList.add('d-none');
    toReg.classList.remove('d-none');
    title.textContent = 'Welcome back';
    sub.textContent = 'Log in to your Alzikrayat account.';
  }
  document.querySelectorAll('[data-mode]').forEach(a => {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      this.dataset.mode === 'register' ? showRegister() : showLogin();
    });
  });
})();

// Bootstrap
document.querySelectorAll('.needs-validation').forEach(form => {
  form.addEventListener('submit', function (e) {
    if (!form.checkValidity()) {
      e.preventDefault();
      e.stopPropagation();
    }
    form.classList.add('was-validated');
  });
});


(function () {
  const form = document.getElementById('commentForm');
  const list = document.getElementById('commentList');
  if (!form || !list) return;

  form.addEventListener('submit', function () {
    const input = form.querySelector('input[name="comment"]');
    const text = input.value.trim();
    if (!text) return;

    const row = document.createElement('div');
    row.className = 'd-flex gap-2 mb-3';
    row.innerHTML =
      '<span class="user-avatar">Y</span>' +
      '<div class="card px-3 py-2 flex-grow-1">' +
        '<div class="small fw-semibold">You <span class="text-body-secondary fw-normal">just now</span></div>' +
        '<div class="small"></div>' +
      '</div>';
    row.querySelector('.small:last-child').textContent = text; // textContent — safe from injection
    list.appendChild(row);
  });
})();
// mention autocomplete
(function () {
  const input = document.getElementById('commentInput');
  const list = document.getElementById('mentionList');
  const dataEl = document.getElementById('usersData');
  if (!input || !list || !dataEl) return;

  const users = JSON.parse(dataEl.textContent);

  function showMatches(query, cursorPos) {
    const matches = users.filter(u => u.name.toLowerCase().includes(query));
    list.innerHTML = matches.map(u => `<button type="button" class="list-group-item list-group-item-action">@${u.name}</button>`).join('');

    list.querySelectorAll('button').forEach((btn, i) => {
      btn.addEventListener('click', () => {
        const name = matches[i].name.replace(/\s+/g, '');
        input.value = input.value.slice(0, cursorPos).replace(/@\w*$/, '@' + name + ' ') + input.value.slice(cursorPos);
        list.classList.add('d-none');
        input.focus();
      });
    });
    list.classList.toggle('d-none', matches.length === 0);
  }

  input.addEventListener('input', () => {
    const cursorPos = input.selectionStart;
    const match = input.value.slice(0, cursorPos).match(/@(\w*)$/);
    match ? showMatches(match[1].toLowerCase(), cursorPos) : list.classList.add('d-none');
  });

  document.addEventListener('click', e => {
    if (e.target !== input) list.classList.add('d-none');
  });
})();