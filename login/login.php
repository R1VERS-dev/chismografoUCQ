<?php
session_start();
require 'conexion.php';

$error = '';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $usuario = trim($_POST['usuario']);
    $password = trim($_POST['password']);

    if (!empty($usuario) && !empty($password)) {
        $stmt = $pdo->prepare('SELECT * FROM usuarios WHERE usuario = ?');
        $stmt->execute([$usuario]);
        $user = $stmt->fetch();

        if ($user && password_verify($password, $user['password'])) {
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['user_name'] = $user['usuario'];
            $error = "¡Login exitoso! Bienvenido " . htmlspecialchars($user['usuario']);
        } else {
            $error = "Credenciales inválidas";
        }
    } else {
        $error = "Todos los campos son obligatorios";
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Glossy</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="blur-background"></div>
    <div class="login-container">
        <div class="glass-card">
            <h2>Iniciar Sesión</h2>
            <form action="login.php" method="post">
                <div class="input-group">
                    <input type="text" name="usuario" required autocomplete="off">
                    <label>Usuario</label>
                    <span class="highlight"></span>
                </div>
                <div class="input-group">
                    <input type="password" name="password" required>
                    <label>Contraseña</label>
                    <span class="highlight"></span>
                </div>
                <button type="submit" class="glossy-btn">Ingresar</button>
                <?php if($error): ?>
                    <p class="error-message"><?= $error ?></p>
                <?php endif; ?>
            </form>
        </div>
    </div>
</body>
</html>