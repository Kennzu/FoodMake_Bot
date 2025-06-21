

-- Структура таблицы couple_requests
CREATE TABLE `couple_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sender_id` bigint DEFAULT NULL,
  `receiver_id` bigint DEFAULT NULL,
  `status` enum('pending','accepted','rejected') DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `sender_id` (`sender_id`),
  KEY `receiver_id` (`receiver_id`),
  CONSTRAINT `couple_requests_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`telegram_id`),
  CONSTRAINT `couple_requests_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`telegram_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Данные таблицы couple_requests


-- Структура таблицы couples_user
CREATE TABLE `couples_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `couple_uuid` char(36) DEFAULT NULL,
  `partner1_id` bigint DEFAULT NULL,
  `partner2_id` bigint DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `couple_uuid` (`couple_uuid`),
  UNIQUE KEY `partner1_id` (`partner1_id`,`partner2_id`),
  KEY `partner2_id` (`partner2_id`),
  CONSTRAINT `couples_user_ibfk_1` FOREIGN KEY (`partner1_id`) REFERENCES `users` (`telegram_id`),
  CONSTRAINT `couples_user_ibfk_2` FOREIGN KEY (`partner2_id`) REFERENCES `users` (`telegram_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Данные таблицы couples_user


-- Структура таблицы food_breakfast
CREATE TABLE `food_breakfast` (
  `id` int NOT NULL AUTO_INCREMENT,
  `couple_uuid` char(36) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `description` text,
  `calories` int DEFAULT NULL,
  `image` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `couple_uuid` (`couple_uuid`),
  CONSTRAINT `food_breakfast_ibfk_1` FOREIGN KEY (`couple_uuid`) REFERENCES `couples_user` (`couple_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Данные таблицы food_breakfast


-- Структура таблицы food_dinner
CREATE TABLE `food_dinner` (
  `id` int NOT NULL AUTO_INCREMENT,
  `couple_uuid` char(36) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `description` text,
  `calories` int DEFAULT NULL,
  `image` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `couple_uuid` (`couple_uuid`),
  CONSTRAINT `food_dinner_ibfk_1` FOREIGN KEY (`couple_uuid`) REFERENCES `couples_user` (`couple_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Данные таблицы food_dinner


-- Структура таблицы food_lanch
CREATE TABLE `food_lanch` (
  `id` int NOT NULL AUTO_INCREMENT,
  `couple_uuid` char(36) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `description` text,
  `calories` int DEFAULT NULL,
  `image` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `couple_uuid` (`couple_uuid`),
  CONSTRAINT `food_lanch_ibfk_1` FOREIGN KEY (`couple_uuid`) REFERENCES `couples_user` (`couple_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Данные таблицы food_lanch


-- Структура таблицы subscriptions
CREATE TABLE `subscriptions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `couple_uuid` char(36) DEFAULT NULL,
  `start_date` timestamp NULL DEFAULT NULL,
  `end_date` timestamp NULL DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `couple_uuid` (`couple_uuid`),
  CONSTRAINT `subscriptions_ibfk_1` FOREIGN KEY (`couple_uuid`) REFERENCES `couples_user` (`couple_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Данные таблицы subscriptions


-- Структура таблицы users
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `telegram_id` bigint DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `telegram_id` (`telegram_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Данные таблицы users


-- Структура таблицы users_db
CREATE TABLE `users_db` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Данные таблицы users_db
