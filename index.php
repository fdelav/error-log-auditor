<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>No toques nada</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>NO TOQUES NADA</h1>
        <p class="subtitle">XAMPP Error Logger - ¡Cuidado con los botones!</p>

        <div class="button-row">
            <button id="btn-error" class="btn btn-error">
                <span class="btn-label">ERROR</span>
                <span class="btn-count" id="error-count">0</span>
            </button>

            <button id="btn-warning" class="btn btn-warning">
                <span class="btn-label">WARNING</span>
                <span class="btn-count" id="warning-count">0</span>
            </button>

            <button id="btn-nmap" class="btn btn-nmap">
                <span class="btn-label">NMAP</span>
                <span class="btn-sublabel">SIMULADO</span>
                <span class="btn-count" id="nmap-count">0</span>
            </button>
        </div>

        <div class="button-row">
            <button id="btn-info" class="btn btn-info">
                <span class="btn-label">INFO</span>
                <span class="btn-count" id="info-count">0</span>
            </button>
        </div>

        <div class="message" id="message"></div>
    </div>

    <script src="script.js"></script>
</body>
</html>