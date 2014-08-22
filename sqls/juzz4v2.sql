-- MySQL dump 10.13  Distrib 5.5.35, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: juzz4v2
-- ------------------------------------------------------
-- Server version	5.5.35-0ubuntu0.12.04.2-log

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

CREATE DATABASE IF NOT EXISTS `juzz4v2`;
use `juzz4v2`;

--
-- Table structure for table `channel_device_map`
--

DROP TABLE IF EXISTS `channel_device_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `channel_device_map` (
  `kup_device_id` bigint(20) DEFAULT NULL,
  `kup_channel_id` tinyint(2) DEFAULT NULL,
  `node_device_id` bigint(20) DEFAULT NULL,
  KEY `idx_kup_dev_id` (`kup_device_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channel_device_map`
--

LOCK TABLES `channel_device_map` WRITE;
/*!40000 ALTER TABLE `channel_device_map` DISABLE KEYS */;
/*!40000 ALTER TABLE `channel_device_map` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configurations`
--

DROP TABLE IF EXISTS `configurations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configurations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `value` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configurations`
--

LOCK TABLES `configurations` WRITE;
/*!40000 ALTER TABLE `configurations` DISABLE KEYS */;
INSERT INTO `configurations` VALUES (1,'platform-settings','{\"host\":\"localhost\",\"event-port\":\"7474\"}');
/*!40000 ALTER TABLE `configurations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_events`
--

DROP TABLE IF EXISTS `device_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_events` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `data` mediumtext,
  `event_type` int(11) NOT NULL,
  `received_time` datetime DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `device_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKAE941322A1D5461E` (`device_id`),
  CONSTRAINT `FKAE941322A1D5461E` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_events`
--

LOCK TABLES `device_events` WRITE;
/*!40000 ALTER TABLE `device_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `device_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_models`
--

DROP TABLE IF EXISTS `device_models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_models` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `created_by` bigint(20) DEFAULT NULL,
  `modified_at` datetime DEFAULT NULL,
  `modified_by` bigint(20) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `channels` int(11) NOT NULL,
  `data` varchar(255) DEFAULT NULL,
  `action` text,
  `misc` text,
  `liveview` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=240 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_models`
--

LOCK TABLES `device_models` WRITE;
/*!40000 ALTER TABLE `device_models` DISABLE KEYS */;
INSERT INTO `device_models` VALUES (100,NULL,NULL,NULL,NULL,'Dahua IP Camera',1,NULL,NULL,'{\r\n	\"servertype\": \"dahua-ipc\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n		},\n            \r\n		\"activex\":{\r\n			\"objectcode\": \"<object id=\'ocx\' width=\'100%\' height=\'100%\' classid=\'CLSID:D8993483-BB2A-42b1-A3DF-52290DB03FAE\' codebase=\'webrec.cab#version=2,1,6,25\' ><param name=\'lVideoWindNum\' value=1><param name=\'VideoWindBGColor\' value=\'\'><param name=\'VideoWindBarColor\' value=\'\'><param name=\'VideoWindTextColor\' value=\'\'><param name=\'SetLangFromIP\' value=\'localhost\'><param name=\'SetHostPort\' value=37777><param name=\'SetLanguage\' value=101></object><script defer type=\\\"text/javascript\\\">function init_dahua() {ocx.LoginDeviceEx(\\\"#{device:host}\\\",0,\\\"#{device:misc:login}\\\",\\\"#{device:misc:password}\\\",0);ocx.ConnectRealVideo(0,0);}setTimeout(\'init_dahua()\',6000);</script>\"\r\n		}\r\n	}\r\n\n}'),(101,NULL,NULL,NULL,NULL,'Dahua DVR 4-Channel',4,NULL,NULL,'{\r\n	\"servertype\": \"dahua-dvr-4\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n		},\n            \r\n		\"activex\":{\r\n			\"objectcode\": \"<object id=\'ocx\' width=\'100%\' height=\'100%\' classid=\'CLSID:D8993483-BB2A-42b1-A3DF-52290DB03FAE\' codebase=\'webrec.cab#version=2,1,6,25\' ><param name=\'lVideoWindNum\' value=1><param name=\'VideoWindBGColor\' value=\'\'><param name=\'VideoWindBarColor\' value=\'\'><param name=\'VideoWindTextColor\' value=\'\'><param name=\'SetLangFromIP\' value=\'localhost\'><param name=\'SetHostPort\' value=37777><param name=\'SetLanguage\' value=101></object><script defer type=\\\"text/javascript\\\">function init_dahua() {ocx.LoginDeviceEx(\\\"#{device:host}\\\",0,\\\"#{device:misc:login}\\\",\\\"#{device:misc:password}\\\",0);ocx.ConnectRealVideo(0,0);}setTimeout(\'init_dahua()\',6000);</script>\"\r\n		}\r\n	},\r\n\n	\"1\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:1}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n		},\n            \r\n		\"activex\":{\r\n			\"objectcode\": \"<object id=\'ocx\' width=\'100%\' height=\'100%\' classid=\'CLSID:D8993483-BB2A-42b1-A3DF-52290DB03FAE\' codebase=\'webrec.cab#version=2,1,6,25\' ><param name=\'lVideoWindNum\' value=1><param name=\'VideoWindBGColor\' value=\'\'><param name=\'VideoWindBarColor\' value=\'\'><param name=\'VideoWindTextColor\' value=\'\'><param name=\'SetLangFromIP\' value=\'localhost\'><param name=\'SetHostPort\' value=37777><param name=\'SetLanguage\' value=101></object><script defer type=\\\"text/javascript\\\">function init_dahua() {ocx.LoginDeviceEx(\\\"#{device:host}\\\",0,\\\"#{device:misc:login}\\\",\\\"#{device:misc:password}\\\",0);ocx.ConnectRealVideo(1,0);}setTimeout(\'init_dahua()\',6000);</script>\"\r\n		}\r\n	},\r\n\n	\"2\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:2}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n		},\n            \r\n		\"activex\":{\r\n			\"objectcode\": \"<object id=\'ocx\' width=\'100%\' height=\'100%\' classid=\'CLSID:D8993483-BB2A-42b1-A3DF-52290DB03FAE\' codebase=\'webrec.cab#version=2,1,6,25\' ><param name=\'lVideoWindNum\' value=1><param name=\'VideoWindBGColor\' value=\'\'><param name=\'VideoWindBarColor\' value=\'\'><param name=\'VideoWindTextColor\' value=\'\'><param name=\'SetLangFromIP\' value=\'localhost\'><param name=\'SetHostPort\' value=37777><param name=\'SetLanguage\' value=101></object><script defer type=\\\"text/javascript\\\">function init_dahua() {ocx.LoginDeviceEx(\\\"#{device:host}\\\",0,\\\"#{device:misc:login}\\\",\\\"#{device:misc:password}\\\",0);ocx.ConnectRealVideo(2,0);}setTimeout(\'init_dahua()\',6000);</script>\"\r\n		}\r\n	},\r\n\n	\"3\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:3}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n		},\n            \r\n		\"activex\":{\r\n			\"objectcode\": \"<object id=\'ocx\' width=\'100%\' height=\'100%\' classid=\'CLSID:D8993483-BB2A-42b1-A3DF-52290DB03FAE\' codebase=\'webrec.cab#version=2,1,6,25\' ><param name=\'lVideoWindNum\' value=1><param name=\'VideoWindBGColor\' value=\'\'><param name=\'VideoWindBarColor\' value=\'\'><param name=\'VideoWindTextColor\' value=\'\'><param name=\'SetLangFromIP\' value=\'localhost\'><param name=\'SetHostPort\' value=37777><param name=\'SetLanguage\' value=101></object><script defer type=\\\"text/javascript\\\">function init_dahua() {ocx.LoginDeviceEx(\\\"#{device:host}\\\",0,\\\"#{device:misc:login}\\\",\\\"#{device:misc:password}\\\",0);ocx.ConnectRealVideo(3,0);}setTimeout(\'init_dahua()\',6000);</script>\"\r\n		}\r\n	}\r\n\n}'),(102,NULL,NULL,NULL,NULL,'Amegia IP Camera',1,NULL,NULL,'{\r\n	\"servertype\": \"amegia-ipc\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n		},\n            \r\n		\"activex\":{\r\n			\"objectcode\": \"<object id=\'RTSPCtl\' width=\'100%\' height=\'100%\' classid=\'CLSID:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B\' codebase=\'http://www.apple.com/qtactivex/qtplugin.cab\'><param name=\'qtsrc\' value=\'rtsp://#{device:host}:554/v05\'><param name=\'type\' value=\'video/quicktime\'><param name=\'scale\' value=\'tofit\'><param name=\'bgcolor\' value=\'black\'><param name=\'controller\' value=\'false\'></object>\"\r\n		}\r\n	}\r\n\n}'),(103,NULL,NULL,NULL,NULL,'HiSharp Mobile DVR 4 Channel',4,NULL,NULL,'{\r\n	\"servertype\": \"hisharp-mdvr-4\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-gsensor\",\"live-gps\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	},\r\n\n	\"1\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:1}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	},\r\n\n	\"2\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:2}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	},\r\n\n	\"3\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:3}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	}\r\n\n}'),(104,NULL,NULL,NULL,NULL,'TVT DVR 4 Channel',4,NULL,NULL,'{\r\n	\"servertype\": \"tvt-dvr-4\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	},\r\n\n	\"1\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:1}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	},\r\n\n	\"2\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:2}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	},\r\n\n	\"3\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:3}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	}\r\n\n}'),(105,NULL,NULL,NULL,NULL,'TVT Mobile DVR 4 Channel',4,NULL,NULL,'{\r\n	\"servertype\": \"tvt-mdvr-4\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	},\r\n\n	\"1\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:1}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	},\r\n\n	\"2\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:2}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	},\r\n\n	\"3\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:3}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	}\r\n\n}'),(106,NULL,NULL,NULL,NULL,'Vivotek IP Camera',1,NULL,NULL,'{\r\n	\"servertype\": \"vivotek-ipc\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n		},\n            \r\n		\"activex\":{\r\n			\"objectcode\": \"<OBJECT onmouseover=\"mousein(this)\" onmouseout=\"mouseout(this)\" style=\"z-index:1;\" id=\"#{system:random_id}\" WIDTH=\"100%\" HEIGHT=\"100%\" standby=\"Loading plug-in...\" name=\"VitCtrl\" CLASSID=\"CLSID:70EDCF63-CA7E-4812-8528-DA1EA2FD53B6\" CODEBASE=\"#{system:static_path}/J4SVitCtrl.cab#version=4,0,0,5\"><PARAM NAME=\"Language\" VALUE=\"EN\"><PARAM NAME=\"RemoteIPAddr\" VALUE=\"#{device:host}\"><PARAM NAME=\"HttpPort\" VALUE=\"#{device:misc:port}\"><PARAM NAME=\"ViewStream\" VALUE=\"#{device:video_stream}\"><PARAM NAME=\"UserName\" VALUE=\"#{device:misc:login}\"><PARAM NAME=\"Password\" VALUE=\"#{device:misc:password}\"><PARAM NAME=\"IgnoreBorder\" VALUE=\"true\"><PARAM NAME=\"ServerModelType\" VALUE=\"5\"><PARAM NAME=\"IgnoreCaption\" VALUE=\"true\"><PARAM NAME=\"ControlType\" VALUE=\"0\"><PARAM NAME=\"HideConnectIP\" VALUE=\"true\"><PARAM NAME=\"DisplayErrorMsg\" VALUE=\"false\"></OBJECT>\",\r\n	\"ptz\": {\r\n\n                                \"left\": \"#{system:random_id}.SendCameraCommand(\'left\');\",\r\n\n                                \"right\": \"#{system:random_id}.SendCameraCommand(\'right\');\",\r\n\n                                \"up\": \"#{system:random_id}.SendCameraCommand(\'up\');\",\r\n\n                                \"down\": \"#{system:random_id}.SendCameraCommand(\'down\');\",\r\n\n                                \"in\": \"#{system:random_id}.SendCameraCommand(\'tele\');\",\r\n\n                                \"out\": \"#{system:random_id}.SendCameraCommand(\'wide\');\",\r\n\n                                \"home\": \"#{system:random_id}.SendCameraCommand(\'home\');\"\r\n\n                        }	}\r\n	}\r\n\n}'),(107,NULL,NULL,NULL,NULL,'Axis IP Camera',1,NULL,NULL,'{\r\n  \"servertype\": \"axis-ipc\",\r\n       \"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n   \"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n        \"0\": {\r\n            \"mjpeg\": {\r\n                        \"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n   }\r\n   },\r\n\n        \"1\": {\r\n            \"mjpeg\": {\r\n                        \"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:1}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n   }\r\n   },\r\n\n        \"2\": {\r\n            \"mjpeg\": {\r\n                        \"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:2}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n   }\r\n   },\r\n\n        \"3\": {\r\n            \"mjpeg\": {\r\n                        \"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:3}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n   }\r\n   }\r\n\n}'),(108,NULL,NULL,NULL,NULL,'Amegia PnP IP Camera',1,NULL,NULL,'{\r\n	\"servertype\": \"amegia-pnp-ipc\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n		},\n            \r\n		\"activex\":{\r\n			\"objectcode\": \"<object id=\'RTSPCtl\' width=\'100%\' height=\'100%\' classid=\'CLSID:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B\' codebase=\'http://www.apple.com/qtactivex/qtplugin.cab\'><param name=\'qtsrc\' value=\'rtsp://#{device:host}:554/v05\'><param name=\'type\' value=\'video/quicktime\'><param name=\'scale\' value=\'tofit\'><param name=\'bgcolor\' value=\'black\'><param name=\'controller\' value=\'false\'></object>\"\r\n		}\r\n	}\r\n\n}'),(109,NULL,NULL,NULL,NULL,'TVT PNP DVR 4 Channel',4,NULL,NULL,'{\r\n  \"servertype\": \"tvt-pnp-dvr-4\",\r\n  \"supportedtasktypes\": [\"live-image\"],\r\n   \"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n        \"0\": {\r\n            \"mjpeg\": {\r\n                        \"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n   }\r\n   },\r\n\n        \"1\": {\r\n            \"mjpeg\": {\r\n                        \"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:1}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n   }\r\n   },\r\n\n        \"2\": {\r\n            \"mjpeg\": {\r\n                        \"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:2}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n   }\r\n   },\r\n\n        \"3\": {\r\n            \"mjpeg\": {\r\n                        \"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:3}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n   }\r\n   }\r\n\n}'),(110,NULL,NULL,NULL,NULL,'General RTSP IP Camera',1,NULL,NULL,'{\r\n	\"servertype\": \"general-rtsp-ipc\",\r\n	\"supportedtasktypes\": [\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n		}\n		}\r\n\n}'),(111,NULL,NULL,NULL,NULL,'Amtk IP Camera',1,NULL,NULL,'{\r\n	\"servertype\": \"amtk-ipc\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/\"}',NULL),(112,NULL,NULL,NULL,NULL,'Panasonic IP Camera',1,NULL,NULL,'{\r\n	\"servertype\": \"panasonic-ipc\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:3}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	}\r\n\n}'),(113,NULL,NULL,NULL,NULL,'Etrovision IP Camera',1,NULL,NULL,'{\r\n	\"servertype\": \"etrovision-ipc\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:3}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	}\r\n\n}'),(115,NULL,NULL,NULL,NULL,'KAI NODE',4,NULL,NULL,'{\r\n	\"servertype\": \"kai-node\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\", \"node\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/\"}',NULL),(116,NULL,NULL,NULL,NULL,'Messoa IP Camera',1,NULL,NULL,'{\r\n	\"servertype\": \"messoa-ipc\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n		},\n            \r\n		\"activex\":{\r\n			\"objectcode\": \"<object id=\'RTSPCtl\' width=\'100%\' height=\'100%\' classid=\'CLSID:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B\' codebase=\'http://www.apple.com/qtactivex/qtplugin.cab\'><param name=\'qtsrc\' value=\'rtsp://#{device:host}:554/v05\'><param name=\'type\' value=\'video/quicktime\'><param name=\'scale\' value=\'tofit\'><param name=\'bgcolor\' value=\'black\'><param name=\'controller\' value=\'false\'></object>\"\r\n		}\r\n	}\r\n\n}'),(117,NULL,NULL,NULL,NULL,'KAI ONE',1,NULL,NULL,'{\r\n	\"servertype\": \"kai-one\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\", \"node\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/\"}',NULL),(121,NULL,NULL,NULL,NULL,'KAI NODE 10',10,NULL,NULL,'{\r\n	\"servertype\": \"kai-node-10\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\",\"live-rtsp\",\"live-rtmp\", \"node\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}',NULL),(235,NULL,NULL,NULL,NULL,'Atracker GPS',1,NULL,NULL,'{\r\n	\"servertype\": \"atracker\",\r\n	\"supportedtasktypes\": [\"live-gps\",\"gpio\",\"live-gsensor\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n	}\r\n	}\r\n\n}'),(236,NULL,NULL,NULL,NULL,'VCA device',0,NULL,NULL,'{\r\n	\"servertype\": \"vca-device\",\r\n	\"supportedtasktypes\": [\"live-gps\"]\r\n}\r\n',NULL),(237,NULL,NULL,NULL,NULL,'General MJPEG IP Camera',1,NULL,NULL,'{\r\n	\"servertype\": \"general-mjpeg-ipc\",\r\n	\"supportedtasktypes\": [\"live-image\",\"live-mjpeg\"],\r\n	\"device_url\": \"http://#{device:host}:#{device:misc:port}/ \r\n\"}','{\n	\"0\": {\r\n		\"mjpeg\": {\r\n			\"objectcode\": \"<applet id=\\\"#{system:random_id}\\\" name=\\\"Motion JPEG Player\\\" code=\\\"com.kaisquare.player.mjpeg.MJPEGPlayer\\\" archive=\\\"#{system:static_path}/kaisquare-player-mjpeg.jar\\\" width=\\\"100%\\\" height=\\\"100%\\\" mayscript=\\\"true\\\"><param name=\\\"url\\\" value=\\\"#{device:device_server_mjpeg_url_map:0}\\\" /><param name=\\\"username\\\" value=\\\"#{device:misc:login}\\\" /><param name=\\\"password\\\" value=\\\"#{device:misc:password}\\\" /><param name=\\\"mouse_click_javascript\\\" value=\\\"liveview_mjpeg_click(document.getElementById(\'#{system:random_id}\'));\\\" /><p style=\\\"color: white;\\\">Your browser does not support <a href=\\\"http://www.java.com/\\\">Java applets</a>.</p></applet>\" \r\n		}\n		}\r\n\n}'),(238,NULL,NULL,NULL,NULL,'Ekahau RTLS Controller',0,NULL,NULL,'{\r\n	\"servertype\": \"ekahau-rtls-controller\",\r\n	\"supportedtasktypes\": [\"live-indoor-location\",\" live-indoor-maps\"]\r\n}\r\n',NULL),(239,NULL,NULL,NULL,NULL,'Genspro Intercom Device',0,NULL,NULL,'{\r\n  \"servertype\": \"genspro-intercom\",\r\n    \"supportedtasktypes\": [\"gpio\"]\r\n}',NULL);
/*!40000 ALTER TABLE `device_models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `device_key` varchar(255) DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `lat` int(11) DEFAULT NULL,
  `lng` int(11) DEFAULT NULL,
  `model_id` bigint(20) DEFAULT NULL,
  `current_position_id` bigint(20) DEFAULT NULL,
  `misc` text,
  `device_server_urls` text,
  `snapshot_recording_enabled` int(11) DEFAULT NULL,
  `snapshot_recording_interval` int(11) NOT NULL,
  `cloud_recording_enabled` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK5CF8ACDDEE3626C0` (`model_id`),
  KEY `FK5CF8ACDDED2F2678` (`current_position_id`),
  CONSTRAINT `FK5CF8ACDDED2F2678` FOREIGN KEY (`current_position_id`) REFERENCES `positions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ds_device_info`
--

DROP TABLE IF EXISTS `ds_device_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ds_device_info` (
  `id` bigint(20) NOT NULL,
  `device_key` varchar(255) DEFAULT NULL,
  `device_info` text,
  `status` tinyint(2) DEFAULT NULL,
  `server_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ds_device_info`
--

LOCK TABLES `ds_device_info` WRITE;
/*!40000 ALTER TABLE `ds_device_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `ds_device_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ds_server_info`
--

DROP TABLE IF EXISTS `ds_server_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ds_server_info` (
  `id` bigint(20) NOT NULL,
  `type` varchar(255) DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `port` smallint(5) unsigned DEFAULT NULL,
  `register_time` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ds_server_info`
--

LOCK TABLES `ds_server_info` WRITE;
/*!40000 ALTER TABLE `ds_server_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `ds_server_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_types`
--

DROP TABLE IF EXISTS `event_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_types` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `tech_name` varchar(255) DEFAULT NULL,
  `data` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9801 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_types`
--

LOCK TABLES `event_types` WRITE;
/*!40000 ALTER TABLE `event_types` DISABLE KEYS */;
INSERT INTO `event_types` VALUES (1,'Alarm','event-alarm',NULL),(2,'Motion','event-motion',NULL),(3,'Video loss','event-video-loss',NULL),(4,'Connection lost','event-connection-lost',NULL),(5,'Connected','event-connected',NULL),(6,'Connection poor','event-connection-poor',NULL),(512,'Digital input','event-input',NULL),(513,'Digital output','event-output',NULL),(514,'Manual','event-manual',NULL),(1024,'Idle','event-idle',NULL),(1025,'Speeding','event-speeding',NULL),(2048,'Sudden acceleration','event-sudden-acceleration',NULL),(2049,'Sudden braking','event-sudden-braking',NULL),(2050,'Sudden left','event-sudden-left',NULL),(2051,'Sudden right','event-sudden-right',NULL),(2052,'Sudden up','event-sudden-up',NULL),(2053,'Sudden down','event-sudden-down',NULL),(4096,'Entering geofence','event-geofence-enter',NULL),(4097,'Exiting geofence','event-geofence-exit',NULL),(5010,'Audio','event-audio',NULL),(5015,'Passive infrared','event-passive-infrared',NULL),(5020,'Event Intercom Visitor Alert','event-intercom-visitor-alert',NULL),(6001,'Node unregistered','event-node-unregistered',NULL),(6002,'Node registered','event-node-registered',NULL),(6021,'Upstream failed','event-upstream-failed',NULL),(7001,'Storage started','event-storage-started',NULL),(7002,'Storage stopped','event-storage-stopped',NULL),(7021,'Disk full','event-disk-full',NULL),(8192,'Count','event-count',NULL),(8200,'Intrusion Detected','event-vca-intrusion',NULL),(8201,'Loitering Detected','event-vca-loitering',NULL),(8202,'Face Detected','event-vca-face',NULL),(8203,'Heat Map Alert','event-vca-heatmap',NULL),(8204,'Licecse Plate Detected','event-vca-lpr',NULL),(8205,'Counting Triggered','event-vca-counting',NULL),(8206,'View Obstructed','event-vca-viewobstructed',NULL),(8207,'Audience Event','event-vca-audienceprofiling',NULL),(8208,'Vca Video Blur','event-vca-video-blur',NULL),(8209,'Vca Perimeter','event-vca-perimeter',NULL),(8210,'Vca People Counting','event-vca-people-counting',NULL),(8211,'Vca Object Counting','event-vca-object-counting',NULL),(8212,'Vca Video Loss','event-vca-video-loss',NULL),(9800,'Event video recording','event-recording',NULL);
/*!40000 ALTER TABLE `event_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gpsdata`
--

DROP TABLE IF EXISTS `gpsdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gpsdata` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `device_id` bigint(20) DEFAULT NULL,
  `direction` int(11) DEFAULT NULL,
  `lat` int(11) DEFAULT NULL,
  `lng` int(11) DEFAULT NULL,
  `speed` int(11) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `fixed` bit(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gpsdata`
--

LOCK TABLES `gpsdata` WRITE;
/*!40000 ALTER TABLE `gpsdata` DISABLE KEYS */;
/*!40000 ALTER TABLE `gpsdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gsensordata`
--

DROP TABLE IF EXISTS `gsensordata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gsensordata` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `created_at` datetime DEFAULT NULL,
  `device_id` bigint(20) DEFAULT NULL,
  `x` double DEFAULT NULL,
  `y` double DEFAULT NULL,
  `z` double DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `devidindex` (`device_id`),
  KEY `createdatindex` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gsensordata`
--

LOCK TABLES `gsensordata` WRITE;
/*!40000 ALTER TABLE `gsensordata` DISABLE KEYS */;
/*!40000 ALTER TABLE `gsensordata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `positions`
--

DROP TABLE IF EXISTS `positions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `positions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `modified_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `lat` int(11) DEFAULT NULL,
  `lng` int(11) DEFAULT NULL,
  `speed` int(11) DEFAULT NULL,
  `direction` int(11) DEFAULT NULL,
  `current_gpsdata_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK65C08C6AB9A8DC3C` (`current_gpsdata_id`),
  KEY `speedindex` (`speed`),
  KEY `latindex` (`lat`),
  KEY `modifiedatindex` (`modified_at`),
  KEY `lngindex` (`lng`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `positions`
--

LOCK TABLES `positions` WRITE;
/*!40000 ALTER TABLE `positions` DISABLE KEYS */;
/*!40000 ALTER TABLE `positions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recording_temp_info`
--

DROP TABLE IF EXISTS `recording_temp_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recording_temp_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `device_id` bigint(20) DEFAULT NULL,
  `server_id` bigint(20) DEFAULT NULL,
  `type` tinyint(2) DEFAULT NULL,
  `task` tinyint(2) DEFAULT NULL,
  `time_interval` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recording_temp_info`
--

LOCK TABLES `recording_temp_info` WRITE;
/*!40000 ALTER TABLE `recording_temp_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `recording_temp_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rs_device_info`
--

DROP TABLE IF EXISTS `rs_device_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rs_device_info` (
  `id` bigint(20) NOT NULL,
  `device_info` text,
  `server_id` bigint(20) DEFAULT NULL,
  `status` tinyint(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rs_device_info`
--

LOCK TABLES `rs_device_info` WRITE;
/*!40000 ALTER TABLE `rs_device_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `rs_device_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rs_server_info`
--

DROP TABLE IF EXISTS `rs_server_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rs_server_info` (
  `id` bigint(20) NOT NULL,
  `host` varchar(255) DEFAULT NULL,
  `port` smallint(5) unsigned DEFAULT NULL,
  `server_info` text,
  `register_time` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rs_server_info`
--

LOCK TABLES `rs_server_info` WRITE;
/*!40000 ALTER TABLE `rs_server_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `rs_server_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `storage_keys`
--

DROP TABLE IF EXISTS `storage_keys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `storage_keys` (
  `mac` varchar(255) DEFAULT NULL,
  `device_id` bigint(20) DEFAULT NULL,
  `channel` tinyint(2) DEFAULT NULL,
  `time` bigint(20) DEFAULT NULL,
  `namespace` varchar(255) DEFAULT NULL,
  `s_object` varchar(255) DEFAULT NULL,
  `s_key` varchar(255) DEFAULT NULL,
  `insert_time` bigint(20) DEFAULT NULL,
  UNIQUE KEY `s_key` (`s_key`),
  KEY `idx_storage_key` (`mac`(20),`device_id`,`channel`,`namespace`(20),`s_object`(20))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storage_keys`
--

LOCK TABLES `storage_keys` WRITE;
/*!40000 ALTER TABLE `storage_keys` DISABLE KEYS */;
/*!40000 ALTER TABLE `storage_keys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stream_session_info`
--

DROP TABLE IF EXISTS `stream_session_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stream_session_info` (
  `id` varchar(255) NOT NULL,
  `type` varchar(255) DEFAULT NULL,
  `ttl` bigint(20) DEFAULT NULL,
  `device_id` bigint(20) DEFAULT NULL,
  `channel_id` tinyint(2) DEFAULT NULL,
  `time` bigint(20) DEFAULT NULL,
  `start_time` bigint(20) DEFAULT NULL,
  `end_time` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stream_session_info`
--

LOCK TABLES `stream_session_info` WRITE;
/*!40000 ALTER TABLE `stream_session_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `stream_session_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tasks` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `device_id` bigint(20) DEFAULT NULL,
  `channel_id` tinyint(2) DEFAULT NULL,
  `command` varchar(255) DEFAULT NULL,
  `insert_time` bigint(20) DEFAULT NULL,
  `time` bigint(20) DEFAULT NULL,
  `status` tinyint(2) DEFAULT NULL,
  `t_data` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_dev_id` (`device_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-07-24 16:22:29
