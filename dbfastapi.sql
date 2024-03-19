/*
 Navicat Premium Data Transfer

 Source Server         : docker_postgres
 Source Server Type    : PostgreSQL
 Source Server Version : 160000 (160000)
 Source Host           : localhost:5432
 Source Catalog        : dbfastapi
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 160000 (160000)
 File Encoding         : 65001

 Date: 19/03/2024 07:39:06
*/


-- ----------------------------
-- Sequence structure for auto
-- ----------------------------
DROP SEQUENCE IF EXISTS "auto";
CREATE SEQUENCE "auto" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "users";
CREATE TABLE "users" (
  "id" int4 NOT NULL DEFAULT nextval('auto'::regclass),
  "guid" char(36) COLLATE "pg_catalog"."default",
  "fullname" varchar(100) COLLATE "pg_catalog"."default",
  "email" varchar(100) COLLATE "pg_catalog"."default",
  "password" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6),
  "updated_at" timestamp(6),
  "deleted_at" timestamp(6)
)
;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO "users" ("id", "guid", "fullname", "email", "password", "created_at", "updated_at", "deleted_at") VALUES (1, '162992be-684f-42e9-8db6-b8f4b21fcb48', 'Alfon Ritonga', 'alfonritonga@gmail.com', '$2a$12$ptKSPp3gPlK9ZoRQsfUi3OhXQkvmxrGqpUW0Ykke.BG5IQSbkykim', '2024-03-18 23:38:23', '2024-03-18 23:38:26', NULL);
INSERT INTO "users" ("id", "guid", "fullname", "email", "password", "created_at", "updated_at", "deleted_at") VALUES (3, '9672971b-1877-4817-a0b8-1bfb2898438b', 'Alfon Ritonga', 'alfonritonga@gmail.coma', '$2b$12$ekr5iXzPw3BcCYpzY6s.K.yPJIefN8RSpuJRKh9mfQsqj6I4Rp45C', NULL, NULL, NULL);
INSERT INTO "users" ("id", "guid", "fullname", "email", "password", "created_at", "updated_at", "deleted_at") VALUES (4, 'aa412f57-18cd-43a7-b043-f5bb34d60a64', 'Alfon Ritonga', 'alfonritonga@gmail.comaa', '$2b$12$97cvSJMCpscdRXdDBAnWPelIm/G7vzQ3H7SoH70ztWH2sxns30urO', NULL, NULL, NULL);
INSERT INTO "users" ("id", "guid", "fullname", "email", "password", "created_at", "updated_at", "deleted_at") VALUES (5, '3c9c1763-f1d6-4b65-bd46-aaf810d4065c', 'Alfon Ritonga', 'alfonritonga@gmail.comw', '$2b$12$ySTike3s9G4SBCtY4zjBaeVS8bhyecpe8BWC7mcRHJtS4e8OImFua', NULL, NULL, NULL);
COMMIT;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "auto"
OWNED BY "users"."id";
SELECT setval('"auto"', 5, true);

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");
