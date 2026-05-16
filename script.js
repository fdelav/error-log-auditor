const counters = {
    error: 0,
    warning: 0,
    info: 0,
    nmap: 0
};

function updateDisplay(type) {
    document.getElementById(`${type}-count`).textContent = counters[type];
}

function showMessage(type, text) {
    const msg = document.getElementById('message');
    msg.textContent = text;
    msg.className = `message ${type} show`;

    setTimeout(() => {
        msg.classList.remove('show');
    }, 2500);
}

async function logMessage(type) {
    try {
        const response = await fetch('log.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `type=${type}`
        });

        const result = await response.json();

        const labels = { error: 'ERROR', warning: 'WARNING', info: 'INFO', nmap: 'NMAP' };

        if (result.success) {
            counters[type]++;
            updateDisplay(type);

            const label = labels[type] || type.toUpperCase();
            showMessage(type, `${label} registrado #${counters[type]}`);
        } else {
            showMessage('error', result.error || 'Error al registrar log');
        }
    } catch (err) {
        showMessage('error', 'Error de conexión');
    }
}

document.getElementById('btn-error').addEventListener('click', () => logMessage('error'));
document.getElementById('btn-warning').addEventListener('click', () => logMessage('warning'));
document.getElementById('btn-info').addEventListener('click', () => logMessage('info'));
document.getElementById('btn-nmap').addEventListener('click', () => logMessage('nmap'));