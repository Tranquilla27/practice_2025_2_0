let mainFormulaLoaded = false;
let nestedFormulas = {};
let variableWidgets = [];
let selectedVariableIndex = -1;

function showAddFormulaModal() {
    document.getElementById('addFormulaModal').style.display = 'block';
}

function showInsertFormulaModal() {
    if (!mainFormulaLoaded) {
        showAlert('Сначала добавьте основную формулу');
        return;
    }

    const variableList = document.getElementById('variableList');
    variableList.innerHTML = '';

    let hasEmptyVariables = false;

    for (let i = 0; i < variableWidgets.length; i++) {
        const widget = variableWidgets[i];

        if (!widget.isFormula) {
            const div = document.createElement('div');
            div.className = 'form-group';

            const input = document.createElement('input');
            input.type = 'radio';
            input.name = 'variableSelect';
            input.id = 'var_' + i;
            input.value = i;
            input.onchange = function () {
                selectedVariableIndex = i;
            };

            const label = document.createElement('label');
            label.htmlFor = 'var_' + i;
            label.style.display = 'inline';
            label.style.marginLeft = '10px';
            label.textContent = widget.label.textContent;

            if (widget.input.value === '') {
                hasEmptyVariables = true;
            } else {
                input.disabled = true;
                label.style.color = '#999';
                label.textContent += ' (уже заполнено)';
            }

            div.appendChild(input);
            div.appendChild(label);
            variableList.appendChild(div);
        }
    }

    if (!hasEmptyVariables) {
        variableList.innerHTML = '<p>Нет доступных пустых переменных для замены формулой</p>';
        document.querySelector('#insertFormulaModal .btn-primary').disabled = true;
    } else {
        document.querySelector('#insertFormulaModal .btn-primary').disabled = false;
    }

    document.getElementById('insertFormulaModal').style.display = 'block';
}

function showTopicSelectionModal() {
    document.getElementById('topicSelectionModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function openStudyWindow() {
    closeModal('topicSelectionModal');
    document.getElementById('studyWindow').style.display = 'block';
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    document.body.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(alertDiv);
        }, 300);
    }, 3000);
}

function insertMainFormula() {
    closeModal('addFormulaModal');

    if (mainFormulaLoaded) return;

    document.getElementById('formulaEditor').style.display = 'block';

    const inputsContainer = document.getElementById('formulaInputs');
    inputsContainer.innerHTML = '';

    addVariableInput('v (скорость):', inputsContainer);
    addVariableInput('t (время):', inputsContainer);

    mainFormulaLoaded = true;
}

function addVariableInput(labelText, container) {
    const div = document.createElement('div');
    div.className = 'form-group';

    const label = document.createElement('label');
    label.textContent = labelText;

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'variable-input';

    div.appendChild(label);
    div.appendChild(input);
    container.appendChild(div);

    variableWidgets.push({
        label: label,
        input: input,
        isFormula: false,
        container: div
    });
}

function confirmInsertFormula() {
    if (selectedVariableIndex === -1) {
        showAlert('Выберите переменную для замены', 'error');
        return;
    }

    const widget = variableWidgets[selectedVariableIndex];

    if (widget.input.value !== '') {
        showAlert('Выбранная переменная уже заполнена', 'error');
        return;
    }

    closeModal('insertFormulaModal');
    insertFormulaBlock(selectedVariableIndex);
    selectedVariableIndex = -1;
}

function insertFormulaBlock(index) {
    const widget = variableWidgets[index];
    const container = widget.container;

    container.innerHTML = '';

    const label = document.createElement('label');
    label.textContent = widget.label.textContent;
    container.appendChild(label);

    const formulaText = document.createElement('p');
    formulaText.className = 'formula-text';
    formulaText.textContent = '(2 * x) / y (ПРИМЕР)';
    formulaText.style.color = 'green';
    formulaText.style.fontStyle = 'italic';
    container.appendChild(formulaText);

    const nestedDiv = document.createElement('div');
    nestedDiv.className = 'nested-formula';

    const xDiv = document.createElement('div');
    xDiv.className = 'form-group';

    const xLabel = document.createElement('label');
    xLabel.textContent = 'x (значение):';

    const xInput = document.createElement('input');
    xInput.type = 'text';

    xDiv.appendChild(xLabel);
    xDiv.appendChild(xInput);
    nestedDiv.appendChild(xDiv);

    const yDiv = document.createElement('div');
    yDiv.className = 'form-group';

    const yLabel = document.createElement('label');
    yLabel.textContent = 'y (знаменатель):';

    const yInput = document.createElement('input');
    yInput.type = 'text';

    yDiv.appendChild(yLabel);
    yDiv.appendChild(yInput);
    nestedDiv.appendChild(yDiv);

    container.appendChild(nestedDiv);

    variableWidgets[index] = {
        label: label,
        input: formulaText,
        isFormula: true,
        container: container,
        nestedInputs: [xInput, yInput]
    };

    nestedFormulas[index] = variableWidgets[index].nestedInputs;

    showAlert(`Формула добавлена в переменную ${widget.label.textContent}`, 'success');
}

function calculateResult() {
    try {
        if (!mainFormulaLoaded) {
            throw new Error('Сначала добавьте основную формулу');
        }

        for (let i = 0; i < variableWidgets.length; i++) {
            const widget = variableWidgets[i];

            if (!widget.isFormula) {
                if (widget.input.value === '') {
                    throw new Error(`Поле '${widget.label.textContent}' не заполнено`);
                }
            } else {
                if (widget.nestedInputs[0].value === '' || widget.nestedInputs[1].value === '') {
                    throw new Error(`Не заполнены все поля для формулы в '${widget.label.textContent}'`);
                }
            }
        }

        const vValue = getVariableValue(0);
        const tValue = getVariableValue(1);

        const result = vValue * tValue;

        showAlert(`Ответ: S = ${result.toFixed(2)}`, 'success');
    } catch (error) {
        showAlert(`Ошибка: ${error.message}`, 'error');
    }
}

function getVariableValue(index) {
    const widget = variableWidgets[index];

    if (!widget.isFormula) {
        const value = widget.input.value;

        const numValue = parseFloat(value);

        if (isNaN(numValue)) {
            throw new Error(`Некорректное значение в поле '${widget.label.textContent}'`);
        }

        return numValue;
    } else {
        const xInput = widget.nestedInputs[0];
        const yInput = widget.nestedInputs[1];

        const x = parseFloat(xInput.value);
        const y = parseFloat(yInput.value);

        if (isNaN(x) || isNaN(y)) {
            throw new Error(`Некорректные значения для формулы в поле '${widget.label.textContent}'`);
        }

        if (y === 0) {
            throw new Error(`Деление на ноль в формуле поля '${widget.label.textContent}'`);
        }

        return (2 * x) / y;
    }
}