document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Подтверждение удаления сотрудника
    const deleteLinks = document.querySelectorAll('a[href*="delete_employee"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить этого сотрудника?\nЭто действие нельзя отменить.')) {
                e.preventDefault();
            }
        });
    });
    
    // 2. Валидация формы добавления/редактирования сотрудника
    const forms = document.querySelectorAll('form[method="post"]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const phoneInput = form.querySelector('input[name="phone"]');
            const emailInput = form.querySelector('input[name="email"]');
            
            // Валидация телефона
            if (phoneInput && phoneInput.value) {
                const phoneRegex = /^[\d\s\-\+\(\)]+$/;
                if (!phoneRegex.test(phoneInput.value)) {
                    alert('Некорректный номер телефона! Разрешены только цифры, пробелы, +, -, ( и )');
                    phoneInput.focus();
                    e.preventDefault();
                    return;
                }
            }
            
            // Валидация email
            if (emailInput && emailInput.value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(emailInput.value)) {
                    alert('Введите корректный email адрес!');
                    emailInput.focus();
                    e.preventDefault();
                    return;
                }
            }
        });
    });
    
    // 3. Автоматическое форматирование телефона
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
    
    // 4. Подсветка строк таблицы при наведении (уже есть в CSS, но добавим JS для динамики)
    const tableRows = document.querySelectorAll('table tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transition = 'background-color 0.2s ease';
        });
    });
    
    // 5. Динамическая загрузка "Показать ещё" (если есть пагинация)
    const loadMoreBtn = document.querySelector('a[href*="page="]');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            
            const btn = this;
            const originalText = btn.textContent;
            btn.textContent = 'Загрузка...';
            btn.style.opacity = '0.7';
            
            try {
                const response = await fetch(btn.href);
                const html = await response.text();
                
                // Создаем временный элемент для парсинга
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = html;
                
                // Находим новые строки таблицы
                const newRows = tempDiv.querySelectorAll('table tr:not(:first-child)');
                const table = document.querySelector('table');
                
                // Добавляем новые строки с анимацией
                newRows.forEach((row, index) => {
                    setTimeout(() => {
                        row.style.opacity = '0';
                        row.style.transform = 'translateY(20px)';
                        table.appendChild(row);
                        
                        // Анимация появления
                        setTimeout(() => {
                            row.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                            row.style.opacity = '1';
                            row.style.transform = 'translateY(0)';
                        }, 10);
                    }, index * 100);
                });
                
                // Обновляем кнопку "Показать ещё"
                const newLoadMoreBtn = tempDiv.querySelector('a[href*="page="]');
                if (newLoadMoreBtn) {
                    btn.href = newLoadMoreBtn.href;
                    btn.textContent = newLoadMoreBtn.textContent;
                } else {
                    btn.style.display = 'none';
                }
                
            } catch (error) {
                console.error('Ошибка загрузки:', error);
                alert('Ошибка загрузки данных. Попробуйте ещё раз.');
                btn.textContent = originalText;
            }
            
            btn.style.opacity = '1';
        });
    }
    
    // 6. Поиск с задержкой (debounce)
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let timeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                // Автоматически отправляем форму поиска через 500ms после остановки ввода
                this.closest('form').submit();
            }, 500);
        });
    }
    
    // 7. Показ/скрытие пароля
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
    
    // 8. Анимация загрузки при отправке формы
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
    
    // 9. Динамическое обновление даты в футере
    const yearSpan = document.querySelector('#current-year');
    if (!yearSpan) {
        const footer = document.querySelector('.footer p');
        if (footer) {
            footer.innerHTML = footer.innerHTML.replace('2025', new Date().getFullYear());
        }
    }
    
    // 10. Уведомления (toast)
    window.showToast = function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span class="toast-icon">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
            <span class="toast-message">${message}</span>
            <button class="toast-close">×</button>
        `;
        
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: ${type === 'success' ? '#c6f6d5' : type === 'error' ? '#fed7d7' : '#bee3f8'};
            color: ${type === 'success' ? '#22543d' : type === 'error' ? '#c53030' : '#2c5282'};
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 9999;
            animation: slideInRight 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        // Кнопка закрытия
        toast.querySelector('.toast-close').addEventListener('click', () => {
            toast.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        });
        
        // Автоматическое скрытие через 5 секунд
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
    };
    
    // Анимации для toast
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        .toast-close {
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            padding: 0;
            margin-left: 10px;
            opacity: 0.7;
        }
        .toast-close:hover {
            opacity: 1;
        }
    `;
    document.head.appendChild(style);
    
    // 11. Проверка на мобильное устройство
    if ('ontouchstart' in window || navigator.maxTouchPoints) {
        document.body.classList.add('touch-device');
        
        // Увеличиваем размер кликабельных элементов на мобильных
        const buttons = document.querySelectorAll('button, .btn, a');
        buttons.forEach(btn => {
            btn.style.minHeight = '44px';
            btn.style.minWidth = '44px';
        });
    }
    
    console.log('Кадровая система загружена!');
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