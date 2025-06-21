// Переключение темы
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Проверка сохраненной темы
if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark-theme');
}

themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-theme');
    
    // Сохранение выбора темы
    if (body.classList.contains('dark-theme')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    // Анимация кнопок "Откликнуться"
    const applyButtons = document.querySelectorAll('.apply-btn');
    applyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const originalHTML = this.innerHTML;
            
            // Проверяем, чтобы не было повторного нажатия
            if (this.classList.contains('clicked')) {
                return;
            }
            
            this.classList.add('clicked');
            this.innerHTML = '<i class="fas fa-check"></i> Отклик отправлен';
            this.style.background = '#2ecc71';
            
            setTimeout(() => {
                this.innerHTML = originalHTML;
                this.style.background = ''; // Возвращаем исходный цвет
                this.classList.remove('clicked');
            }, 2000);
        });
    });
});
