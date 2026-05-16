<?php
header('Content-Type: application/json');

$type = $_POST['type'] ?? '';
$logFile = 'C:/xampp/apache/logs/error.log';

$messages = [
    'error' => 'Client error generated',
    'warning' => 'Client warning generated',
    'info' => 'Client info generated',
    'nmap' => 'NMAP SIMULATED SCAN'
];

if (!isset($messages[$type])) {
    echo json_encode(['success' => false, 'error' => 'Tipo inválido']);
    exit;
}

$clientIP = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$clientPort = $_SERVER['REMOTE_PORT'] ?? '0';
$timestamp = date('M j H:i:s');
$hostname = 'xampp-server';
$process = 'php';
$pid = getmypid();

if ($type === 'nmap') {
    $targetIP = '192.168.1.' . rand(1, 254);
    $openPorts = implode(',', [22, 80, 443, rand(1000, 9999)]);
    $logEntry = $timestamp . " nmap-simulator nmap[" . $pid . "]: [scan] IP: " . $targetIP . " Ports: " . $openPorts . " Status: open - NMAP SIMULATED SCAN\n";
} else {
    $logEntry = $timestamp . " " . $hostname . " " . $process . "[" . $pid . "]: [" . $type . "] IP: " . $clientIP . " Port: " . $clientPort . " - " . $messages[$type] . "\n";
}

$result = file_put_contents($logFile, $logEntry, FILE_APPEND | LOCK_EX);

echo json_encode(['success' => (bool)$result]);