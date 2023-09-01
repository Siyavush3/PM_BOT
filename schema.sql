-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: arknet_pm_bot
-- ------------------------------------------------------
-- Server version	8.0.33-0ubuntu0.20.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `user_id` bigint NOT NULL,
  `task_id` bigint NOT NULL AUTO_INCREMENT,
  `task_text` text NOT NULL,
  `deadline` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `done` tinyint(1) NOT NULL,
  `close_time` time DEFAULT NULL,
  `color` varchar(255) DEFAULT NULL,
  `close_type` varchar(255) DEFAULT NULL,
  `close_comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1733672501,15,'Ggh','2023-07-06',1,'05:44:24',NULL,'Задача требует дополнительных ресурсов','Комментарий'),(1733672501,16,'Ggfbfg','2023-07-06',1,'05:44:40',NULL,'Другая','Комментарий'),(1733672501,26,'/show_all_tasks','2023-07-06',1,'21:00:11',NULL,'Другая','Комментарий'),(1733672501,27,'Желтый','2023-07-06',1,'21:07:11',NULL,'Задача требует дополнительных ресурсов','Комментарий'),(1733672501,28,'Зеленый','2023-07-06',1,'05:43:33','Желтый','Завершена Успешно','Комментарий'),(1733672501,29,'Описание','2023-07-06',1,'05:43:15','Желтый','Задача требует дополнительных ресурсов','Комментарий'),(179794457,30,'Заключить договор с Антариес, и уточнить с какого числа они будут платить','2023-07-06',0,NULL,'Красный',NULL,NULL),(179794457,37,'/done_task','2023-06-06',1,'05:05:06','/show_tasks','Завершена Успешно','Завершил'),(70485323,39,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,NULL,'Красный',NULL,NULL),(70485323,40,'развернуть два микротика и сделать тест L2tp, openvpn, wireguard, ospf  на внутренних интрефейсах через OVS и на внешних на скорость','2023-07-08',0,NULL,'Красный',NULL,NULL),(70485323,41,'после выполнения задачи 40 Нужно поднять 5ть микротиков один RP и два RPE и самые крайние CPE через mpls с CPE на CPE через vpls дать спедтест','2023-07-09',0,NULL,'Красный',NULL,NULL),(105553112,42,'Добавить ключевых сотрудников организации и провести тест бота','2023-07-07',1,'05:42:05','Красный','Завершена Успешно','Добавил женьку, макса, джамшида, бобра, раима, алишера, бехруза'),(1733672501,43,'Задача','2023-07-07',0,NULL,'Желтый',NULL,NULL);
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `tasks_insert_trigger` AFTER INSERT ON `tasks` FOR EACH ROW INSERT INTO tasks_log (task_id, user_id, task_text, deadline, done, timestamp)
VALUES (NEW.task_id, NEW.user_id, NEW.task_text, NEW.deadline, NEW.done, NOW()) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `tasks_update_trigger` AFTER UPDATE ON `tasks` FOR EACH ROW INSERT INTO tasks_log (task_id, user_id, task_text, deadline, done, timestamp)
VALUES (NEW.task_id, NEW.user_id, NEW.task_text, NEW.deadline, NEW.done, NOW()) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `tasks_log`
--

DROP TABLE IF EXISTS `tasks_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks_log` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `task_id` int DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  `task_text` varchar(255) DEFAULT NULL,
  `deadline` date DEFAULT NULL,
  `done` tinyint(1) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks_log`
--

