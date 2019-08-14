CREATE DATABASE `GridL`;
USE `GridL`;
CREATE TABLE `moves` (
    `UserID` int(11) NOT NULL,
    `Time` int(11) NOT NULL,
    `PositionX` int(11) NOT NULL,
    `PositionY` int(11) NOT NULL,
    `Piece` int(11) NOT NULL,
    `Confirmed` bool DEFAULT FALSE,
    PRIMARY KEY (`UserID`)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;