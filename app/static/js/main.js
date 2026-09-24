// Grid switcher — toggles Bootstrap column class on each item
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

// Login / Register toggle
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

// Bootstrap-native validation
document.querySelectorAll('.needs-validation').forEach(form => {
  form.addEventListener('submit', function (e) {
    if (!form.checkValidity()) {
      e.preventDefault();
      e.stopPropagation();
    }
    form.classList.add('was-validated');
  });
});

// Comment: optimistic append, then real POST persists it
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
