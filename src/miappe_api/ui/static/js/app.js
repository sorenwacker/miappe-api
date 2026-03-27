// Minimal JavaScript for HTMX UI

// Handle collapsible sections
document.addEventListener('click', function(e) {
    const header = e.target.closest('.collapsible-header');
    if (header) {
        const collapsible = header.closest('.collapsible');
        collapsible.classList.toggle('open');
    }
});

// Handle profile select change
document.addEventListener('change', function(e) {
    if (e.target.id === 'profile-select') {
        const profile = e.target.value;
        window.location.href = '/profile/' + profile;
    }
});

// Auto-dismiss notifications after 5 seconds
document.addEventListener('htmx:afterSwap', function(e) {
    if (e.target.id === 'notification-container') {
        const notifications = e.target.querySelectorAll('.notification');
        notifications.forEach(function(notification) {
            setTimeout(function() {
                notification.style.opacity = '0';
                setTimeout(function() {
                    notification.remove();
                }, 200);
            }, 5000);
        });
    }
});

// Handle delete confirmation
function confirmDelete(nodeId, nodeLabel) {
    return confirm('Delete "' + nodeLabel + '"?');
}

// Field validation rules for specific fields
var fieldValidators = {
    // Email validation
    'email': function(value) {
        if (!value) return true;
        return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value);
    },
    // Geographic coordinates (used in Study and other entities)
    'latitude': function(value) {
        if (!value) return true;
        var num = parseFloat(value);
        return !isNaN(num) && num >= -90 && num <= 90;
    },
    'longitude': function(value) {
        if (!value) return true;
        var num = parseFloat(value);
        return !isNaN(num) && num >= -180 && num <= 180;
    },
    'altitude': function(value) {
        if (!value) return true;
        var num = parseFloat(value);
        return !isNaN(num) && num >= -500 && num <= 10000;
    },
    // BiologicalMaterial coordinates
    'biological_material_latitude': function(value) {
        if (!value) return true;
        var num = parseFloat(value);
        return !isNaN(num) && num >= -90 && num <= 90;
    },
    'biological_material_longitude': function(value) {
        if (!value) return true;
        var num = parseFloat(value);
        return !isNaN(num) && num >= -180 && num <= 180;
    },
    'biological_material_altitude': function(value) {
        if (!value) return true;
        var num = parseFloat(value);
        return !isNaN(num) && num >= -500 && num <= 10000;
    }
};

// Type-based validation
function validateByType(value, type) {
    if (!value) return true;
    switch (type) {
        case 'integer':
            return /^-?\d+$/.test(value);
        case 'float':
            return /^-?\d*\.?\d+$/.test(value);
        case 'date':
            return /^\d{4}-\d{2}-\d{2}$/.test(value);
        default:
            return true;
    }
}

// Validate table cell input
function validateTableCell(input) {
    var fieldName = input.getAttribute('data-field') || input.getAttribute('name');
    var dataType = input.getAttribute('data-type') || 'string';
    var value = input.value;
    var isValid = true;

    // Check field-specific validators first
    if (fieldValidators[fieldName]) {
        isValid = fieldValidators[fieldName](value);
    } else {
        // Fall back to type-based validation
        isValid = validateByType(value, dataType);
    }

    // Update visual state
    if (isValid) {
        input.classList.remove('invalid');
    } else {
        input.classList.add('invalid');
    }

    return isValid;
}

// Validate all table cells on input change
document.addEventListener('input', function(e) {
    if (e.target.classList.contains('form-input')) {
        validateTableCell(e.target);
    }
});

// Validate all cells after HTMX swap (for newly added rows)
document.addEventListener('htmx:afterSwap', function(e) {
    var table = e.target.closest('.data-table');
    if (table) {
        var inputs = table.querySelectorAll('.form-input');
        inputs.forEach(function(input) {
            if (input.value) {
                validateTableCell(input);
            }
        });
    }
});
