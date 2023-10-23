-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 23, 2023 at 07:56 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vintage_palace`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `number` int(15) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`name`, `email`, `number`, `password`) VALUES
('Lennox kulecho', 'lenox@gmail.com', 711046100, '1234');

-- --------------------------------------------------------

--
-- Table structure for table `attendants`
--

CREATE TABLE `attendants` (
  `attendant_id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(50) NOT NULL,
  `status` varchar(15) NOT NULL DEFAULT 'Active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendants`
--

INSERT INTO `attendants` (`attendant_id`, `name`, `phone`, `email`, `status`) VALUES
('A001', 'Jeff smith', '0725436787', 'jsmith@gmail.com', 'Active'),
('A002', 'Abdullah karim', '0748364764', 'ahouston@gmail.com', 'Deactivated'),
('A003', 'Wesley Golden', '0751155001', 'Wgolden@gmail.com', 'Active'),
('A004', 'Ivy Perkins', '0720338318', 'ivyp@gmail.com', 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cart_id` int(11) NOT NULL,
  `art_number` varchar(20) NOT NULL,
  `shoe_name` varchar(50) NOT NULL,
  `price` int(11) NOT NULL,
  `quantity` int(10) NOT NULL,
  `total` int(10) NOT NULL,
  `sold_by` varchar(50) NOT NULL,
  `attendant_id` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sales_records`
--

CREATE TABLE `sales_records` (
  `sale_number` int(20) NOT NULL,
  `sale_id` varchar(20) NOT NULL,
  `art_number` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `price` int(20) NOT NULL,
  `quantity` int(20) NOT NULL,
  `total` int(20) NOT NULL,
  `sold_by` varchar(50) NOT NULL,
  `attendant_id` varchar(10) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp(),
  `time` time NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales_records`
--

INSERT INTO `sales_records` (`sale_number`, `sale_id`, `art_number`, `name`, `price`, `quantity`, `total`, `sold_by`, `attendant_id`, `date`, `time`) VALUES
(15, '102', 'S003', 'AF1_white_and_black.webp', 2500, 4, 10000, 'Jeff smith', '', '2023-10-15', '18:11:36'),
(16, '102', 'S004', 'AF1_blue.webp', 2500, 3, 7500, 'Jeff smith', '', '2023-10-15', '18:11:36'),
(17, '103', 'S004', 'AF1_blue.webp', 2500, 2, 5000, 'Jeff smith', '', '2023-10-15', '18:11:36'),
(18, '104', 'S003', 'AF1_white_and_black.webp', 2500, 2, 5000, 'Jeff smith', '', '2023-10-15', '18:11:36'),
(19, '105', 'S002', 'AirForce1LowOff-WhiteLightGreenSpark', 1300, 1, 1300, 'Jeff smith', '', '2023-10-15', '18:11:36'),
(20, '105', 'S004', 'AF1_blue', 2500, 1, 2500, 'Jeff smith', '', '2023-10-15', '18:11:36'),
(21, '106', 'S003', 'AF1_white_and_black', 2500, 1, 2500, 'Jeff smith', '', '2023-10-15', '18:11:36'),
(22, '106', 'S001', 'AF1_wnb_low_cut', 1200, 5, 6000, 'Jeff smith', '', '2023-10-15', '18:11:36'),
(23, '106', 'S002', 'AirForce1LowOff-WhiteLightGreenSpark', 1300, 4, 5200, 'Jeff smith', '', '2023-10-15', '18:11:36'),
(24, '107', 'S004', 'AF1_blue', 2500, 1, 2500, 'Jeff smith', 'A001', '2023-10-15', '18:11:36'),
(25, '107', 'S003', 'AF1_white_and_black', 2500, 1, 2500, 'Jeff smith', 'A001', '2023-10-15', '18:11:36'),
(26, '108', 'S003', 'AF1_white_and_black', 2500, 1, 2500, 'Jeff smith', 'A001', '2023-10-15', '18:11:36'),
(27, '108', 'S004', 'AF1_blue', 2500, 1, 2500, 'Jeff smith', 'A001', '2023-10-15', '18:11:36'),
(28, '108', 'S002', 'AirForce1LowOff-WhiteLightGreenSpark', 1300, 2, 2600, 'Jeff smith', 'A001', '2023-10-15', '18:11:36'),
(29, '109', 'S5', 'Jordan 1 low', 2200, 2, 4400, 'Jeff smith', 'A001', '2023-10-15', '19:44:27'),
(30, '109', 'S7', 'Air force 1 shadow', 1800, 3, 5400, 'Jeff smith', 'A001', '2023-10-15', '19:44:27'),
(31, '110', 'S5', 'Jordan 1 low', 2200, 4, 8800, 'Wesley Golden', 'A003', '2023-10-15', '21:54:59'),
(32, '110', 'S3', 'AF1_white_and_black', 2500, 1, 2500, 'Wesley Golden', 'A003', '2023-10-15', '21:54:59'),
(33, '111', 'S5', 'Jordan 1 low', 2200, 1, 2200, 'Wesley Golden', 'A003', '2023-10-16', '15:04:57'),
(34, '111', 'S7', 'Air force 1 shadow', 1200, 2, 2400, 'Wesley Golden', 'A003', '2023-10-16', '15:04:57');

-- --------------------------------------------------------

--
-- Table structure for table `shoes`
--

CREATE TABLE `shoes` (
  `product_number` int(10) NOT NULL,
  `art_number` varchar(20) NOT NULL,
  `shoe_type` varchar(50) NOT NULL,
  `shoe_name` varchar(100) NOT NULL,
  `price` int(10) NOT NULL,
  `amount_sold` int(10) NOT NULL DEFAULT 0,
  `stock` int(10) NOT NULL,
  `picture` varchar(50) NOT NULL,
  `status` varchar(15) NOT NULL DEFAULT 'Active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shoes`
--

INSERT INTO `shoes` (`product_number`, `art_number`, `shoe_type`, `shoe_name`, `price`, `amount_sold`, `stock`, `picture`, `status`) VALUES
(1, 'S1', 'Air force', 'AF1_wnb_low_cut', 1800, 25, 65, 'AF1_wnb_low_cut.jpg', 'Deactivated'),
(4, 'S3', 'Air force', 'AF1_white_and_black', 2500, 14, 23, 'AF1_white_and_black.webp', 'Active'),
(5, 'S4', 'Air force', 'AF1_blue', 2500, 8, 48, 'AF1_blue.webp', 'Deactivated'),
(6, 'S5', 'Air jordan', 'Jordan 1 low', 2200, 7, 23, 'jordan_1.webp', 'Active'),
(7, 'S7', 'Air force', 'Air force 1 shadow', 1200, 5, 15, 'air_force_1_shadow.webp', 'Active'),
(8, 'S8', 'Nike', 'Nike ultrafry', 2000, 0, 15, 'nike.webp', 'Active');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `attendants`
--
ALTER TABLE `attendants`
  ADD PRIMARY KEY (`attendant_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_id`);

--
-- Indexes for table `sales_records`
--
ALTER TABLE `sales_records`
  ADD PRIMARY KEY (`sale_number`);

--
-- Indexes for table `shoes`
--
ALTER TABLE `shoes`
  ADD PRIMARY KEY (`product_number`),
  ADD UNIQUE KEY `art number` (`art_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `cart_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `sales_records`
--
ALTER TABLE `sales_records`
  MODIFY `sale_number` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `shoes`
--
ALTER TABLE `shoes`
  MODIFY `product_number` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
