-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: testdatabase
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Current Database: `testdatabase`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `testdatabase` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `testdatabase`;

--
-- Table structure for table `admin_users`
--

DROP TABLE IF EXISTS `admin_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_users` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(10) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_users`
--

LOCK TABLES `admin_users` WRITE;
/*!40000 ALTER TABLE `admin_users` DISABLE KEYS */;
INSERT INTO `admin_users` VALUES (1,'admin','1234');
/*!40000 ALTER TABLE `admin_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fooditem`
--

DROP TABLE IF EXISTS `fooditem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fooditem` (
  `food_item_id` int NOT NULL AUTO_INCREMENT,
  `dish_name` varchar(50) DEFAULT NULL,
  `dish_description` varchar(2000) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`food_item_id`),
  UNIQUE KEY `dup` (`dish_name`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fooditem`
--

LOCK TABLES `fooditem` WRITE;
/*!40000 ALTER TABLE `fooditem` DISABLE KEYS */;
INSERT INTO `fooditem` VALUES (33,'Yangzhou Fried Rice','A popular Chinese dish featuring stir-fried rice, vegetables, and often meat or seafood. It\'s known for its flavorful combination of ingredients and its fluffy, well-cooked rice.  This dish is a staple in many Chinese restaurants and home kitchens. ',0),(34,'Avocado and Cucumber Salad','A refreshing and simple salad made with diced avocado and cucumber, often seasoned with salt, pepper, and a light vinaigrette. It\'s a perfect side dish for grilled meats or fish, or can be enjoyed on its own as a light and healthy meal.',1),(35,'Chicken Fried Rice','A popular Chinese dish consisting of stir-fried rice, chicken, vegetables, and eggs. It\'s often seasoned with soy sauce, salt, and pepper, creating a flavorful and satisfying meal.  The dish is typically served hot and can be customized with various ingredients. ',1),(39,'Egg Fried Rice','A popular Chinese dish consisting of stir-fried rice, eggs, and vegetables. It\'s often seasoned with soy sauce, salt, and pepper, and can be customized with various ingredients. A quick and flavorful meal enjoyed worldwide. ',1),(52,'Strawberry Milkshake','A classic summer treat, this milkshake is made with fresh strawberries, ice cream, and milk, blended until smooth and creamy. It\'s topped with whipped cream and a fresh strawberry for a sweet and refreshing indulgence.',1);
/*!40000 ALTER TABLE `fooditem` ENABLE KEYS */;
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
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_my_ingredients_after_status` AFTER UPDATE ON `fooditem` FOR EACH ROW BEGIN
    CALL update_my_ingredients_proc(NEW.status);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredients` (
  `ingredient_id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(20) DEFAULT NULL,
  `weight` decimal(15,3) DEFAULT NULL,
  `unit` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ingredient_id`),
  UNIQUE KEY `ingredient` (`ingredient`)
) ENGINE=InnoDB AUTO_INCREMENT=248 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredients`
--

LOCK TABLES `ingredients` WRITE;
/*!40000 ALTER TABLE `ingredients` DISABLE KEYS */;
INSERT INTO `ingredients` VALUES (214,'avocado',450.000,'g'),(215,'cucumber',400.000,'g'),(216,'parsley',30.000,'g'),(217,'salt',8.000,'g'),(218,'pepper',3.000,'g'),(224,'rice',200.000,'g'),(225,'chicken',100.000,'g'),(226,'greenchillies',10.000,'g'),(227,'carrot',10.000,'g'),(228,'onion',10.000,'g'),(229,'eggs',2.000,'nos'),(230,'soy sauce',20.000,'ml'),(233,'oil',10.000,'ml'),(238,'green onions',20.000,'g'),(239,'red bell pepper',20.000,'g'),(240,'vegetable oil',10.000,'ml'),(242,'garlic',1.000,'g'),(243,'ginger',1.000,'g'),(244,'milk',250.000,'ml'),(245,'strawberries',100.000,'g'),(246,'whipped cream',50.000,'g'),(247,'ice cream',100.000,'g');
/*!40000 ALTER TABLE `ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `my_ingredients`
--

DROP TABLE IF EXISTS `my_ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `my_ingredients` (
  `ingredient_id` int DEFAULT NULL,
  `my_ingredient` varchar(20) DEFAULT NULL,
  `weight` decimal(15,3) DEFAULT NULL,
  `unit` varchar(100) DEFAULT NULL,
  UNIQUE KEY `constraint_name` (`my_ingredient`),
  KEY `ingredient_id` (`ingredient_id`),
  CONSTRAINT `my_ingredients_ibfk_1` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`ingredient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `my_ingredients`
--

