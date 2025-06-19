// Функционал профиля
const profileBtn = document.getElementById('profileBtn');
const profileMenu = document.getElementById('profileMenu');

// Показ/скрытие меню профиля
profileBtn.addEventListener('click', () => {
    profileMenu.classList.toggle('hidden');
});

// Закрытие меню при клике вне его
document.addEventListener('click', (e) => {
    if (!profileBtn.contains(e.target) && !profileMenu.contains(e.target)) {
        profileMenu.classList.add('hidden');
    }
});


// Функционал переключения темы
const themeToggle = document.querySelector('[data-theme-toggle]');

// Проверяем сохраненную тему
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    themeToggle.checked = true;
}

// Обработчик переключения темы
themeToggle.addEventListener('change', () => {
    if (themeToggle.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
    }
}); 