document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Кадровая система загружена');
    
    // 1. Подтверждение удаления сотрудника
    const deleteLinks = document.querySelectorAll('a[href*="delete_employee"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить этого сотрудника?\nЭто действие нельзя отменить.')) {
                e.preventDefault();
            }
        });
    });
    
    // 2. Автоматическое форматирование телефона (без валидации)
    const phoneInputs = document.querySelectorAll('input[name="phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = this.value.replace(/\D/g, '');
            
            if (value.length > 0) {
                if (!value.startsWith('+')) {
                    value = '+7' + value;
                }
                
                // Форматирование: +7 (XXX) XXX-XX-XX
                if (value.length > 2) {
                    value = value.substring(0, 2) + ' (' + value.substring(2, 5) + ') ' + 
                            value.substring(5, 8) + '-' + value.substring(8, 10) + '-' + 
                            value.substring(10, 12);
                }
            }
            
            this.value = value;
        });
    });
    
    // 3. Подсветка строк таблицы при наведении
    const tableRows = document.querySelectorAll('table tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transition = 'background-color 0.2s ease';
        });
    });
    
    // 4. Поиск с задержкой (debounce)
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let timeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                this.closest('form').submit();
            }, 500);
        });
    }
    
    // 5. Показ/скрытие пароля
    const passwordInput = document.querySelector('input[name="password"]');
    if (passwordInput) {
        const passwordContainer = passwordInput.parentElement;
        
        // Создаем кнопку показа пароля
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.innerHTML = '👁️';
        toggleBtn.style.cssText = `
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            cursor: pointer;
            font-size: 18px;
            opacity: 0.7;
        `;
        
        passwordContainer.style.position = 'relative';
        passwordInput.style.paddingRight = '40px';
        passwordContainer.appendChild(toggleBtn);
        
        toggleBtn.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.innerHTML = type === 'password' ? '👁️' : '👁️‍🗨️';
        });
    }
    
    // 6. Анимация загрузки при отправке формы
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Добавляем индикатор загрузки
            if (!this.querySelector('.spinner')) {
                const spinner = document.createElement('span');
                spinner.className = 'spinner';
                spinner.innerHTML = ' ⏳';
                this.appendChild(spinner);
                
                // Блокируем повторную отправку
                this.disabled = true;
                this.style.opacity = '0.7';
            }
        });
    });
    
    // 7. Динамическое обновление даты в футере
    const yearSpan = document.querySelector('#current-year');
    if (!yearSpan) {
        const footer = document.querySelector('.footer p');
        if (footer) {
            footer.innerHTML = footer.innerHTML.replace('2025', new Date().getFullYear());
        }
    }
    
    // 8. Проверка на мобильное устройство
    if ('ontouchstart' in window || navigator.maxTouchPoints) {
        document.body.classList.add('touch-device');
        
        // Увеличиваем размер кликабельных элементов на мобильных
        const buttons = document.querySelectorAll('button, .btn, a');
        buttons.forEach(btn => {
            btn.style.minHeight = '44px';
            btn.style.minWidth = '44px';
        });
    }
    
    // 9. Уведомления (toast) - упрощенная версия
    window.showToast = function(message, type = 'info') {
        // Простой alert для теста
        alert((type === 'success' ? '✅ ' : type === 'error' ? '❌ ' : 'ℹ️ ') + message);
    };
});

// Глобальные функции для использования в других местах
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        window.showToast('Скопировано в буфер обмена!', 'success');
    }).catch(err => {
        console.error('Ошибка копирования:', err);
    });
}