LOCK TABLES `tasks_log` WRITE;
/*!40000 ALTER TABLE `tasks_log` DISABLE KEYS */;
INSERT INTO `tasks_log` VALUES (1,12,1733672501,'Задача','2023-07-01',0,'2023-06-30 10:47:40'),(2,12,5469004328,'Задача','2023-07-01',0,'2023-06-30 10:51:09'),(3,12,5469004328,'Задача','2023-07-03',0,'2023-06-30 10:51:09'),(4,12,5469004328,'Задача','2023-07-03',0,'2023-06-30 10:54:16'),(5,12,5469004328,'Задача','2023-07-03',0,'2023-06-30 10:54:16'),(6,13,1733672501,'Новая задача','2023-07-03',0,'2023-06-30 19:24:45'),(7,14,105553112,'Добавление пользователей','2023-07-01',0,'2023-06-30 19:58:34'),(8,14,105553112,'Добавление пользователей','2023-07-01',0,'2023-07-01 04:33:41'),(9,14,105553112,'Добавление пользователей','2023-07-02',0,'2023-07-01 04:33:41'),(10,14,105553112,'Добавление пользователей','2023-07-02',1,'2023-07-01 04:39:49'),(11,14,105553112,'Добавление пользователей','2023-07-02',1,'2023-07-01 04:39:49'),(12,15,1733672501,'Ggh','2023-07-06',0,'2023-07-05 19:33:19'),(13,16,1733672501,'Ggfbfg','2023-07-06',0,'2023-07-05 20:43:56'),(14,26,1733672501,'/show_all_tasks','2023-07-06',0,'2023-07-05 20:50:05'),(15,27,1733672501,'Желтый','2023-07-06',0,'2023-07-05 20:51:37'),(16,26,1733672501,'/show_all_tasks','2023-07-06',1,'2023-07-05 21:00:11'),(17,28,1733672501,'Зеленый','2023-07-06',0,'2023-07-05 21:03:09'),(18,27,1733672501,'Желтый','2023-07-06',1,'2023-07-05 21:07:11'),(19,29,1733672501,'Описание','2023-07-06',0,'2023-07-05 21:08:42'),(20,29,1733672501,'Описание','2023-07-06',1,'2023-07-06 05:43:15'),(21,28,1733672501,'Зеленый','2023-07-06',1,'2023-07-06 05:43:33'),(22,15,1733672501,'Ggh','2023-07-06',1,'2023-07-06 05:44:24'),(23,16,1733672501,'Ggfbfg','2023-07-06',1,'2023-07-06 05:44:40'),(24,30,105553112,'Заключить договор с Антариес, и уточнить с какого числа они будут платить','2023-07-06',0,'2023-07-06 07:36:01'),(25,30,105553112,'Заключить договор с Антариес, и уточнить с какого числа они будут платить','2023-07-06',0,'2023-07-06 07:41:17'),(26,30,105553112,'Заключить договор с Антариес, и уточнить с какого числа они будут платить','2023-07-06',0,'2023-07-06 07:41:17'),(27,37,179794457,'/done_task','2023-06-06',0,'2023-07-06 07:44:16'),(28,30,179794457,'Заключить договор с Антариес, и уточнить с какого числа они будут платить','2023-07-06',0,'2023-07-06 08:33:54'),(29,30,179794457,'Заключить договор с Антариес, и уточнить с какого числа они будут платить','2023-07-06',0,'2023-07-06 08:33:54'),(30,38,105553112,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:05:48'),(31,38,70485323,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:06:37'),(32,38,70485323,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:06:37'),(33,38,38,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:13:10'),(34,38,38,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:13:52'),(35,38,38,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:14:05'),(36,38,38,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:15:23'),(37,38,38,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:15:26'),(38,38,38,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:24:43'),(39,38,38,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:24:43'),(40,38,38,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:24:50'),(41,38,38,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:24:58'),(42,38,38,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:25:02'),(43,38,38,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:25:49'),(44,38,38,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-06 13:27:19'),(45,39,105553112,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-07 10:50:02'),(46,39,105553112,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-07 10:50:43'),(47,39,105553112,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-07 10:50:43'),(48,39,70485323,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-07 10:51:56'),(49,39,70485323,'Настроить и установить на pfsense хокимията wazuh','2023-07-07',0,'2023-07-07 10:51:56'),(50,40,105553112,'развернуть два микротика и сделать тест L2tp, openvpn, wireguard, ospf  на внутренних интрефейсах через OVS и на внешних на скорость','2023-07-08',0,'2023-07-07 13:26:13'),(51,40,70485323,'развернуть два микротика и сделать тест L2tp, openvpn, wireguard, ospf  на внутренних интрефейсах через OVS и на внешних на скорость','2023-07-08',0,'2023-07-07 13:27:44'),(52,40,70485323,'развернуть два микротика и сделать тест L2tp, openvpn, wireguard, ospf  на внутренних интрефейсах через OVS и на внешних на скорость','2023-07-08',0,'2023-07-07 13:27:44'),(53,41,105553112,'после выполнения задачи 40 Нужно поднять 5ть микротиков один RP и два RPE и самые крайние CPE через mpls с CPE на CPE через vpls дать спедтест','2023-07-09',0,'2023-07-07 13:28:54'),(54,41,70485323,'после выполнения задачи 40 Нужно поднять 5ть микротиков один RP и два RPE и самые крайние CPE через mpls с CPE на CPE через vpls дать спедтест','2023-07-09',0,'2023-07-07 13:29:20'),(55,41,70485323,'после выполнения задачи 40 Нужно поднять 5ть микротиков один RP и два RPE и самые крайние CPE через mpls с CPE на CPE через vpls дать спедтест','2023-07-09',0,'2023-07-07 13:29:20'),(56,42,105553112,'Добавить ключевых сотрудников организации и провести тест бота','2023-07-07',0,'2023-07-07 13:30:17'),(57,43,1733672501,'Задача','2023-07-07',0,'2023-07-07 17:17:59'),(58,37,179794457,'/done_task','2023-06-06',1,'2023-07-08 05:05:06'),(59,42,105553112,'Добавить ключевых сотрудников организации и провести тест бота','2023-07-07',1,'2023-07-08 05:42:05');
/*!40000 ALTER TABLE `tasks_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` bigint NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `reassign_allowed` int NOT NULL,
  `username` text NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (70485323,0,1,'Женька'),(105553112,1,1,'dm1n1str4t0r'),(108303586,0,1,'Ilkhom'),(179794457,0,1,'Alisher'),(303230207,0,1,'Bobir'),(1094410793,0,1,'Рахим'),(1315685797,0,1,'Бехруз🤩'),(1333892191,0,1,'Jamshid'),(1733672501,1,1,'dm1n1strat0r'),(5469004328,0,0,'Sell_materials');
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

-- Dump completed on 2023-07-11  9:24:22
