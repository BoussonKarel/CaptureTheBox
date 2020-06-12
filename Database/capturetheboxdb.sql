-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Gegenereerd op: 11 jun 2020 om 20:59
-- Serverversie: 10.3.17-MariaDB-0+deb10u1
-- PHP-versie: 7.3.11-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `capturetheboxdb`
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `bezit`
--

CREATE TABLE `bezit` (
  `BezitID` int(11) NOT NULL,
  `SpelID` int(11) DEFAULT NULL,
  `SpelerID` int(11) NOT NULL,
  `Starttijd` datetime DEFAULT NULL,
  `Eindtijd` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Gegevens worden geëxporteerd voor tabel `bezit`
--

INSERT INTO `bezit` (`BezitID`, `SpelID`, `SpelerID`, `Starttijd`, `Eindtijd`) VALUES
(1, 1, 1, '2020-05-01 14:00:00', '2020-05-01 16:25:00'),
(2, 1, 13, '2020-05-01 16:25:00', '2020-05-01 17:11:00'),
(3, 1, 3, '2020-05-01 17:11:00', '2020-05-01 20:01:00'),
(4, 1, 14, '2020-05-01 20:01:00', '2020-05-01 20:31:00'),
(5, 1, 5, '2020-05-01 20:31:00', '2020-05-01 21:45:00'),
(6, 1, 11, '2020-05-01 21:45:00', '2020-05-01 22:36:00'),
(7, 1, 7, '2020-05-01 22:36:00', '2020-05-02 08:55:00'),
(8, 1, 8, '2020-05-02 08:55:00', '2020-05-02 10:21:00'),
(9, 1, 9, '2020-05-02 10:21:00', '2020-05-02 10:51:00'),
(10, 1, 10, '2020-05-02 10:51:00', '2020-05-02 12:01:00'),
(11, 1, 6, '2020-05-02 12:01:00', '2020-05-02 13:55:00'),
(12, 1, 12, '2020-05-02 13:55:00', '2020-05-02 14:51:00'),
(13, 1, 2, '2020-05-02 14:51:00', '2020-05-02 15:59:00'),
(14, 1, 4, '2020-05-02 15:59:00', '2020-05-02 17:15:00'),
(15, 1, 9, '2020-05-02 17:15:00', '2020-05-02 18:32:00'),
(16, 1, 2, '2020-05-02 18:32:00', '2020-05-02 20:31:00'),
(17, 1, 3, '2020-05-02 20:31:00', '2020-05-02 21:56:00'),
(18, 1, 4, '2020-05-02 21:56:00', '2020-05-02 23:01:00'),
(19, 1, 11, '2020-05-02 23:01:00', '2020-05-03 09:52:00'),
(20, 1, 6, '2020-05-03 09:52:00', '2020-05-03 11:31:00'),
(21, 1, 7, '2020-05-03 11:31:00', '2020-05-03 13:15:00'),
(22, 1, 8, '2020-05-03 13:15:00', '2020-05-03 15:01:00'),
(23, 1, 1, '2020-05-03 15:01:00', '2020-05-03 17:54:00'),
(24, 1, 10, '2020-05-03 17:54:00', '2020-05-03 19:36:00'),
(25, 1, 5, '2020-05-03 19:36:00', '2020-06-03 14:00:00'),
(26, 2, 1, '2020-06-03 14:00:00', '2020-06-03 21:00:00'),
(27, 2, 3, '2020-06-03 21:00:00', '2020-06-04 09:00:00'),
(28, 2, 2, '2020-06-04 09:00:00', '2020-06-04 13:00:00'),
(29, 2, 1, '2020-06-04 13:00:00', '2020-06-04 13:59:33'),
(30, 2, 2, '2020-06-04 13:59:33', '2020-06-04 19:51:52'),
(32, 2, 3, '2020-06-04 19:51:52', '2020-06-04 20:00:00'),
(34, 2, 1, '2020-06-04 20:00:00', '2020-06-05 21:19:00'),
(35, 7, 21, '2020-06-06 12:44:42', '2020-06-06 12:45:00'),
(36, 7, 26, '2020-06-06 12:45:00', '2020-06-06 12:47:38'),
(37, 7, 21, '2020-06-06 12:47:38', '2020-06-06 13:38:44'),
(38, 8, 23, '2020-06-09 20:06:26', '2020-06-09 20:07:46'),
(39, 8, 21, '2020-06-09 20:07:46', '2020-06-09 20:15:54'),
(40, 8, 21, '2020-06-09 20:15:54', NULL),
(41, 9, 34, '2020-06-11 14:39:23', '2020-06-11 18:00:00'),
(47, 9, 35, '2020-06-11 18:00:00', '2020-06-11 20:53:14'),
(48, 9, 35, '2020-06-11 20:53:14', '2020-06-11 20:56:53'),
(49, 9, 34, '2020-06-11 20:56:53', '2020-06-11 20:57:00');

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `meting`
--

CREATE TABLE `meting` (
  `MetingID` int(11) NOT NULL,
  `SpelID` int(11) DEFAULT NULL,
  `Tijdstip` datetime NOT NULL,
  `SensorID` int(11) NOT NULL,
  `Waarde` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Gegevens worden geëxporteerd voor tabel `meting`
--

INSERT INTO `meting` (`MetingID`, `SpelID`, `Tijdstip`, `SensorID`, `Waarde`) VALUES
(1, 8, '2020-06-09 19:42:32', 1, '51.177576;3.216123'),
(2, 8, '2020-06-09 19:45:10', 2, '49.01960784313725'),
(3, 8, '2020-06-09 19:45:10', 1, '51.177576;3.216123'),
(4, 8, '2020-06-09 19:48:45', 2, '49.02'),
(5, 8, '2020-06-09 19:48:45', 1, '51.177576;3.216123'),
(6, 8, '2020-06-09 19:49:12', 2, '49.02'),
(7, 8, '2020-06-09 19:49:13', 1, '51.177576;3.216123'),
(8, 8, '2020-06-09 19:50:18', 2, '49.02'),
(9, 8, '2020-06-09 19:50:18', 1, '51.177576;3.216123'),
(10, 8, '2020-06-09 19:51:42', 2, '49.02'),
(11, 8, '2020-06-09 19:51:42', 1, '51.177576;3.216123'),
(12, 8, '2020-06-09 19:52:43', 2, '49.02'),
(13, 8, '2020-06-09 19:52:43', 1, '51.177576;3.216123'),
(14, 8, '2020-06-09 19:57:48', 2, '49.02'),
(15, 8, '2020-06-09 19:57:48', 1, '51.177576;3.216123'),
(16, 8, '2020-06-09 19:58:48', 2, '49.02'),
(17, 8, '2020-06-09 19:58:48', 1, '51.177576;3.216123'),
(18, 8, '2020-06-09 19:59:27', 2, '49.02'),
(19, 8, '2020-06-09 19:59:27', 1, '51.177576;3.216123'),
(20, 8, '2020-06-09 20:00:46', 2, '49.02'),
(21, 8, '2020-06-09 20:00:46', 1, '51.177576;3.216123'),
(22, 8, '2020-06-09 20:01:40', 2, '49.02'),
(23, 8, '2020-06-09 20:01:40', 1, '51.177576;3.216123'),
(24, 8, '2020-06-09 20:02:39', 2, '49.02'),
(25, 8, '2020-06-09 20:02:39', 1, '51.177576;3.216123'),
(26, 8, '2020-06-09 20:03:12', 2, '49.02'),
(27, 8, '2020-06-09 20:03:12', 1, '51.177576;3.216123'),
(28, 8, '2020-06-09 20:03:48', 2, '49.02'),
(29, 8, '2020-06-09 20:03:48', 1, '51.177576;3.216123'),
(30, 8, '2020-06-09 20:04:40', 2, '49.02'),
(31, 8, '2020-06-09 20:04:41', 1, '51.177576;3.216123'),
(32, 8, '2020-06-09 20:05:19', 2, '49.02'),
(33, 8, '2020-06-09 20:05:19', 1, '51.177576;3.216123'),
(34, 8, '2020-06-09 20:15:54', 2, '49.02'),
(35, 8, '2020-06-09 20:15:54', 1, '51.177576;3.216123'),
(36, NULL, '2020-06-10 15:48:35', 2, '49.02'),
(37, NULL, '2020-06-10 15:48:35', 1, '51.177576;3.216123'),
(38, 9, '2020-06-11 14:39:23', 2, '0'),
(39, 9, '2020-06-11 14:39:23', 1, '50.82528;3.249998'),
(40, 9, '2020-06-11 14:40:47', 2, '49.02'),
(41, 9, '2020-06-11 14:40:47', 1, '51.177576;3.216123'),
(42, 9, '2020-06-11 14:48:16', 2, '0'),
(43, 9, '2020-06-11 14:55:44', 1, '50.82528;3.249998'),
(44, 9, '2020-06-11 15:55:31', 2, '49.02'),
(45, 9, '2020-06-11 15:55:31', 1, '51.177576;3.216123'),
(46, 9, '2020-06-11 15:55:39', 2, '0'),
(47, 9, '2020-06-11 15:55:39', 1, '51.19378;3.232359'),
(48, 9, '2020-06-11 16:09:17', 2, '0'),
(49, 9, '2020-06-11 16:34:40', 1, '50.82528;3.249998'),
(50, 9, '2020-06-11 18:08:17', 2, '49.02'),
(51, 9, '2020-06-11 18:08:18', 1, '51.177576;3.216123'),
(52, NULL, '2020-06-11 20:11:48', 2, '49.02'),
(53, NULL, '2020-06-11 20:11:48', 1, '51.177576;3.216123'),
(54, 9, '2020-06-11 20:20:38', 2, '0.0'),
(55, 9, '2020-06-11 20:20:39', 1, '50.82528;3.249998'),
(56, 9, '2020-06-11 20:29:57', 2, '49.02'),
(57, 9, '2020-06-11 20:29:58', 1, '51.177576;3.216123'),
(58, 9, '2020-06-11 20:53:13', 2, '49.02'),
(59, 9, '2020-06-11 20:53:14', 1, '51.177576;3.216123'),
(60, 9, '2020-06-11 20:56:53', 2, '0.0'),
(61, 9, '2020-06-11 20:56:54', 1, '50.82528;3.249998');

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `sensor`
--

CREATE TABLE `sensor` (
  `SensorID` int(11) NOT NULL,
  `Naam` varchar(45) DEFAULT NULL,
  `Type` varchar(45) DEFAULT NULL,
  `Omschrijving` varchar(200) DEFAULT NULL,
  `Meeteenheid` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Gegevens worden geëxporteerd voor tabel `sensor`
--

INSERT INTO `sensor` (`SensorID`, `Naam`, `Type`, `Omschrijving`, `Meeteenheid`) VALUES
(1, 'NEO-7M', 'GPS', 'Geeft de GPS locatie van het spel terug.', 'LAT, LONG'),
(2, 'LDR', 'LDR', 'Geeft het lichtpercentage terug.', '%');

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `spel`
--

CREATE TABLE `spel` (
  `SpelID` int(11) NOT NULL,
  `Begintijd` datetime NOT NULL,
  `Eindtijd` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Gegevens worden geëxporteerd voor tabel `spel`
--

INSERT INTO `spel` (`SpelID`, `Begintijd`, `Eindtijd`) VALUES
(1, '2020-05-01 14:00:00', '2020-05-03 20:00:00'),
(2, '2020-06-03 14:00:00', '2020-06-05 21:19:00'),
(7, '2020-06-06 12:44:00', '2020-06-06 13:38:44'),
(8, '2020-06-09 19:00:00', '2020-06-09 20:30:00'),
(9, '2020-06-10 10:00:00', '2020-06-11 20:57:00');

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `speler`
--

CREATE TABLE `speler` (
  `SpelerID` int(11) NOT NULL,
  `RFIDUID` varchar(64) DEFAULT NULL,
  `Naam` varchar(45) DEFAULT NULL,
  `Moderator` tinyint(4) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Gegevens worden geëxporteerd voor tabel `speler`
--

INSERT INTO `speler` (`SpelerID`, `RFIDUID`, `Naam`, `Moderator`) VALUES
(1, '7a 63 50 73', 'Karel', 1),
(2, 'BB CC DD EE', 'Silken', 0),
(3, 'CC DD EE FF', 'Arthur', 0),
(4, 'DD EE FF GG', 'Thomas', 0),
(5, 'EE FF GG HH', 'Tom', 0),
(6, 'FF GG HH II', 'Pieter', 0),
(7, 'GG HH II JJ', 'Kasper', 0),
(8, 'HH II JJ KK', 'Jolan', 0),
(9, 'II JJ KK LL', 'Aaron', 0),
(10, 'JJ KK LL MM', 'Tuur', 0),
(11, 'KK LL MM NN', 'Tanguy', 0),
(12, 'LL MM NN O', 'Stijn', 0),
(13, 'MM NN OO PP', 'Olivier', 0),
(14, 'NN OO PP QQ', 'Jonas', 0),
(21, '66 c0 54 73', 'Karel', 1),
(22, '52 ae 43 73', 'Silken', 0),
(23, '6a 08 15 a3', 'Arthur', 0),
(24, '29 bf fd a3', 'Thomas', 0),
(25, '7a 63 50 73', 'Pieter', 0),
(26, '2a 1f 56 73', 'Kasper', 0),
(27, NULL, 'Jolan', 0),
(28, NULL, 'Tom', 0),
(29, NULL, 'Bram', 0),
(30, NULL, 'Stijn', 0),
(31, NULL, 'Aaron', 0),
(32, NULL, 'Tuur', 0),
(33, NULL, 'Tanguy', 0),
(34, '66 c0 54 73', 'Karel', 0),
(35, '52 ae 43 73', 'Silken', 0);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `spel_has_speler`
--

CREATE TABLE `spel_has_speler` (
  `Spel_SpelID` int(11) NOT NULL,
  `Speler_SpelerID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Gegevens worden geëxporteerd voor tabel `spel_has_speler`
--

INSERT INTO `spel_has_speler` (`Spel_SpelID`, `Speler_SpelerID`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(1, 12),
(1, 13),
(1, 14),
(2, 1),
(2, 2),
(2, 3),
(2, 4),
(7, 21),
(7, 22),
(7, 23),
(7, 24),
(7, 25),
(7, 26),
(7, 27),
(7, 28),
(7, 29),
(7, 30),
(7, 31),
(7, 32),
(7, 33),
(8, 21),
(8, 23),
(9, 34),
(9, 35);

-- --------------------------------------------------------

--
-- Stand-in structuur voor view `vwGetSpelerByRFID`
-- (Zie onder voor de actuele view)
--
CREATE TABLE `vwGetSpelerByRFID` (
`SpelerID` int(11)
);

-- --------------------------------------------------------

--
-- Stand-in structuur voor view `vwScoresPerSpeler`
-- (Zie onder voor de actuele view)
--
CREATE TABLE `vwScoresPerSpeler` (
`Naam` varchar(45)
,`Score` time
);

-- --------------------------------------------------------

--
-- Structuur voor de view `vwGetSpelerByRFID`
--
DROP TABLE IF EXISTS `vwGetSpelerByRFID`;

CREATE ALGORITHM=UNDEFINED DEFINER=`mysql`@`localhost` SQL SECURITY DEFINER VIEW `vwGetSpelerByRFID`  AS  select `SP`.`SpelerID` AS `SpelerID` from (`spel_has_speler` `SHS` join `speler` `SP` on(`SHS`.`Speler_SpelerID` = `SP`.`SpelerID`)) where `SHS`.`Spel_SpelID` = 2 and `SP`.`RFIDUID` = 'AA BB CC DD' ;

-- --------------------------------------------------------

--
-- Structuur voor de view `vwScoresPerSpeler`
--
DROP TABLE IF EXISTS `vwScoresPerSpeler`;

CREATE ALGORITHM=UNDEFINED DEFINER=`mysql`@`localhost` SQL SECURITY DEFINER VIEW `vwScoresPerSpeler`  AS  select `S`.`Naam` AS `Naam`,sec_to_time(sum(to_seconds(`B`.`Eindtijd`) - to_seconds(`B`.`Starttijd`))) AS `Score` from (`bezit` `B` join `speler` `S` on(`B`.`SpelerID` = `S`.`SpelerID`)) group by `S`.`Naam` ;

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `bezit`
--
ALTER TABLE `bezit`
  ADD PRIMARY KEY (`BezitID`),
  ADD KEY `fk_Capture_spel1_idx` (`SpelID`),
  ADD KEY `fk_Capture_speler1_idx` (`SpelerID`);

--
-- Indexen voor tabel `meting`
--
ALTER TABLE `meting`
  ADD PRIMARY KEY (`MetingID`),
  ADD KEY `fk_Meting_Sensor1_idx` (`SensorID`);

--
-- Indexen voor tabel `sensor`
--
ALTER TABLE `sensor`
  ADD PRIMARY KEY (`SensorID`);

--
-- Indexen voor tabel `spel`
--
ALTER TABLE `spel`
  ADD PRIMARY KEY (`SpelID`);

--
-- Indexen voor tabel `speler`
--
ALTER TABLE `speler`
  ADD PRIMARY KEY (`SpelerID`);

--
-- Indexen voor tabel `spel_has_speler`
--
ALTER TABLE `spel_has_speler`
  ADD PRIMARY KEY (`Spel_SpelID`,`Speler_SpelerID`),
  ADD KEY `fk_Spel_has_Speler_Speler1_idx` (`Speler_SpelerID`),
  ADD KEY `fk_Spel_has_Speler_Spel1_idx` (`Spel_SpelID`);

--
-- AUTO_INCREMENT voor geëxporteerde tabellen
--

--
-- AUTO_INCREMENT voor een tabel `bezit`
--
ALTER TABLE `bezit`
  MODIFY `BezitID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;
--
-- AUTO_INCREMENT voor een tabel `meting`
--
ALTER TABLE `meting`
  MODIFY `MetingID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;
--
-- AUTO_INCREMENT voor een tabel `sensor`
--
ALTER TABLE `sensor`
  MODIFY `SensorID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT voor een tabel `spel`
--
ALTER TABLE `spel`
  MODIFY `SpelID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT voor een tabel `speler`
--
ALTER TABLE `speler`
  MODIFY `SpelerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;
--
-- Beperkingen voor geëxporteerde tabellen
--

--
-- Beperkingen voor tabel `bezit`
--
ALTER TABLE `bezit`
  ADD CONSTRAINT `fk_Capture_spel1` FOREIGN KEY (`SpelID`) REFERENCES `spel` (`SpelID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Capture_speler1` FOREIGN KEY (`SpelerID`) REFERENCES `speler` (`SpelerID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Beperkingen voor tabel `meting`
--
ALTER TABLE `meting`
  ADD CONSTRAINT `fk_Meting_Sensor1` FOREIGN KEY (`SensorID`) REFERENCES `sensor` (`SensorID`);

--
-- Beperkingen voor tabel `spel_has_speler`
--
ALTER TABLE `spel_has_speler`
  ADD CONSTRAINT `fk_Spel_has_Speler_Spel1` FOREIGN KEY (`Spel_SpelID`) REFERENCES `spel` (`SpelID`),
  ADD CONSTRAINT `fk_Spel_has_Speler_Speler1` FOREIGN KEY (`Speler_SpelerID`) REFERENCES `speler` (`SpelerID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
