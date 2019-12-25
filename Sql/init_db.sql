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
  `pe_static` float(10, 2) DEFAULT NULL COMMENT '静态市盈率',
  `pe_dynamic` float(10, 2) DEFAULT NULL COMMENT '动态市盈率',
  `pe_rolling` float(10, 2) DEFAULT NULL COMMENT '滚动市盈率',
  `pb` float(10, 2) DEFAULT NULL COMMENT '市净率',
  `roe` float(10, 2) DEFAULT NULL COMMENT '加权净资产收益率',
  `price` float(10, 2) DEFAULT NULL COMMENT '最新股价',
  `turnover_rate` float(6, 2) DEFAULT NULL COMMENT '换手率',
  `total_value` bigint(255) DEFAULT NULL COMMENT '总市值',
  `circul_value` bigint(255) DEFAULT NULL COMMENT '流通市值',
  `prof` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '行业',
  `province` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '所属省份',
  `concept` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '概念',
  `create_time` timestamp(0) DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp(0) DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  `last_data_date` date DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `stock_no`(`stock_no`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 117806 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for stock_date
-- ----------------------------
DROP TABLE IF EXISTS `stock_date`;
CREATE TABLE `stock_date`  (
  `id` bigint(40) NOT NULL AUTO_INCREMENT,
  `stock_no` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '股票代码',
  `stock_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `trade_date` date NOT NULL COMMENT '日期',
  `JinShou` float(8, 2) DEFAULT NULL COMMENT '今收',
  `ZuoShou` float(8, 2) DEFAULT NULL COMMENT '昨收',
  `ShangZhang` float(6, 2) DEFAULT NULL COMMENT '上涨（价格）',
  `ZhangFu` float(6, 2) DEFAULT NULL COMMENT '涨幅百分点(如1.58代表上涨1.58%)',
  `JinKai` float(8, 2) DEFAULT NULL COMMENT '今开',
  `HuanSouLv` float(6, 2) DEFAULT NULL COMMENT '换手率百分点',
  `ChengJiaoLiang` int(20) DEFAULT NULL COMMENT '成交量(手)',
  `ChengJiaoE` bigint(40) DEFAULT NULL COMMENT '成交额(万元)',
  `ZuiGao` float(8, 2) DEFAULT NULL COMMENT '当日最高价',
  `ZuiDi` float(8, 2) DEFAULT NULL COMMENT '当日最低价',
  `ZhenFu` float(4, 2) DEFAULT NULL COMMENT '当日振幅',
  `NeiPan` int(12) DEFAULT NULL COMMENT '内盘（手）',
  `WaiPan` int(12) DEFAULT NULL COMMENT '外盘（手）',
  `WeiBi` float(10, 2) DEFAULT NULL COMMENT '委比（百分点）',
  `LiuTongShiZhi` int(16) DEFAULT NULL COMMENT '流通市值（万元）',
  `ZongShiZhi` int(16) DEFAULT NULL COMMENT '总市值（万元）',
  `ShiYingLv_MRQ` float(10, 2) DEFAULT NULL COMMENT '市盈率',
  `ShiJingLv` float(10, 2) DEFAULT NULL COMMENT '市净率',
  `LiangBi` float(10, 2) DEFAULT NULL COMMENT '量比',
  PRIMARY KEY (`id`, `stock_no`, `trade_date`) USING BTREE,
  UNIQUE INDEX `stockDate`(`stock_no`, `trade_date`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;



SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for stock_feihong
-- ----------------------------
DROP TABLE IF EXISTS `stock_fenhong`;
CREATE TABLE `stock_fenhong`  (
  `stock_no` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '股票代码',
  `stock_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '股票名字',
  `chuquan_date` date NOT NULL COMMENT '除权日',
  `fangan` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '方案',
  `guxilv` float(10, 2) NOT NULL COMMENT '股息率'
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
