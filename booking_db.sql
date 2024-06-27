-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 27, 2024 at 03:18 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `booking_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `account_table`
--

CREATE TABLE `account_table` (
  `id` int(11) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `fullname` varchar(255) DEFAULT NULL,
  `registration` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `account_table`
--

INSERT INTO `account_table` (`id`, `email`, `password`, `fullname`, `registration`) VALUES
(1, 'admin@admin.com', '238Tonlegee', 'Admin', '241M2098'),
(20, 'jacktom.lynam@gmail.com', '238Tonlegee', 'Jack Lynam', '212CD0981'),
(23, 'jack.lynam@ericsson.com', '238Tonlegee', 'Jack Lynam', '191D1029'),
(24, 'cianna.meehan@ericsson.com', 'Hello1234!', 'cianna meehan', '191D2091'),
(25, 'emmanuel.jiss@ericsson.com', 'Password123!', 'Emmanuel', '11LS1549'),
(26, 'vidhurvarma.dandu@gmail.com', 'Vidhurvarma1', 'Vidhur', '11d18976');

-- --------------------------------------------------------

--
-- Table structure for table `booking_table`
--

CREATE TABLE `booking_table` (
  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `startTime` time NOT NULL,
  `endTime` time NOT NULL,
  `parkSpot` int(11) NOT NULL CHECK (`parkSpot` between 0 and 6),
  `accountID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking_table`
--

INSERT INTO `booking_table` (`id`, `date`, `startTime`, `endTime`, `parkSpot`, `accountID`) VALUES
(37, '2024-06-21', '08:00:00', '10:00:00', 2, 15),
(38, '2024-06-21', '09:00:00', '10:00:00', 1, 15),
(39, '2024-06-21', '07:00:00', '13:30:00', 6, 15),
(41, '2024-06-25', '12:00:00', '13:00:00', 3, 15),
(42, '2024-06-25', '12:00:00', '13:00:00', 2, 15),
(46, '2024-06-26', '08:00:00', '10:00:00', 2, 19),
(59, '2024-06-29', '14:05:00', '15:05:00', 3, 25),
(61, '2024-07-01', '15:00:00', '16:00:00', 1, 25),
(62, '2024-06-28', '14:18:00', '15:19:00', 1, 23),
(63, '2024-06-28', '14:18:00', '15:19:00', 2, 23);

-- --------------------------------------------------------

--
-- Table structure for table `contact_table`
--

CREATE TABLE `contact_table` (
  `id` int(11) NOT NULL,
  `fullname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `message` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact_table`
--

INSERT INTO `contact_table` (`id`, `fullname`, `email`, `message`) VALUES
(2, 'Jack Lynam', 'jack.lynam@ericsson.com', 'test message'),
(4, 'emmanuel', 'emmanuel.jiss@ericsson.com', 'Dylan seems to not be convinced this works.');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account_table`
--
ALTER TABLE `account_table`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `booking_table`
--
ALTER TABLE `booking_table`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `contact_table`
--
ALTER TABLE `contact_table`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account_table`
--
ALTER TABLE `account_table`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `booking_table`
--
ALTER TABLE `booking_table`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `contact_table`
--
ALTER TABLE `contact_table`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
