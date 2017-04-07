
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `publisher_list`
-- ----------------------------
DROP TABLE IF EXISTS `publisher_list`;
CREATE TABLE `publisher_list` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `publisher_id` varchar(50) DEFAULT '' COMMENT '公众号的微信号',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for `publisher_info`
-- ----------------------------
DROP TABLE IF EXISTS `publisher_info`;
CREATE TABLE `publisher_info` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `name` varchar(50) DEFAULT '' COMMENT '公众号名称',
  `publisher_id` varchar(20) DEFAULT '' COMMENT '公众号ID',
  `company` varchar(100) DEFAULT '' COMMENT '主体名称',
  `description` varchar(200) DEFAULT '' COMMENT '功能简介',
  `logo_url` varchar(200) DEFAULT '' COMMENT 'logo url',
  `qr_url` varchar(200) DEFAULT '' COMMENT '二维码URL',
  `create_time` datetime DEFAULT NULL COMMENT '加入时间',
  `update_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  `push_count` int(11) DEFAULT '0' COMMENT '群发次数',
  `article_count` int(11) DEFAULT '0' COMMENT '群发篇数',
  `last_push_id` int(30) DEFAULT '0' COMMENT '最后的群发ID',
  `last_push_time` datetime DEFAULT NULL COMMENT '最后一次群发的时间',
  `newsfeed_url` varchar(300) DEFAULT '' COMMENT '最近文章URL',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=286 DEFAULT CHARSET=utf8mb4;


-- ----------------------------
-- Table structure for `newsfeed`
-- ----------------------------
DROP TABLE IF EXISTS `newsfeed`;
CREATE TABLE `newsfeed` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `title` varchar(100) DEFAULT '' COMMENT '文章标题',
  `index_html_path` varchar(180) DEFAULT '' COMMENT '本地存储地址',
  `source_url` varchar(300) DEFAULT '' COMMENT '原文地址',
  `cover_url` varchar(200) DEFAULT '' COMMENT '封面图URL',
  `description` varchar(200) DEFAULT '' COMMENT '文章摘要',
  `date_time` datetime DEFAULT NULL COMMENT '文章推送时间',
  `publisher_id` varchar(20) DEFAULT '0' COMMENT '公众号ID',
  `read_count` int(11) DEFAULT '0' COMMENT '阅读数',
  `like_count` int(11) DEFAULT '0' COMMENT '点攒数',
  `comment_count` int(11) DEFAULT '0' COMMENT '评论数',
  `content_url` varchar(300) DEFAULT '' COMMENT '文章永久地址',
  `author` varchar(50) DEFAULT '' COMMENT '作者',
  `msg_index` int(11) DEFAULT '0' COMMENT '一次群发中的图文顺序 1是头条 ',
  `copyright_stat` int(1) DEFAULT '0' COMMENT '11表示原创 其它表示非原创',
  `push_id` int(30) DEFAULT '0' COMMENT '群发消息ID',
  `type` int(11) DEFAULT '0' COMMENT '消息类型',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6559 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of newsfeed
-- ----------------------------

-- ----------------------------
-- Table structure for `newsfeed_stats`
-- ----------------------------
DROP TABLE IF EXISTS `newsfeed_stats`;
CREATE TABLE `newsfeed_stats` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `newsfeed_id` int(11) DEFAULT '0' COMMENT '文章ID',
  `create_time` datetime DEFAULT NULL COMMENT '记录时间',
  `read_count` int(11) DEFAULT '0' COMMENT '新增阅读数',
  `like_count` int(11) DEFAULT '0' COMMENT '新增点攒数',
  `comment_count` int(11) DEFAULT '0' COMMENT '新增评论数',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4006 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of newsfeed_stats
-- ----------------------------
