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
-- Table structure for table `live_300722`
--

DROP TABLE IF EXISTS `live_300722`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_300722` (
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
-- Dumping data for table `live_300722`
--

LOCK TABLES `live_300722` WRITE;
/*!40000 ALTER TABLE `live_300722` DISABLE KEYS */;
INSERT INTO `live_300722` VALUES ('新余国科','45.970','42.720','45.970','45.970','45.970','45.860','45.970','468700','21546139.000','10','45.860','30','45.850','16','45.530','5','45.500','80','45.320','784','45.970','8','45.980','491','45.990','2363','46.000','10','46.060','2018-04-04','09:29:03','300722'),('新余国科','45.970','42.720','45.970','45.970','45.530','45.710','45.970','523200','24046240.000','11','45.710','50','45.550','10','45.500','10','45.480','20','45.470','567','45.970','8','45.980','464','45.990','2273','46.000','10','46.060','2018-04-04','09:30:03','300722'),('新余国科','45.970','42.720','45.860','46.000','45.480','45.600','45.860','860300','39503144.000','6','45.600','82','45.580','4','45.550','40','45.530','20','45.520','6','45.860','2','45.970','1','45.990','1852','46.000','3','46.060','2018-04-04','09:30:06','300722'),('新余国科','45.970','42.720','46.000','46.000','45.480','45.990','46.000','955200','43862316.000','1','45.990','1','45.970','34','45.860','13','45.800','15','45.670','1487','46.000','3','46.060','5','46.080','1','46.100','6','46.120','2018-04-04','09:30:09','300722'),('新余国科','45.970','42.720','45.800','46.000','45.480','45.670','45.800','996900','45777189.000','3','45.670','4','45.660','65','45.610','3','45.600','70','45.580','2','45.800','2','45.830','5','45.960','40','45.990','1378','46.000','2018-04-04','09:30:12','300722'),('新余国科','45.970','42.720','45.980','46.000','45.480','45.970','45.980','1034800','47519127.000','2','45.970','6','45.860','1','45.670','4','45.660','65','45.610','3','45.980','2','45.990','1156','46.000','3','46.060','5','46.080','2018-04-04','09:30:15','300722'),('新余国科','45.970','42.720','46.000','46.000','45.480','45.970','46.000','1074800','49358537.000','15','45.970','7','45.860','61','45.610','3','45.600','70','45.580','823','46.000','3','46.060','5','46.080','1','46.100','6','46.120','2018-04-04','09:30:18','300722'),('新余国科','45.970','42.720','46.000','46.000','45.480','45.970','46.000','1092500','50172489.000','3','45.970','1','45.860','1','45.830','51','45.800','2','45.670','688','46.000','3','46.060','5','46.080','1','46.100','6','46.120','2018-04-04','09:30:21','300722'),('新余国科','45.970','42.720','46.000','46.000','45.480','45.800','46.000','1147700','52705177.000','2','45.800','28','45.690','3','45.670','4','45.660','61','45.610','504','46.000','3','46.060','5','46.080','1','46.100','6','46.120','2018-04-04','09:30:24','300722'),('新余国科','45.970','42.720','46.000','46.000','45.480','46.000','46.060','1201897','55198159.000','420','46.000','2','45.980','171','45.970','5','45.870','10','45.860','3','46.060','5','46.080','2','46.100','6','46.120','1','46.130','2018-04-04','09:30:27','300722'),('新余国科','45.970','42.720','46.120','46.120','45.480','46.090','46.120','1204297','55308727.000','40','46.090','3','46.060','2','46.050','31','46.020','1004','46.000','5','46.120','1','46.130','1','46.180','4','46.200','2','46.240','2018-04-04','09:30:30','300722'),('新余国科','45.970','42.720','46.500','46.580','45.480','46.500','46.580','1220097','56042211.000','1','46.500','1282','46.300','2','46.120','24','46.090','21','46.080','18','46.580','2','46.600','55','46.650','18','46.660','5','46.670','2018-04-04','09:30:33','300722'),('新余国科','45.970','42.720','46.650','46.650','45.480','46.650','46.660','1232897','56637360.000','45','46.650','13','46.500','1230','46.300','6','46.200','15','46.130','18','46.660','5','46.670','1','46.680','1','46.700','19','46.770','2018-04-04','09:30:36','300722');
/*!40000 ALTER TABLE `live_300722` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-06 14:47:10
