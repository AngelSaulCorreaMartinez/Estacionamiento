CREATE DATABASE  IF NOT EXISTS `parking` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `parking`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: parking
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `estacionamiento_entrada`
--

DROP TABLE IF EXISTS `estacionamiento_entrada`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estacionamiento_entrada` (
  `id_carro` int NOT NULL,
  `Hora_Entrada` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estacionamiento_entrada`
--

LOCK TABLES `estacionamiento_entrada` WRITE;
/*!40000 ALTER TABLE `estacionamiento_entrada` DISABLE KEYS */;
INSERT INTO `estacionamiento_entrada` VALUES (2,'2024-07-04 11:00:26'),(3,'2024-07-04 11:58:32'),(5,'2024-07-04 11:39:52'),(8,'2024-07-04 11:58:09'),(16,'2024-07-04 11:57:33'),(27,'2024-07-04 11:39:57'),(2,'2024-07-04 12:05:16'),(2,'2024-07-04 12:05:16'),(35,'2024-07-04 12:05:22'),(35,'2024-07-04 12:05:22'),(35,'2024-07-04 12:05:22'),(97,'2024-07-04 12:05:39'),(97,'2024-07-04 12:05:39'),(175,'2024-07-04 12:06:04'),(204,'2024-07-04 12:06:11'),(12,'2024-07-04 12:21:17'),(16,'2024-07-04 12:29:45'),(8,'2024-07-04 12:32:47'),(9,'2024-07-04 12:36:06');
/*!40000 ALTER TABLE `estacionamiento_entrada` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estacionamiento_salida`
--

DROP TABLE IF EXISTS `estacionamiento_salida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estacionamiento_salida` (
  `id_carro` int NOT NULL,
  `Hora_Salida` varchar(45) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estacionamiento_salida`
--

LOCK TABLES `estacionamiento_salida` WRITE;
/*!40000 ALTER TABLE `estacionamiento_salida` DISABLE KEYS */;
INSERT INTO `estacionamiento_salida` VALUES (17,'2024-07-04 12:29:48'),(17,'2024-07-04 12:29:48'),(6,'2024-07-04 12:32:44'),(6,'2024-07-04 12:34:26'),(4,'2024-07-04 12:36:00'),(4,'2024-07-04 12:36:00');
/*!40000 ALTER TABLE `estacionamiento_salida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `niveles`
--

DROP TABLE IF EXISTS `niveles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `niveles` (
  `id_Cajon` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `Hora_Salida` datetime NOT NULL,
  `Hora_Entrada` datetime NOT NULL,
  `Disponibilidad` varchar(45) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `niveles`
--

LOCK TABLES `niveles` WRITE;
/*!40000 ALTER TABLE `niveles` DISABLE KEYS */;
INSERT INTO `niveles` VALUES ('20','2024-07-01 04:00:36','2002-10-23 14:00:00','');
/*!40000 ALTER TABLE `niveles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `Correo` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `Tipo_Usuario` int NOT NULL,
  `Contraseña` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`Correo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-04 15:08:08
