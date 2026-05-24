// ===== Theme Toggle =====
function getTheme() {
    return localStorage.getItem('theme') || 'dark';
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = theme === 'dark' ? '🌙' : '☀️';
}

function toggleTheme() {
    const current = getTheme();
    const next = current === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', next);
    applyTheme(next);
}

// Apply theme on load
applyTheme(getTheme());

// ===== Mobile Menu =====
function toggleMenu() {
    document.getElementById('navLinks').classList.toggle('open');
}

// ===== Shared Utilities =====
function showError(msg) {
    const el = document.getElementById('errorMsg');
    if (el) {
        el.textContent = '⚠️ ' + msg;
        el.classList.add('visible');
    }
}

function hideError() {
    const el = document.getElementById('errorMsg');
    if (el) el.classList.remove('visible');
}

function showLoading(show) {
    const spinner = document.getElementById('btnSpinner');
    if (spinner) spinner.style.display = show ? 'inline-block' : 'none';
}

function toggleSteps() {
    const list = document.getElementById('stepsList');
    const icon = document.getElementById('toggleIcon');
    if (!list) return;
    if (list.style.display === 'none') {
        list.style.display = 'flex';
        if (icon) icon.classList.add('open');
    } else {
        list.style.display = 'none';
        if (icon) icon.classList.remove('open');
    }
}

function copyResult() {
    const text = document.getElementById('resultText');
    if (text) {
        navigator.clipboard.writeText(text.textContent).then(() => {
            const btn = document.querySelector('.copy-btn');
            if (btn) {
                btn.textContent = '✓';
                setTimeout(() => btn.textContent = '📋', 1500);
            }
        });
    }
}

function escapeHtml(str) {
    if (typeof str !== 'string') return str;
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}
