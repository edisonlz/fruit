-- MySQL dump 10.13  Distrib 5.6.13, for osx10.7 (x86_64)
--
-- Host: localhost    Database: fruit
-- ------------------------------------------------------
-- Server version	5.6.13

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add content type',3,'add_contenttype'),(8,'Can change content type',3,'change_contenttype'),(9,'Can delete content type',3,'delete_contenttype'),(10,'Can add session',4,'add_session'),(11,'Can change session',4,'change_session'),(12,'Can delete session',4,'delete_session'),(13,'Can add log entry',5,'add_logentry'),(14,'Can change log entry',5,'change_logentry'),(15,'Can delete log entry',5,'delete_logentry'),(16,'Can add migration history',6,'add_migrationhistory'),(17,'Can change migration history',6,'change_migrationhistory'),(18,'Can delete migration history',6,'delete_migrationhistory'),(19,'Can add 首页盒子',7,'add_box'),(20,'Can change 首页盒子',7,'change_box'),(21,'Can delete 首页盒子',7,'delete_box'),(22,'Can add item category',8,'add_itemcategory'),(23,'Can change item category',8,'change_itemcategory'),(24,'Can delete item category',8,'delete_itemcategory'),(25,'Can add 促销类型',9,'add_itempromote'),(26,'Can change 促销类型',9,'change_itempromote'),(27,'Can delete 促销类型',9,'delete_itempromote'),(28,'Can add 促销类型',10,'add_item'),(29,'Can change 促销类型',10,'change_item'),(30,'Can delete 促销类型',10,'delete_item'),(31,'Can add 提货点',11,'add_shoppingaddress'),(32,'Can change 提货点',11,'change_shoppingaddress'),(33,'Can delete 提货点',11,'delete_shoppingaddress'),(34,'Can add user',12,'add_user'),(35,'Can change user',12,'change_user'),(36,'Can delete user',12,'delete_user'),(37,'Can add 盒子水果',13,'add_boxitem'),(38,'Can change 盒子水果',13,'change_boxitem'),(39,'Can delete 盒子水果',13,'delete_boxitem'),(43,'Can add 城市',15,'add_city'),(44,'Can change 城市',15,'change_city'),(45,'Can delete 城市',15,'delete_city'),(46,'Can add 商品图片',16,'add_itemimage'),(47,'Can change 商品图片',16,'change_itemimage'),(48,'Can delete 商品图片',16,'delete_itemimage'),(49,'Can add 商品图片标签',17,'add_imagetag'),(50,'Can change 商品图片标签',17,'change_imagetag'),(51,'Can delete 商品图片标签',17,'delete_imagetag');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_box`
--

DROP TABLE IF EXISTS `content_box`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_box` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `title` varchar(100) NOT NULL,
  `position` int(11) NOT NULL,
  `iner_count` int(11) NOT NULL,
  `box_type` int(11) NOT NULL,
  `shop_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `content_box_5654bf12` (`state`),
  KEY `content_box_a59e4220` (`is_delete`),
  KEY `content_box_1f456125` (`position`),
  KEY `content_box_ae633a4e` (`box_type`),
  KEY `content_box_74d4252d` (`shop_id`),
  CONSTRAINT `shop_id_refs_id_89615131` FOREIGN KEY (`shop_id`) REFERENCES `content_shoppingaddress` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_box`
--

LOCK TABLES `content_box` WRITE;
/*!40000 ALTER TABLE `content_box` DISABLE KEYS */;
INSERT INTO `content_box` VALUES (1,0,'2015-06-13 15:41:33','2015-06-13 15:41:33',0,'今日特选',0,2,0,2),(2,0,'2015-06-13 16:13:26','2015-06-13 16:13:26',0,'顺丰优选',0,6,1,2);
/*!40000 ALTER TABLE `content_box` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_boxitem`
--

