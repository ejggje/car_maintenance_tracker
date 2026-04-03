-- MySQL dump 10.13  Distrib 8.0.45, for macos15 (x86_64)
--
-- Host: localhost    Database: car_maintenance
-- ------------------------------------------------------
-- Server version	9.6.0

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'f11e1d86-248f-11f1-8fd4-a87963846d98:1-22';

--
-- Table structure for table `maintenance_record`
--

DROP TABLE IF EXISTS `maintenance_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenance_record` (
  `maintenance_record_id` int NOT NULL AUTO_INCREMENT,
  `vehicle_id` int NOT NULL,
  `maintenance_type_id` int NOT NULL,
  `facility_id` int DEFAULT NULL,
  `service_date` date NOT NULL,
  `mileage_at_service` int NOT NULL,
  `cost` decimal(10,2) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`maintenance_record_id`),
  KEY `vehicle_id` (`vehicle_id`),
  KEY `maintenance_type_id` (`maintenance_type_id`),
  KEY `facility_id` (`facility_id`),
  CONSTRAINT `maintenance_record_ibfk_1` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle` (`vehicle_id`),
  CONSTRAINT `maintenance_record_ibfk_2` FOREIGN KEY (`maintenance_type_id`) REFERENCES `maintenance_type` (`maintenance_type_id`),
  CONSTRAINT `maintenance_record_ibfk_3` FOREIGN KEY (`facility_id`) REFERENCES `service_facility` (`facility_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenance_record`
--

LOCK TABLES `maintenance_record` WRITE;
/*!40000 ALTER TABLE `maintenance_record` DISABLE KEYS */;
INSERT INTO `maintenance_record` VALUES (1,1,1,1,'2024-11-01',30000,49.99,'Conventional oil, no issues'),(2,2,2,2,'2024-10-15',50000,29.99,'All tires rotated'),(3,3,3,3,'2024-09-20',39000,89.99,'Front brakes replaced'),(4,4,4,4,'2024-08-05',75000,34.99,'Both filters replaced'),(5,5,1,NULL,'2025-01-10',14000,NULL,'Self-performed oil change'),(6,6,1,6,'2024-01-15',25000,89.99,'Full coolant flush completed'),(7,7,2,7,'2024-02-20',58000,120.00,'All 4 spark plugs replaced'),(8,8,3,8,'2024-03-10',43000,199.99,'New battery installed'),(9,9,4,9,'2024-04-05',36000,79.99,'Four wheel alignment done'),(10,10,5,10,'2024-05-12',20000,24.99,'Both wiper blades replaced'),(11,11,6,6,'2024-06-18',80000,29.99,'Cabin filter replaced'),(12,12,7,7,'2024-07-22',15000,109.99,'Power steering flush done'),(13,13,8,8,'2024-08-30',31000,89.99,'Differential fluid replaced'),(14,14,1,9,'2024-09-14',53000,89.99,'Coolant flush completed'),(15,15,2,10,'2024-10-01',39000,115.00,'Spark plugs replaced'),(16,1,6,1,'2024-10-15',32500,34.99,'Engine air filter replaced'),(17,2,4,2,'2024-11-02',51500,79.99,'Alignment corrected'),(18,3,5,3,'2024-11-20',40500,22.99,'Wiper blades replaced'),(19,4,3,4,'2024-12-05',77500,189.99,'Battery replaced under warranty'),(20,5,7,5,'2024-12-18',14500,99.99,'Power steering service done'),(21,6,9,6,'2025-01-08',26000,49.99,'Fuel filter replaced'),(22,7,10,7,'2025-01-25',59500,149.99,'AC recharged for summer'),(23,8,1,8,'2025-02-14',44500,89.99,'Coolant flush done'),(24,9,6,9,'2025-03-01',37500,29.99,'Cabin filter replaced'),(25,10,4,10,'2025-03-20',21500,79.99,'Wheel alignment adjusted');
/*!40000 ALTER TABLE `maintenance_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenance_type`
--

DROP TABLE IF EXISTS `maintenance_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenance_type` (
  `maintenance_type_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `default_interval_miles` int DEFAULT NULL,
  `default_interval_days` int DEFAULT NULL,
  PRIMARY KEY (`maintenance_type_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenance_type`
--

LOCK TABLES `maintenance_type` WRITE;
/*!40000 ALTER TABLE `maintenance_type` DISABLE KEYS */;
INSERT INTO `maintenance_type` VALUES (1,'Oil Change','Replace engine oil and filter',5000,180),(2,'Tire Rotation','Rotate tires for even wear',7500,180),(3,'Brake Inspection','Inspect brake pads and rotors',12000,365),(4,'Air Filter Replacement','Replace cabin and engine air filters',15000,365),(5,'Transmission Service','Flush and replace transmission fluid',30000,730),(6,'Coolant Flush','Flush and replace engine coolant',30000,730),(7,'Spark Plug Replacement','Replace spark plugs for optimal engine performance',30000,1095),(8,'Battery Replacement','Replace vehicle battery',50000,1460),(9,'Wheel Alignment','Align wheels to manufacturer specifications',12000,365),(10,'Wiper Blade Replacement','Replace front and rear wiper blades',10000,365),(11,'Cabin Air Filter','Replace cabin air filter',15000,365),(12,'Power Steering Flush','Flush and replace power steering fluid',50000,730),(13,'Differential Service','Replace differential fluid',30000,730),(14,'Fuel Filter Replacement','Replace fuel filter',20000,730),(15,'AC Service','Inspect and recharge air conditioning system',20000,730),(16,'Timing Belt Replacement','Replace timing belt and tensioner',60000,1825),(17,'CV Axle Replacement','Replace CV axle boots or full axle',80000,0),(18,'Serpentine Belt Replacement','Replace serpentine belt',50000,1460),(19,'Shock Absorber Replacement','Replace front or rear shock absorbers',50000,0),(20,'Exhaust System Inspection','Inspect exhaust system for leaks or damage',15000,365);
/*!40000 ALTER TABLE `maintenance_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_facility`
--

DROP TABLE IF EXISTS `service_facility`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_facility` (
  `facility_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `address` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `website` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`facility_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_facility`
--

LOCK TABLES `service_facility` WRITE;
/*!40000 ALTER TABLE `service_facility` DISABLE KEYS */;
INSERT INTO `service_facility` VALUES (1,'Jiffy Lube','123 Main St, Blacksburg, VA','540-555-0101','www.jiffylube.com'),(2,'Firestone Complete Auto Care','456 Oak Ave, Blacksburg, VA','540-555-0102','www.firestone.com'),(3,'Valvoline Instant Oil Change','789 Elm St, Christiansburg, VA','540-555-0103','www.valvoline.com'),(4,'Pep Boys','321 College Ave, Blacksburg, VA','540-555-0104','www.pepboys.com'),(5,'NTB Tire & Service','654 Price Fork Rd, Blacksburg, VA','540-555-0105','www.ntb.com'),(6,'Midas Auto Service','987 University Ave, Blacksburg, VA','540-555-0106','www.midas.com'),(7,'Monro Muffler Brake','147 Main Street, Radford, VA','540-555-0107','www.monro.com'),(8,'Goodyear Auto Service','258 Prices Fork Rd, Blacksburg, VA','540-555-0108','www.goodyear.com'),(9,'Sears Auto Center','369 South Main St, Christiansburg, VA','540-555-0109','www.searsauto.com'),(10,'Christian Brothers Auto','741 Patrick Henry Dr, Blacksburg, VA','540-555-0110','www.cbac.com'),(11,'Mavis Discount Tire','852 Roanoke St, Christiansburg, VA','540-555-0111','www.mavistire.com'),(12,'Advance Auto Parts','963 University City Blvd, Blacksburg, VA','540-555-0112','www.advanceautoparts.com'),(13,'O\'Reilly Auto Parts','159 Main St, Blacksburg, VA','540-555-0113','www.oreillyauto.com'),(14,'AAA Car Care','357 Prices Fork Rd, Blacksburg, VA','540-555-0114','www.aaa.com'),(15,'Dealer Service Center','468 University Ave, Blacksburg, VA','540-555-0115','www.dealerservice.com');
/*!40000 ALTER TABLE `service_facility` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Erik','Garcia','ejggje@vt.edu','hash1','owner',1),(2,'Shamit','Pradhan','shamit22@vt.edu','hash2','owner',1),(3,'Keegan','McFadden','keeganm@vt.edu','hash3','owner',1),(4,'Tim','Wilson','timwilson@vt.edu','hash4','owner',1),(5,'Jane','Doe','janedoe@email.com','hash5','servicer',1),(6,'Alice','Johnson','alice.j@email.com','hash6','owner',1),(7,'Bob','Smith','bob.smith@email.com','hash7','owner',1),(8,'Carol','Williams','carol.w@email.com','hash8','owner',1),(9,'David','Brown','david.b@email.com','hash9','owner',1),(10,'Emma','Davis','emma.d@email.com','hash10','owner',1),(11,'Frank','Miller','frank.m@email.com','hash11','servicer',1),(12,'Grace','Wilson','grace.w@email.com','hash12','owner',1),(13,'Henry','Moore','henry.m@email.com','hash13','owner',1),(14,'Isabella','Taylor','isabella.t@email.com','hash14','owner',1),(15,'James','Anderson','james.a@email.com','hash15','servicer',1),(16,'Karen','Thomas','karen.t@email.com','hash16','owner',1),(17,'Liam','Jackson','liam.j@email.com','hash17','owner',1),(18,'Mia','White','mia.w@email.com','hash18','owner',1),(19,'Noah','Harris','noah.h@email.com','hash19','owner',1),(20,'Olivia','Martin','olivia.m@email.com','hash20','owner',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle` (
  `vehicle_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `vin` varchar(17) NOT NULL,
  `make` varchar(50) NOT NULL,
  `model` varchar(50) NOT NULL,
  `year` int NOT NULL,
  `current_mileage` int NOT NULL,
  PRIMARY KEY (`vehicle_id`),
  UNIQUE KEY `vin` (`vin`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `vehicle_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle`
--

LOCK TABLES `vehicle` WRITE;
/*!40000 ALTER TABLE `vehicle` DISABLE KEYS */;
INSERT INTO `vehicle` VALUES (1,1,'1HGBH41JXMN109186','Honda','Civic',2021,34000),(2,2,'2T1BURHE0JC043821','Toyota','Corolla',2019,52000),(3,3,'3VWFE21C04M000001','Volkswagen','Jetta',2020,41000),(4,4,'1FTFW1ET5DKE12345','Ford','F-150',2018,78000),(5,1,'5YJSA1DN1DFP14736','Tesla','Model S',2022,15000),(6,6,'1G1ZT53806F109327','Chevrolet','Malibu',2020,28000),(7,7,'2HGFG12567H123456','Honda','Accord',2018,61000),(8,8,'3FADP4EJ5EM123456','Ford','Fiesta',2017,45000),(9,9,'1FTEX1EM9EF123456','Ford','Ranger',2019,38000),(10,10,'WAUFFAFL5DN123456','Audi','A4',2021,22000),(11,11,'1N4AL3AP9FC123456','Nissan','Altima',2016,82000),(12,12,'JF2SJAEC5GH123456','Subaru','Forester',2022,17000),(13,13,'5NPE24AF1FH123456','Hyundai','Sonata',2020,33000),(14,14,'2T1BURHE4JC123456','Toyota','Camry',2018,55000),(15,15,'1HGCR2F3XFA123456','Honda','Accord',2019,41000),(16,16,'KNDJN2A24G7123456','Kia','Soul',2017,67000),(17,17,'1C4RJFAG0FC123456','Jeep','Grand Cherokee',2021,29000),(18,18,'WBA3A5C51CF123456','BMW','328i',2016,74000),(19,19,'1GNKVGED0BJ123456','Chevrolet','Traverse',2020,36000),(20,20,'4T1BF1FK5EU123456','Toyota','Camry',2023,8000);
/*!40000 ALTER TABLE `vehicle` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-03 13:37:12
