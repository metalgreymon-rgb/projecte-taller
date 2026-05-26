-- Taller Mecànic Connectat - Esquema de BDs (Jan Bote i Joan Molina)

CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    telefon VARCHAR(20),
    correu VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    matricula VARCHAR(20) NOT NULL,
    model VARCHAR(50),
    any_fabricacio INT,
    quilometres INT,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS cites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    data_cita DATE NOT NULL,
    servei_sollicitat VARCHAR(100),
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

-- Dades de prova

INSERT INTO clients (nom, telefon, correu) VALUES
('Maria Garcia',    '612 345 678', 'maria.garcia@email.com'),
('Joan Puig',       '634 567 890', 'joan.puig@email.com'),
('Anna Martínez',   '698 123 456', 'anna.martinez@email.com'),
('Pere Soler',      '611 987 654', 'pere.soler@email.com'),
('Laura Ferrer',    '677 234 567', 'laura.ferrer@email.com');

INSERT INTO vehicles (client_id, matricula, model, any_fabricacio, quilometres) VALUES
(1, '1234 ABC', 'Seat Ibiza',       2018, 85000),
(1, '5678 DEF', 'Toyota Yaris',     2020, 32000),
(2, '9012 GHI', 'Ford Focus',       2016, 120000),
(3, '3456 JKL', 'Volkswagen Golf',  2019, 67000),
(4, '7890 MNO', 'Renault Clio',     2021, 18000),
(5, '2345 PQR', 'Peugeot 208',      2017, 95000);

INSERT INTO cites (client_id, vehicle_id, data_cita, servei_sollicitat) VALUES
(1, 1, '2025-05-26', 'Canvi d''oli i filtre'),
(1, 2, '2025-05-27', 'Revisió frens'),
(2, 3, '2025-05-28', 'Canvi de pneumàtics'),
(3, 4, '2025-05-29', 'Revisió general ITV'),
(4, 5, '2025-06-02', 'Reparació aire condicionat'),
(5, 6, '2025-06-03', 'Diagnosi electrònica'),
(1, 1, '2025-06-05', 'Canvi bateria');