DROP TABLE IF EXISTS `content_boxitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_boxitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `box_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `position` int(11) NOT NULL,
  `is_delete` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `content_boxitem_cdd9e3d2` (`box_id`),
  KEY `content_boxitem_0a47aae8` (`item_id`),
  KEY `content_boxitem_1f456125` (`position`),
  CONSTRAINT `item_id_refs_id_bcb6a092` FOREIGN KEY (`item_id`) REFERENCES `content_item` (`id`),
  CONSTRAINT `box_id_refs_id_12a1a871` FOREIGN KEY (`box_id`) REFERENCES `content_box` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_boxitem`
--

LOCK TABLES `content_boxitem` WRITE;
/*!40000 ALTER TABLE `content_boxitem` DISABLE KEYS */;
INSERT INTO `content_boxitem` VALUES (1,1,4,1,0),(2,1,9,2,0),(3,2,7,1,0),(4,2,3,2,0),(5,2,6,3,0),(6,2,5,4,0),(7,2,2,5,0),(8,2,8,6,0);
/*!40000 ALTER TABLE `content_boxitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_city`
--

DROP TABLE IF EXISTS `content_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `city_code` varchar(10) NOT NULL,
  `name` varchar(16) NOT NULL,
  `manager` varchar(15) NOT NULL,
  `phone` varchar(15) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `content_city_5654bf12` (`state`),
  KEY `content_city_a59e4220` (`is_delete`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_city`
--

LOCK TABLES `content_city` WRITE;
/*!40000 ALTER TABLE `content_city` DISABLE KEYS */;
INSERT INTO `content_city` VALUES (1,0,'2015-05-23 16:24:09','2015-05-23 16:24:09',0,'010','北京','郭明磊','15801497633'),(2,0,'2015-05-23 16:24:28','2015-05-23 16:24:28',0,'200','上海','郭明磊','15801497633'),(3,0,'2015-05-23 17:15:39','2015-05-23 17:15:39',0,'010','全局','hr','15810398104');
/*!40000 ALTER TABLE `content_city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_imagetag`
--

DROP TABLE IF EXISTS `content_imagetag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_imagetag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image_id` int(11) NOT NULL,
  `content` varchar(50) NOT NULL,
  `link` varchar(256) NOT NULL,
  `tag_x` double NOT NULL,
  `tag_y` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `content_imagetag_06df7330` (`image_id`),
  CONSTRAINT `image_id_refs_id_b6001822` FOREIGN KEY (`image_id`) REFERENCES `content_itemimage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_imagetag`
--

LOCK TABLES `content_imagetag` WRITE;
/*!40000 ALTER TABLE `content_imagetag` DISABLE KEYS */;
/*!40000 ALTER TABLE `content_imagetag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_item`
--

DROP TABLE IF EXISTS `content_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `categroy_id` int(11) NOT NULL,
  `promote_id` int(11) DEFAULT NULL,
  `price` double NOT NULL,
  `stock_price` double NOT NULL,
  `desc` longtext NOT NULL,
  `short_desc` varchar(100) NOT NULL,
  `show_image` varchar(100) NOT NULL,
  `adv_image` varchar(100) NOT NULL,
  `head_image` varchar(100) NOT NULL,
  `screen_shot_1` varchar(100) NOT NULL,
  `screen_shot_2` varchar(100) NOT NULL,
  `screen_shot_3` varchar(100) NOT NULL,
  `screen_shot_4` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `content_item_59aa2403` (`categroy_id`),
  KEY `content_item_e684d0af` (`promote_id`),
  KEY `content_item_a59e4220` (`is_delete`),
  CONSTRAINT `promote_id_refs_id_b7e1e5dd` FOREIGN KEY (`promote_id`) REFERENCES `content_itempromote` (`id`),
  CONSTRAINT `categroy_id_refs_id_98039284` FOREIGN KEY (`categroy_id`) REFERENCES `content_itemcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_item`
--

LOCK TABLES `content_item` WRITE;
/*!40000 ALTER TABLE `content_item` DISABLE KEYS */;
INSERT INTO `content_item` VALUES (2,'樱桃',1,1,10,8,'','','/static/tmp_img/樱桃.jpg','/static/tmp_img/樱桃.jpg','','/static/tmp_img/樱桃简介.jpg','/static/tmp_img/樱桃简介2.jpg','/static/tmp_img/樱桃.jpg','/static/tmp_img/樱桃简介.jpg','2015-06-13 15:21:00','2015-06-13 15:21:00',0),(3,'西瓜',1,1,4,3,'','','/static/tmp_img/西瓜.jpg','/static/tmp_img/西瓜.jpg','','/static/tmp_img/西瓜.jpg','/static/tmp_img/西瓜简介.jpg','/static/tmp_img/西瓜2.jpg','/static/tmp_img/西瓜.jpg','2015-06-13 15:22:46','2015-06-13 15:22:46',0),(4,'荔枝',1,1,4,3,'','','/static/tmp_img/荔枝.jpg','/static/tmp_img/荔枝.jpg','','/static/tmp_img/荔枝简介.jpg','/static/tmp_img/荔枝2.jpg','/static/tmp_img/荔枝3.jpg','/static/tmp_img/荔枝4.jpg','2015-06-13 15:24:36','2015-06-13 16:11:37',0),(5,'红提',1,1,5,3,'','','/static/tmp_img/红提.jpg','/static/tmp_img/红提.jpg','','/static/tmp_img/红提简介.jpg','/static/tmp_img/红提2.jpg','/static/tmp_img/红提.jpg','/static/tmp_img/红提.jpg','2015-06-13 15:26:17','2015-06-13 15:26:17',0),(6,'蓝莓',1,1,10,8,'','','/static/tmp_img/蓝莓.jpg','/static/tmp_img/蓝莓.jpg','','/static/tmp_img/蓝莓简介1.jpg','/static/tmp_img/蓝莓简介2.jpg','/static/tmp_img/蓝莓.jpg','/static/tmp_img/蓝莓.jpg','2015-06-13 15:27:59','2015-06-13 15:27:59',0),(7,'脆梨甜瓜',1,1,4,3,'','','/static/tmp_img/脆瓜.jpg','/static/tmp_img/脆瓜.jpg','','/static/tmp_img/简介1.jpg','/static/tmp_img/简介2.jpg','/static/tmp_img/简介3.jpg','/static/tmp_img/简介4.jpg','2015-06-13 15:32:23','2015-06-13 15:32:23',0),(8,'水蜜桃',1,1,8,4,'','','/static/tmp_img/水蜜桃.jpg','/static/tmp_img/水蜜桃.jpg','','/static/tmp_img/水蜜桃简介1.jpg','/static/tmp_img/水蜜桃简介2.jpg','/static/tmp_img/水蜜桃简介4.jpg','/static/tmp_img/水蜜桃简介3.jpg','2015-06-13 15:34:46','2015-06-13 15:34:46',0),(9,'青桔',1,1,4,3,'','','/static/tmp_img/青橘.jpg','/static/tmp_img/青橘.jpg','','/static/tmp_img/青橘简介1.jpg','/static/tmp_img/青桔简介2.jpg','/static/tmp_img/青桔简介3.jpg','/static/tmp_img/青桔简介4.jpg','2015-06-13 15:37:00','2015-06-13 15:37:00',0);
/*!40000 ALTER TABLE `content_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_itemcategory`
--

DROP TABLE IF EXISTS `content_itemcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_itemcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `title` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `content_itemcategory_5654bf12` (`state`),
  KEY `content_itemcategory_a59e4220` (`is_delete`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_itemcategory`
--

LOCK TABLES `content_itemcategory` WRITE;
/*!40000 ALTER TABLE `content_itemcategory` DISABLE KEYS */;
INSERT INTO `content_itemcategory` VALUES (1,0,'2015-05-16 14:54:01','2015-05-16 14:54:01',0,'特价');
/*!40000 ALTER TABLE `content_itemcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_itemimage`
--

DROP TABLE IF EXISTS `content_itemimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_itemimage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) NOT NULL,
  `url` varchar(200) NOT NULL,
  `type` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `content_itemimage_0a47aae8` (`item_id`),
  CONSTRAINT `item_id_refs_id_20664c52` FOREIGN KEY (`item_id`) REFERENCES `content_item` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_itemimage`
--

LOCK TABLES `content_itemimage` WRITE;
/*!40000 ALTER TABLE `content_itemimage` DISABLE KEYS */;
INSERT INTO `content_itemimage` VALUES (1,2,'/static/tmp_img/樱桃.jpg',1),(2,3,'/static/tmp_img/西瓜.jpg',1),(3,4,'/static/tmp_img/荔枝.jpg',1),(4,5,'/static/tmp_img/红提.jpg',1),(5,6,'/static/tmp_img/蓝莓.jpg',1),(6,7,'/static/tmp_img/脆瓜.jpg',1),(7,8,'/static/tmp_img/水蜜桃.jpg',1),(8,9,'/static/tmp_img/青橘.jpg',1);
/*!40000 ALTER TABLE `content_itemimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_itempromote`
--

DROP TABLE IF EXISTS `content_itempromote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_itempromote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `title` varchar(100) NOT NULL,
  `promote_rate` double NOT NULL,
  `promote_type` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `content_itempromote_5654bf12` (`state`),
  KEY `content_itempromote_a59e4220` (`is_delete`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_itempromote`
--

LOCK TABLES `content_itempromote` WRITE;
/*!40000 ALTER TABLE `content_itempromote` DISABLE KEYS */;
INSERT INTO `content_itempromote` VALUES (1,0,'2015-05-16 14:55:36','2015-05-16 14:55:36',0,'哈哈',1,0);
/*!40000 ALTER TABLE `content_itempromote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `content_shoppingaddress`
--

DROP TABLE IF EXISTS `content_shoppingaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `content_shoppingaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `city_id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `manager` varchar(15) NOT NULL,
  `position` int(11) NOT NULL,
  `onlinetime` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `content_shoppingaddress_5654bf12` (`state`),
  KEY `content_shoppingaddress_a59e4220` (`is_delete`),
  KEY `content_shoppingaddress_b376980e` (`city_id`),
  KEY `content_shoppingaddress_1f456125` (`position`),
  CONSTRAINT `city_id_refs_id_943a7bd1` FOREIGN KEY (`city_id`) REFERENCES `content_city` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content_shoppingaddress`
--

LOCK TABLES `content_shoppingaddress` WRITE;
/*!40000 ALTER TABLE `content_shoppingaddress` DISABLE KEYS */;
INSERT INTO `content_shoppingaddress` VALUES (1,1,'2015-05-23 16:26:51','2015-06-13 15:40:48',0,1,'智慧社','回龙观育知东路30号院首开智慧社','15801497633','郭明磊',0,'2015-05-23 16:26:51'),(2,0,'2015-05-23 17:15:59','2015-05-23 17:20:18',0,3,'全局','全局','10','hr',0,'2015-05-23 00:00:00');
/*!40000 ALTER TABLE `content_shoppingaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2015-05-16 14:54:01',2,8,'1','ItemCategory object',1,''),(2,'2015-05-16 14:54:37',2,9,'None','ItemPromote object',1,''),(3,'2015-05-16 14:55:36',2,9,'1','ItemPromote object',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'content type','contenttypes','contenttype'),(4,'session','sessions','session'),(5,'log entry','admin','logentry'),(6,'migration history','south','migrationhistory'),(7,'首页盒子','content','box'),(8,'item category','content','itemcategory'),(9,'促销类型','content','itempromote'),(10,'促销类型','content','item'),(11,'提货点','content','shoppingaddress'),(12,'user','user','user'),(13,'盒子水果','content','boxitem'),(15,'城市','content','city'),(16,'商品图片','content','itemimage'),(17,'商品图片标签','content','imagetag');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('ai729pdioej70p78yj23zwwc5t0x67md','ZTgyZDE3ZWJiYzAxOTkxYmMwZGJhMzBkYzc4MjEzYjRkNThhODNiMzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6Mn0=','2015-06-06 19:03:34'),('qbcaez6ao4wuezm4xvvtj8azb1syhwn7','ZTgyZDE3ZWJiYzAxOTkxYmMwZGJhMzBkYzc4MjEzYjRkNThhODNiMzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6Mn0=','2015-05-30 15:19:27'),('yndt82sl1jovr5xjbi0ptg4ummtm53fd','ZTgyZDE3ZWJiYzAxOTkxYmMwZGJhMzBkYzc4MjEzYjRkNThhODNiMzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6Mn0=','2015-05-30 14:49:08'),('zz52abvozrtog5nwnbr978g1wbdwdr3l','ZTgyZDE3ZWJiYzAxOTkxYmMwZGJhMzBkYzc4MjEzYjRkNThhODNiMzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6Mn0=','2015-06-27 14:41:56');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `south_migrationhistory`
--

DROP TABLE IF EXISTS `south_migrationhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `south_migrationhistory`
--

LOCK TABLES `south_migrationhistory` WRITE;
/*!40000 ALTER TABLE `south_migrationhistory` DISABLE KEYS */;
INSERT INTO `south_migrationhistory` VALUES (1,'user','0001_initial','2015-05-09 13:53:51'),(2,'django_extensions','0001_empty','2015-05-09 13:53:51');
/*!40000 ALTER TABLE `south_migrationhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user`
--

DROP TABLE IF EXISTS `user_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  `role` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user`
--

LOCK TABLES `user_user` WRITE;
/*!40000 ALTER TABLE `user_user` DISABLE KEYS */;
INSERT INTO `user_user` VALUES (2,'pbkdf2_sha256$12000$C5c6fQ6Wjzt0$wVAGQAjhQ1bUirWnRwZGWTsTZvX4nAnq1YOZ1/DnydI=','2015-06-13 14:41:56',1,'guominglei','','','guominglei@youku.com',1,1,'2015-05-16 14:48:55',1);
/*!40000 ALTER TABLE `user_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_groups`
--

DROP TABLE IF EXISTS `user_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_groups_user_id_3da41bdcd69daabb_uniq` (`user_id`,`group_id`),
  KEY `user_user_groups_6340c63c` (`user_id`),
  KEY `user_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_ec4b76f9c976c6f` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_d3b9eb9815feb5f` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_groups`
--

LOCK TABLES `user_user_groups` WRITE;
/*!40000 ALTER TABLE `user_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_user_permissions`
--

DROP TABLE IF EXISTS `user_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_user_permissions_user_id_505ff7b6d553b31a_uniq` (`user_id`,`permission_id`),
  KEY `user_user_user_permissions_6340c63c` (`user_id`),
  KEY `user_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_419943833cbdeea4` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_9720aebdcf21fab` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_user_permissions`
--

LOCK TABLES `user_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `user_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_userboxperm`
--

DROP TABLE IF EXISTS `user_userboxperm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_userboxperm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `drawer_id` int(11) NOT NULL,
  `source` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_userboxperm_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_6f80cc61e6278be3` FOREIGN KEY (`user_id`) REFERENCES `user_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_userboxperm`
--

LOCK TABLES `user_userboxperm` WRITE;
/*!40000 ALTER TABLE `user_userboxperm` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_userboxperm` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-06-13 17:12:34
