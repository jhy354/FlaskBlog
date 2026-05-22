/* ========== Theme Toggle ========== */
const THEME_KEY = 'blog-theme';
const html = document.documentElement;
const themeBtn = document.getElementById('themeToggle');
const sunIcon = document.getElementById('sunIcon');
const moonIcon = document.getElementById('moonIcon');

function setTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    if (sunIcon && moonIcon) {
        sunIcon.style.display = theme === 'dark' ? 'none' : 'block';
        moonIcon.style.display = theme === 'dark' ? 'block' : 'none';
    }
}

const stored = localStorage.getItem(THEME_KEY);
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
setTheme(stored || (prefersDark ? 'dark' : 'light'));

if (themeBtn) {
    themeBtn.addEventListener('click', () => {
        setTheme(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
}

/* ========== Back to Top ========== */
const backTop = document.getElementById('backTop');
if (backTop) {
    const toggle = () => backTop.classList.toggle('hide', window.scrollY < 200);
    toggle();
    window.addEventListener('scroll', toggle, { passive: true });
    backTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

/* ========== Back to Home ========== */
const backHome = document.getElementById('backHome');
if (backHome) {
    backHome.addEventListener('click', () => {
        window.location.href = '/';
    });
}

/* ========== Reports Category Filter ========== */
const filterBtns = document.querySelectorAll('.filter-btn');
const reportCards = document.querySelectorAll('.report-card');

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        reportCards.forEach(card => {
            card.style.display = (filter === 'all' || card.dataset.course === filter) ? 'flex' : 'none';
        });
    });
});
