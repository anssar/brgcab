function creationValidate(e) {
    e = e || window.event;
    var surname = document.getElementById('surname');
    var firstname = document.getElementById('firstname');
    var patronymic = document.getElementById('patronymic');
    var phone = document.getElementById('phone');
    var gos_number = document.getElementById('gos_number');
    if (surname.value === '' || firstname.value === '' || patronymic.value === ''
        || phone.value === '') {
        var validation_alert = document.getElementById('validation_alert');
        setProperty(validation_alert, 'display', 'block');
        return false;
    }
    if (phone.value.length != 11) {
        var validation_alert = document.getElementById('phone_length_alert');
        setProperty(validation_alert, 'display', 'block');
        return false;
    }
    document.getElementById('creationButton').disabled = true;
}

function carCreationValidate(e) {
    e = e || window.event;
    var gos_number = document.getElementById('gos_number');
    if (gos_number.value === '') {
        var validation_alert = document.getElementById('validation_alert');
        setProperty(validation_alert, 'display', 'block');
        return false;
    }
    if (gos_number.value.length != 3) {
        var validation_alert = document.getElementById('gos_number_length_alert');
        setProperty(validation_alert, 'display', 'block');
        return false;
    }
    document.getElementById('carCreationButton').disabled = true;
}

function editionValidate(e) {
    e = e || window.event;
    var name = document.getElementById('name');
    var phone = document.getElementById('phone');
    if (name.value === '' || phone.value === '') {
        var validation_alert = document.getElementById('validation_alert');
        setProperty(validation_alert, 'display', 'block');
        return false;
    }
    if (phone.value.length != 11) {
        var validation_alert = document.getElementById('phone_length_alert');
        setProperty(validation_alert, 'display', 'block');
        return false;
    }
    document.getElementById('saveButton').disabled = true;
}

function regenerateValidate(e) {
    e = e || window.event;
    if (confirm("Вы уверены, что хотите поменять пароль?")) {
        document.getElementById('regenerateButton').disabled = true;
    }
    else {
        return false;
    }
}

function carExistValidate(e) {
    e = e || window.event;
    document.getElementById('carExistButton').disabled = true;
}

function loadValidate(e) {
    e = e || window.event;
    document.getElementById('loadButton').disabled = true;
}

function setProperty(obj, property, value) {
    if (obj.style.setProperty)
        obj.style.setProperty(property, value);
    else if (obj.style.setAttribute) {
        var parts = property.split('-');
        var propertyCamelCase = parts[0];
        for (var i = 1; i < parts.length; i++) {
            propertyCamelCase += parts[i].charAt(0).toUpperCase() +
                parts[i].substr(1);
        }
        obj.style.setAttribute(propertyCamelCase, value);
    } else {
        console.log('setProperty not supported');
    }
}