document.addEventListener('DOMContentLoaded', () => {
    const editProfileBtn = document.getElementById('editProfileBtn');
    const profileInfo = document.querySelector('.profile-info');
    const profileEditForm = document.getElementById('profileEditForm');
    const cancelEditBtn = document.getElementById('cancelEditBtn');

    // Показать форму редактирования
    editProfileBtn.addEventListener('click', () => {
        profileInfo.classList.add('hidden');
        profileEditForm.classList.remove('hidden');
    });

    // Скрыть форму редактирования
    cancelEditBtn.addEventListener('click', () => {
        profileInfo.classList.remove('hidden');
        profileEditForm.classList.add('hidden');
    });

    // Здесь будет логика сохранения формы
    profileEditForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Данные сохранены! (в будущем здесь будет запрос на сервер)');
        profileInfo.classList.remove('hidden');
        profileEditForm.classList.add('hidden');
    });
});
