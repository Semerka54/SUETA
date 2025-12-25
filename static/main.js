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
    
    // 2. Автоматическое форматирование телефона (курсор всегда в конце)
const phoneInputs = document.querySelectorAll('input[name="phone"]');
phoneInputs.forEach(input => {
    // Устанавливаем начальное значение +7
    if (!input.value) {
        input.value = '+7 ';
    }
    
    input.addEventListener('input', function(e) {
        // Берем все цифры
        let value = this.value.replace(/\D/g, '');
        let formatted = '+7';
        
        // Убираем код страны если есть
        if (value.startsWith('7')) {
            value = value.substring(1);
        } else if (value.startsWith('8')) {
            value = value.substring(1);
        }
        
        // Ограничиваем 10 цифрами
        value = value.substring(0, 10);
        
        // Форматируем
        if (value.length > 0) {
            formatted += ' (' + value.substring(0, 3);
        }
        if (value.length > 3) {
            formatted += ') ' + value.substring(3, 6);
        }
        if (value.length > 6) {
            formatted += '-' + value.substring(6, 8);
        }
        if (value.length > 8) {
            formatted += '-' + value.substring(8, 10);
        }
        
        // Устанавливаем значение
        this.value = formatted;
        
        // Курсор всегда в конце
        setTimeout(() => {
            this.setSelectionRange(formatted.length, formatted.length);
        }, 0);
    });
    
    // При фокусе курсор в конце
    input.addEventListener('focus', function() {
        setTimeout(() => {
            this.setSelectionRange(this.value.length, this.value.length);
        }, 0);
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
    
    
    // 7. Динамическое обновление даты в футере
    const yearSpan = document.querySelector('#current-year');
    if (!yearSpan) {
        const footer = document.querySelector('.footer p');
        if (footer) {
            footer.innerHTML = footer.innerHTML.replace('2025', new Date().getFullYear());
        }
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