-- MySQL dump 10.13  Distrib 5.6.23, for Win64 (x86_64)
--
-- Host: localhost    Database: stocking
-- ------------------------------------------------------
-- Server version	5.6.23-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `live_300191`
--

DROP TABLE IF EXISTS `live_300191`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_300191` (
  `name` text,
  `open` text,
  `pre_close` text,
  `price` text,
  `high` text,
  `low` text,
  `bid` text,
  `ask` text,
  `volume` text,
  `amount` text,
  `b1_v` text,
  `b1_p` text,
  `b2_v` text,
  `b2_p` text,
  `b3_v` text,
  `b3_p` text,
  `b4_v` text,
  `b4_p` text,
  `b5_v` text,
  `b5_p` text,
  `a1_v` text,
  `a1_p` text,
  `a2_v` text,
  `a2_p` text,
  `a3_v` text,
  `a3_p` text,
  `a4_v` text,
  `a4_p` text,
  `a5_v` text,
  `a5_p` text,
  `date` text,
  `time` text,
  `code` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `live_300191`
--

LOCK TABLES `live_300191` WRITE;
/*!40000 ALTER TABLE `live_300191` DISABLE KEYS */;
INSERT INTO `live_300191` VALUES ('潜能恒信','24.500','22.780','24.500','24.500','24.500','24.380','24.500','1339400','32815300.000','40','24.380','2','24.320','300','24.310','5','24.300','13','24.280','1097','24.500','10','24.520','148','24.550','309','24.600','435','24.660','2018-04-04','09:29:03','300191'),('潜能恒信','24.500','22.780','24.480','24.500','24.300','24.320','24.480','1548100','37895687.000','6','24.320','553','24.300','33','24.280','10','24.240','2','24.220','708','24.480','8','24.490','1180','24.500','10','24.520','148','24.550','2018-04-04','09:30:03','300191'),('潜能恒信','24.500','22.780','24.680','24.850','24.300','24.660','24.680','2358700','57758604.000','1','24.660','7','24.600','38','24.560','27','24.540','11','24.530','254','24.680','15','24.850','10','24.860','216','24.870','19','24.880','2018-04-04','09:30:06','300191'),('潜能恒信','24.500','22.780','24.930','24.930','24.300','24.770','24.930','2571700','63005194.000','3','24.770','39','24.600','26','24.550','98','24.520','2','24.510','18','24.930','2','24.940','1','24.950','26','24.960','51','24.970','2018-04-04','09:30:09','300191');
/*!40000 ALTER TABLE `live_300191` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-06 14:46:43
