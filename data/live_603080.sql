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
-- Table structure for table `live_603080`
--

DROP TABLE IF EXISTS `live_603080`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_603080` (
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
-- Dumping data for table `live_603080`
--

LOCK TABLES `live_603080` WRITE;
/*!40000 ALTER TABLE `live_603080` DISABLE KEYS */;
INSERT INTO `live_603080` VALUES ('新疆火炬','35.850','33.670','35.850','35.850','35.850','35.800','35.850','673900','24159315.000','1','35.800','3','35.750','2','35.720','31','35.700','2','35.690','316','35.850','15','35.880','20','35.900','70','35.950','152','35.980','2018-04-04','09:29:41','603080'),('新疆火炬','35.850','33.670','36.000','36.550','35.350','36.000','36.550','1603205','57496729.000','64','36.000','5','35.990','6','35.980','3','35.950','5','35.940','63','36.550','17','36.560','3','36.580','31','36.600','5','36.610','2018-04-04','09:30:05','603080'),('新疆火炬','35.850','33.670','35.940','36.660','35.350','35.940','36.660','1648505','59138223.000','5','35.940','10','35.920','22','35.910','290','35.900','4','35.890','67','36.660','11','36.670','5','36.680','31','36.690','38','36.700','2018-04-04','09:30:08','603080'),('新疆火炬','35.850','33.670','36.670','36.670','35.350','35.900','36.670','1688805','60592116.000','160','35.900','4','35.890','85','35.880','96','35.870','118','35.860','9','36.670','5','36.680','31','36.690','38','36.700','10','36.750','2018-04-04','09:30:09','603080'),('新疆火炬','35.850','33.670','36.340','36.780','35.350','36.340','36.780','1724905','61908348.000','21','36.340','3','36.080','1','36.020','50','36.000','4','35.990','12','36.780','183','36.790','203','36.800','7','36.810','2','36.830','2018-04-04','09:30:14','603080'),('新疆火炬','35.850','33.670','36.790','36.790','35.350','36.670','36.790','1766405','63429533.000','111','36.670','2','36.660','2','36.550','10','36.500','1','36.490','72','36.790','213','36.800','7','36.810','2','36.830','47','36.850','2018-04-04','09:30:15','603080');
/*!40000 ALTER TABLE `live_603080` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-06 14:47:35
