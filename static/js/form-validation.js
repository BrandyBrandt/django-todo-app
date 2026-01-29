document.addEventListener('DOMContentLoaded', function() {
    var taskForm = document.getElementById('taskForm');
    if (taskForm) {
        initTaskFormValidation(taskForm);
    }
    
    var categoryForm = document.getElementById('categoryForm');
    if (categoryForm) {
        initCategoryFormValidation(categoryForm);
    }
    
    initToggleAjax();
    initClearReminderTime();
});

function showFieldError(fieldId, message) {
    var errorSpan = document.getElementById(fieldId + '-error');
    var field = document.getElementById('id_' + fieldId);
    
    if (errorSpan) {
        errorSpan.textContent = message;
        errorSpan.style.display = 'block';
    }
    
    if (field) {
        field.classList.add('field-invalid');
        field.setAttribute('aria-invalid', 'true');
    }
}

function clearFieldError(fieldId) {
    var errorSpan = document.getElementById(fieldId + '-error');
    var field = document.getElementById('id_' + fieldId);
    
    if (errorSpan) {
        errorSpan.textContent = '';
        errorSpan.style.display = 'none';
    }
    
    if (field) {
        field.classList.remove('field-invalid');
        field.removeAttribute('aria-invalid');
    }
}

function initClearReminderTime() {
    var clearBtn = document.getElementById('clear-reminder-time');
    var reminderTimeField = document.getElementById('id_reminder_time');
    
    if (clearBtn && reminderTimeField) {
        clearBtn.addEventListener('click', function(e) {
            e.preventDefault();
            reminderTimeField.value = '';
            clearFieldError('reminder_time');
        });
    }
}

function initTaskFormValidation(form) {
    
    var titleField = document.getElementById('id_title');
    var dueDateField = document.getElementById('id_due_date');
    var dueTimeField = document.getElementById('id_due_time');
    var reminderDateField = document.getElementById('id_reminder_date');
    var reminderTimeField = document.getElementById('id_reminder_time');
    
    if (titleField) {
        titleField.addEventListener('input', function() {
            if (this.value.trim().length >= 3) {
                clearFieldError('title');
            }
        });
    }
    
    if (dueDateField) {
        dueDateField.addEventListener('change', function() {
            if (this.value) {
                clearFieldError('due_date');
            }
        });
    }
    
    if (reminderDateField) {
        reminderDateField.addEventListener('change', function() {
            clearFieldError('reminder_date');
        });
    }
    
    if (reminderTimeField) {
        reminderTimeField.addEventListener('change', function() {
            clearFieldError('reminder_time');
        });
    }
    
    form.addEventListener('submit', function(event) {
        var isValid = true;
        
        if (!validateTitle(titleField ? titleField.value : '')) {
            isValid = false;
        }
        
        if (!validateDueDate(dueDateField ? dueDateField.value : '')) {
            isValid = false;
        }
        
        if (!validateReminder()) {
            isValid = false;
        }
        
        if (!isValid) {
            event.preventDefault();
            
            var firstError = form.querySelector('.field-invalid');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstError.focus();
            }
        }
    });
    
    function validateTitle(value) {
        var trimmed = value.trim();
        
        if (trimmed.length === 0) {
            showFieldError('title', 'Tytuł jest wymagany');
            return false;
        }
        
        if (trimmed.length < 3) {
            showFieldError('title', 'Tytuł musi zawierać minimum 3 znaki');
            return false;
        }
        
        if (trimmed.length > 200) {
            showFieldError('title', 'Tytuł nie może przekraczać 200 znaków');
            return false;
        }
        
        clearFieldError('title');
        return true;
    }
    
    function validateDueDate(value) {
        if (!value) {
            showFieldError('due_date', 'Data terminu wykonania jest wymagana');
            return false;
        }
        
        var selectedDate = new Date(value);
        var today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            showFieldError('due_date', 'Data nie może być z przeszłości');
            return false;
        }
        
        clearFieldError('due_date');
        return true;
    }
    
    function validateReminder() {
        var reminderDate = reminderDateField ? reminderDateField.value : '';
        var reminderTime = reminderTimeField ? reminderTimeField.value : '';
        
        if (!reminderDate && !reminderTime) {
            clearFieldError('reminder_date');
            clearFieldError('reminder_time');
            return true;
        }
        
        if (reminderDate && !reminderTime) {
            showFieldError('reminder_time', 'Podaj również godzinę przypomnienia');
            return false;
        }
        
        if (!reminderDate && reminderTime) {
            showFieldError('reminder_date', 'Podaj również datę przypomnienia');
            return false;
        }
        
        var dueDate = dueDateField ? dueDateField.value : '';
        var dueTime = dueTimeField ? dueTimeField.value : '00:00';
        
        if (dueDate && reminderDate) {
            var dueDateTime = new Date(dueDate + 'T' + dueTime);
            var reminderDateTime = new Date(reminderDate + 'T' + reminderTime);
            
            if (reminderDateTime > dueDateTime) {
                showFieldError('reminder_date', 'Przypomnienie musi być przed terminem wykonania');
                return false;
            }
        }
        
        clearFieldError('reminder_date');
        clearFieldError('reminder_time');
        return true;
    }
}

function initCategoryFormValidation(form) {
    
    var nameField = document.getElementById('id_name');
    
    if (nameField) {
        nameField.addEventListener('input', function() {
            if (this.value.trim().length > 0) {
                clearFieldError('name');
            }
        });
    }
    
    form.addEventListener('submit', function(event) {
        if (!validateCategoryName(nameField ? nameField.value : '')) {
            event.preventDefault();
            nameField.focus();
        }
    });
    
    function validateCategoryName(value) {
        var trimmed = value.trim();
        
        if (trimmed.length === 0) {
            showFieldError('name', 'Nazwa kategorii jest wymagana');
            return false;
        }
        
        if (trimmed.length > 50) {
            showFieldError('name', 'Nazwa nie może przekraczać 50 znaków');
            return false;
        }
        
        clearFieldError('name');
        return true;
    }
}

function initToggleAjax() {
    var toggleForms = document.querySelectorAll('.toggle-form');
    
    toggleForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            var button = form.querySelector('.toggle-btn');
            var taskItem = form.closest('.task-item');
            var csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: 'csrfmiddlewaretoken=' + encodeURIComponent(csrfToken)
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                if (data.success) {
                    if (data.is_completed) {
                        button.textContent = '✓';
                        if (taskItem) {
                            taskItem.classList.add('completed');
                        }
                    } else {
                        button.textContent = '○';
                        if (taskItem) {
                            taskItem.classList.remove('completed');
                        }
                    }
                }
            })
            .catch(function(error) {
                form.submit();
            });
        });
    });
}
