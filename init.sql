CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('activo', 'inactivo', 'suspendido') NOT NULL
);

INSERT INTO usuarios (nombre, email, estado) VALUES
('Juan Pérez', 'juanperez@example.com', 'activo'),
('María López', 'marialopez@example.com', 'inactivo'),
('Carlos Gómez', 'carlosgomez@example.com', 'activo'),
('Ana Torres', 'anatorres@example.com', 'suspendido'),
('Luis Ramírez', 'luisramirez@example.com', 'activo');