LOCK TABLES `my_ingredients` WRITE;
/*!40000 ALTER TABLE `my_ingredients` DISABLE KEYS */;
INSERT INTO `my_ingredients` VALUES (242,'garlic',6.000,'g'),(243,'ginger',1.000,'g'),(244,'milk',1.750,'L');
/*!40000 ALTER TABLE `my_ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `regular_users`
--

DROP TABLE IF EXISTS `regular_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `regular_users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(10) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regular_users`
--

LOCK TABLES `regular_users` WRITE;
/*!40000 ALTER TABLE `regular_users` DISABLE KEYS */;
INSERT INTO `regular_users` VALUES (1,'abcd','1234');
/*!40000 ALTER TABLE `regular_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shoppinglist`
--

DROP TABLE IF EXISTS `shoppinglist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shoppinglist` (
  `ingredient_id` int DEFAULT NULL,
  `weight` decimal(15,3) DEFAULT NULL,
  `unit` varchar(100) DEFAULT NULL,
  KEY `ingredient_id` (`ingredient_id`),
  CONSTRAINT `shoppinglist_ibfk_1` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`ingredient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shoppinglist`
--

LOCK TABLES `shoppinglist` WRITE;
/*!40000 ALTER TABLE `shoppinglist` DISABLE KEYS */;
INSERT INTO `shoppinglist` VALUES (214,450.000,'g'),(215,400.000,'g'),(216,30.000,'g'),(217,8.000,'g'),(218,3.000,'g'),(224,100.000,'g'),(225,100.000,'g'),(226,10.000,'g'),(227,10.000,'g'),(228,10.000,'g'),(229,2.000,'nos'),(230,20.000,'ml'),(233,10.000,'ml'),(238,20.000,'g'),(239,20.000,'g'),(240,10.000,'ml'),(244,250.000,'ml'),(245,100.000,'g'),(246,50.000,'g'),(247,100.000,'g');
/*!40000 ALTER TABLE `shoppinglist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'testdatabase'
--
/*!50003 DROP PROCEDURE IF EXISTS `update_my_ingredients_proc` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_my_ingredients_proc`(IN ingredient_status INT)
BEGIN
    IF ingredient_status = 1 THEN
        UPDATE my_ingredients mi
        INNER JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
        INNER JOIN (
            SELECT ingredient_id, weight AS original_weight 
            FROM my_ingredients
        ) orig ON orig.ingredient_id = mi.ingredient_id
        SET
            mi.weight = CASE
                WHEN mi.weight > i.weight AND mi.unit = i.unit THEN mi.weight - i.weight
                WHEN mi.weight <= i.weight AND mi.unit = i.unit THEN 0
                WHEN mi.weight < i.weight AND i.unit = 'g' AND mi.unit = 'kg' THEN 
                    CASE 
                        WHEN mi.weight - (i.weight / 1000) >= 1 THEN mi.weight - (i.weight / 1000)
                        WHEN mi.weight - (i.weight / 1000) < 1 THEN (mi.weight - (i.weight / 1000)) * 1000
                    END
                WHEN mi.weight < i.weight AND i.unit = 'kg' AND mi.unit = 'g' THEN 0
                WHEN mi.weight < i.weight AND i.unit = 'ml' AND mi.unit = 'L' THEN 
                    CASE 
                        WHEN mi.weight - (i.weight / 1000) >= 1 THEN mi.weight - (i.weight / 1000)
                        WHEN mi.weight - (i.weight / 1000) < 1 THEN (mi.weight - (i.weight / 1000)) * 1000
                    END
				WHEN mi.weight < i.weight AND i.unit = 'L' AND mi.unit = 'ml' THEN 0
                ELSE mi.weight
            END,
            mi.unit = CASE
                WHEN i.unit = 'g' AND mi.unit = 'kg' AND (orig.original_weight - (i.weight / 1000)) < 1.000 THEN 'g'
                WHEN i.unit = 'g' AND mi.unit = 'kg' AND (orig.original_weight - (i.weight / 1000)) >= 1.000 THEN 'kg'
                WHEN mi.unit = 'g' AND i.unit = 'kg' THEN 'g'
                WHEN i.unit = 'ml' AND mi.unit = 'L' AND (orig.original_weight - (i.weight / 1000)) < 1.000 THEN 'ml'
                WHEN i.unit = 'ml' AND mi.unit = 'L' AND (orig.original_weight - (i.weight / 1000)) >= 1.000 THEN 'L'
                WHEN mi.unit = 'ml' AND i.unit = 'L' THEN 'ml'
                WHEN mi.unit = i.unit THEN mi.unit
                ELSE mi.unit
            END
        WHERE mi.ingredient_id = i.ingredient_id;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-05 14:06:59
