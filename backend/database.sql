-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 147.229.177.177    Database: dbikryty
-- ------------------------------------------------------
-- Server version	8.0.34-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `buildingsubtype`
--

DROP TABLE IF EXISTS `buildingsubtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buildingsubtype` (
  `id` int NOT NULL AUTO_INCREMENT,
  `caption` varchar(256) NOT NULL,
  `building_type_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_building_building_f4ca3fe3` (`building_type_id`),
  CONSTRAINT `fk_building_building_f4ca3fe3` FOREIGN KEY (`building_type_id`) REFERENCES `buildingtype` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buildingsubtype`
--

LOCK TABLES `buildingsubtype` WRITE;
/*!40000 ALTER TABLE `buildingsubtype` DISABLE KEYS */;
INSERT INTO `buildingsubtype` VALUES (1,'Bytový dům zděný',4),(2,'Panelový dům',4),(3,'Dům pro seniory',4),(4,'Rodinný dům / Vila',4),(5,'Chaty a chalupy',4),(6,'Základní / Střední /Vysoká škola',1),(7,'Zdravotnické zařízení (nemocnice/kliniky)',1),(8,'Obchodní centra a obchody',1),(9,'Restaurace a Kavárny',1),(10,'Sportovní zařízení',1),(11,'Kulturní centra a galerie',1),(12,'Administrativní budovy/Banky a pojišťovny',1),(13,'Knihovny a studovny',1),(14,'Muzea',1),(15,'Kostely, modlitebny',1),(16,'Rekreační zařízení',1),(17,'Výrobní haly lehkého průmyslu',2),(18,'Sklady a distribuční centra',2),(19,'Administrativní budovy',2),(20,'Tunely',3),(21,'Podchody',3),(22,'Metro a podzemní dráhy (stanice + dráha)',3),(23,'Garáže',3),(24,'Letištní terminály',3),(25,'Železniční stanice',3),(26,'Autobusové nádraží',3);
/*!40000 ALTER TABLE `buildingsubtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `buildingtype`
--

DROP TABLE IF EXISTS `buildingtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buildingtype` (
  `id` int NOT NULL AUTO_INCREMENT,
  `caption` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buildingtype`
--

LOCK TABLES `buildingtype` WRITE;
/*!40000 ALTER TABLE `buildingtype` DISABLE KEYS */;
INSERT INTO `buildingtype` VALUES (1,'Stavby občanské vybavenosti'),(2,'Průmyslové stavby'),(3,'Dopravní stavby'),(4,'Stavby pro bydlení');
/*!40000 ALTER TABLE `buildingtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materialsubtype`
--

DROP TABLE IF EXISTS `materialsubtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materialsubtype` (
  `id` int NOT NULL AUTO_INCREMENT,
  `caption` varchar(256) NOT NULL,
  `material_type_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_material_material_91f0af43` (`material_type_id`),
  CONSTRAINT `fk_material_material_91f0af43` FOREIGN KEY (`material_type_id`) REFERENCES `materialtype` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materialsubtype`
--

LOCK TABLES `materialsubtype` WRITE;
/*!40000 ALTER TABLE `materialsubtype` DISABLE KEYS */;
INSERT INTO `materialsubtype` VALUES (1,'kvádrové',2),(3,'lomové',2),(4,'bez malty (na sucho)',2),(5,'Cihla plná pálená',3),(6,'Cihla děrovaná pálená',3),(7,'Tvárnice lehká (Porotherm…)',3),(8,'Prostý',4),(9,'Armovaný (železobeton)',4),(10,'Škvárový',4),(11,'Plynosilikáty – (YTONG, HEBEL…)',4),(12,'Hliník',7),(13,'Ocel',7),(14,'Měď',7),(15,'Kompozitní panely s hliníkovým jádrem',8),(16,'Skleněná vláknocementová kompozitní deska',8),(17,'Keramický kompozitní materiál',8),(18,'Kompozitní materiál s organickým vláknem',8),(19,'Nanokompozity',8),(20,'Grafenové kompozity',8),(21,'Tvrdé',10),(22,'Měkké',10);
/*!40000 ALTER TABLE `materialsubtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materialtype`
--

DROP TABLE IF EXISTS `materialtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materialtype` (
  `id` int NOT NULL AUTO_INCREMENT,
  `caption` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materialtype`
--

LOCK TABLES `materialtype` WRITE;
/*!40000 ALTER TABLE `materialtype` DISABLE KEYS */;
INSERT INTO `materialtype` VALUES (2,'Zdivo kamenné'),(3,'Zdivo z cihel'),(4,'Beton'),(5,'Hlína'),(6,'Písek suchý'),(7,'Kov'),(8,'Kompozitní materiály'),(9,'Škvára upěchovaná'),(10,'Dřevo');
/*!40000 ALTER TABLE `materialtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `protectivespace`
--

DROP TABLE IF EXISTS `protectivespace`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `protectivespace` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` int NOT NULL,
  `width` double NOT NULL,
  `height` double NOT NULL,
  `depth` double NOT NULL,
  `thickness` double NOT NULL,
  `material_subtype_id` int NOT NULL,
  `shelter_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_protecti_material_d2f4483a` (`material_subtype_id`),
  KEY `fk_protecti_shelters_d7b9b949` (`shelter_id`),
  CONSTRAINT `fk_protecti_material_d2f4483a` FOREIGN KEY (`material_subtype_id`) REFERENCES `materialsubtype` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_protecti_shelters_d7b9b949` FOREIGN KEY (`shelter_id`) REFERENCES `shelters` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protectivespace`
--

LOCK TABLES `protectivespace` WRITE;
/*!40000 ALTER TABLE `protectivespace` DISABLE KEYS */;
INSERT INTO `protectivespace` VALUES (3,2,2,25,20,30,12,4),(5,2,1,1,1,1,1,6),(6,1,5,2,5,30,5,7),(7,3,5,2,5,40,6,8),(8,3,2,2,5,40,1,9),(9,3,4,1,2,10,1,10);
/*!40000 ALTER TABLE `protectivespace` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shelters`
--

DROP TABLE IF EXISTS `shelters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shelters` (
  `id` int NOT NULL AUTO_INCREMENT,
  `address` varchar(256) NOT NULL,
  `x` double NOT NULL,
  `y` double NOT NULL,
  `building_subtype_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_shelters_building_c6a0993f` (`building_subtype_id`),
  KEY `fk_shelters_users_644f389b` (`user_id`),
  CONSTRAINT `fk_shelters_building_c6a0993f` FOREIGN KEY (`building_subtype_id`) REFERENCES `buildingsubtype` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_shelters_users_644f389b` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shelters`
--

LOCK TABLES `shelters` WRITE;
/*!40000 ALTER TABLE `shelters` DISABLE KEYS */;
INSERT INTO `shelters` VALUES (4,'675/119, Jugoslávská, Štefánikova čtvrť, Černá Pole, Brno, okres Brno-město, Jihomoravský kraj, Jihovýchod, 613 00, Česko',49.2134148,16.6223949,3,3),(6,'677/121, Jugoslávská, Štefánikova čtvrť, Černá Pole, Brno, okres Brno-město, Jihomoravský kraj, Jihovýchod, 613 00, Česko',49.2135634,16.6223885,7,3),(7,'673/117, Jugoslávská, Štefánikova čtvrť, Černá Pole, Brno, okres Brno-město, Jihomoravský kraj, Jihovýchod, 613 00, Česko',49.2132962,16.6224526,4,3),(8,'671/115, Jugoslávská, Štefánikova čtvrť, Černá Pole, Brno, okres Brno-město, Jihomoravský kraj, Jihovýchod, 613 00, Česko',49.2132243,16.6224453,4,3),(9,'Adresa 1',49.21430325995331,16.64263486862183,1,3),(10,'ghfgh',49.52899673717214,16.638793945312504,7,3);
/*!40000 ALTER TABLE `shelters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(128) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `modified_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `last_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'iklima@fit.vutbr.cz','Ondřej','$2b$12$WH0LILpP2Eq7WBMyZXdEpO3kMztg9lOTlLFhi.ISd2E5hvabIn0zm','2023-07-19 13:32:17.892842','2023-07-30 13:03:09.713197','Klíma'),(2,'klima@seznam.cz','Ondřej','$2b$12$PdtMTJ1alPbz/jSGwY/3teh/gobeRudn0N.KkdYzoL0deQq7o2L4.','2023-07-30 15:02:09.650928','2023-07-30 15:02:09.650928','Klíma'),(3,'ondra.klima@seznam.cz','Ondřej','$2b$12$cxUy2nIZIhbPt5hlorikxuc6Oq3WK7IOnUNP9nBzhwLoXy4LYkepm','2023-07-30 15:06:45.449059','2023-07-30 15:06:45.449059','Klíma'),(6,'ondra2@seznam.cz','Ondřej','$2b$12$FX19Zk5iKwT8uQssp32iaO5elhsZcoR0RVssHZi6ZxyVguJUH.53S','2023-07-30 15:09:27.459596','2023-07-30 15:09:27.459596','Klíma'),(10,'john@dow.com','John','$2b$12$xbTCROti/CiFKKsmg2dbu.Y1l5Qp8WBBxC8lvbyH0XprMaJM2rtBq','2023-07-31 13:01:39.354340','2023-07-31 13:01:39.354358','Dow'),(12,'dabler@gmail.com','David','$2b$12$MdUtxoI09GN9yGdhZ/MrqeSkayLK17XE1VPbTRsBOGdA5ZBS7S3Qq','2023-08-17 16:07:26.051136','2023-08-17 16:07:26.051150','Bařina');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-22 13:41:02
