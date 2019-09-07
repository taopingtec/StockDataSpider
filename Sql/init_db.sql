drop database if exists stock_data;
create database stock_data DEFAULT CHARACTER SET utf8;

use stock_data;
set @@character_set_server=utf8;
set @@character_set_database=utf8;
set sql_mode=ANSI;


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for stock
-- ----------------------------
DROP TABLE IF EXISTS `stock`;
CREATE TABLE `stock`  (
  `id` bigint(40) NOT NULL AUTO_INCREMENT,
  `stock_no` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `stock_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`, `stock_no`, `stock_name`, `create_time`, `update_time`) USING BTREE,
  UNIQUE INDEX `stock_no`(`stock_no`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1425 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

