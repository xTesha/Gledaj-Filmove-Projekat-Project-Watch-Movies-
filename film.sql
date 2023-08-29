-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 29, 2023 at 07:42 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `film`
--

-- --------------------------------------------------------

--
-- Table structure for table `administratori`
--

CREATE TABLE `administratori` (
  `id` int(11) NOT NULL,
  `korisnickoime` varchar(255) NOT NULL,
  `lozinka` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `administratori`
--

INSERT INTO `administratori` (`id`, `korisnickoime`, `lozinka`) VALUES
(1, 'admin1', 'fe5178ac3ecc8e9956d4f7b2e7a50e2df5a965a54b3f31c2aba7598adef6a998');

-- --------------------------------------------------------

--
-- Table structure for table `komentari`
--

CREATE TABLE `komentari` (
  `id` int(11) NOT NULL,
  `film_id` int(11) DEFAULT NULL,
  `korisnik_id` int(11) DEFAULT NULL,
  `sadrzaj` text DEFAULT NULL,
  `odobren` tinyint(1) DEFAULT NULL,
  `korisnickoime` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `komentari`
--

INSERT INTO `komentari` (`id`, `film_id`, `korisnik_id`, `sadrzaj`, `odobren`, `korisnickoime`) VALUES
(19, 447365, 5, 'Film je predobar, čista desetka 10!', 1, 'andrija1'),
(20, 254128, 5, 'Film vredan gledanja, okvirna osmica!', 1, 'andrija1'),
(21, 976573, 6, 'Lep porodicni film!', 1, 'milos1');

-- --------------------------------------------------------

--
-- Table structure for table `korisnici`
--

CREATE TABLE `korisnici` (
  `id` int(11) NOT NULL,
  `korisnickoime` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `lozinka` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `korisnici`
--

INSERT INTO `korisnici` (`id`, `korisnickoime`, `email`, `lozinka`) VALUES
(1, 'Andrija', 'andrija.t223@gmail.com', 'pbkdf2:sha256:260000$vbjYU1Riv1ub4bWg$34790fd59dd468b1ee1d9803ab91988b8eea913657cd3dab433babf724d3178b'),
(2, 'andrijaandrija', 'andrijadasd.com', 'pbkdf2:sha256:260000$2ukwjezO2rbhrcR1$5d37f6ce2770f7f4b94ff2a222d4546fcded33780d65b58ab814a97eeab654a8'),
(3, 'andrijaandrija', 'andrijadasd@.com', 'pbkdf2:sha256:260000$p5LQes22xERYy7Oz$9dd0cb5fe22ac8861a8e118246a990b73de42db0f53371650f77e96b3b22a60c'),
(4, 'Akikawasaki', 'akikawasaki@gmail.com', 'pbkdf2:sha256:260000$p76OIhtEv2evAxdU$f32d4c59e20ac707c977657f931cbbbd5ba2124118bf1815b2c0733666bccdb0'),
(5, 'andrija1', 'andrija1@gmail.com', 'pbkdf2:sha256:260000$B3TYYw5veXMptFQu$b603004915b510e099189e9162f78cce30f134f87acc06d85fc474e6883330e2'),
(6, 'milos1', 'milos1@gmail.com', 'pbkdf2:sha256:260000$9NrlXR5hA8dVoYC4$ea8bfd125dad43141b55b3cbe503619e68f6073b76b4de78ee561933fa981007'),
(7, 'prokiller', 'prokiller@gmail.com', 'pbkdf2:sha256:260000$q88QoHpMN3ZCDPVI$3ca9e16ff4c37c350506108afe14e2fe5fbae41efffdf34833293f5926c85e31');

-- --------------------------------------------------------

--
-- Table structure for table `watchlist`
--

CREATE TABLE `watchlist` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `movie_id` int(11) DEFAULT NULL,
  `title` varchar(200) NOT NULL,
  `opis` varchar(200) NOT NULL,
  `poster_path` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `watchlist`
--

INSERT INTO `watchlist` (`id`, `user_id`, `movie_id`, `title`, `opis`, `poster_path`) VALUES
(190, 5, 447365, 'Čuvari galaksije: Volume 3', 'James Gunn je redatelj i scenarist, Kevin Feige je producent, a izvršni producenti su Louis D’Esposit, Victoria Alons, Nikolas Korda, Sara Smith i Simon Hatt.  Voljena banda vodi miran život na Knowhe', '/2ZoltS7nPhcXhtr4no1ejDeU5zL.jpg'),
(191, 5, 385687, 'Brzi i žestoki 10', 'Tijekom mnogih misija i protiv nemogućih izgleda, Dom Toretto i njegova obitelj nadmudrili su, iznervirali i nadmašili svakog neprijatelja na svom putu. Sada se suočavaju s najsmrtonosnijim protivniko', '/cTctDhck3tthYEwX46BjNTHP1fq.jpg'),
(192, 5, 254128, 'San Andreas', 'Priča prati pilota helikoptera i spasioca Raya koji nakon stravičnog potresa kreće iz Los Angelesa u San Francisco sa svojom suprugom, s kojom nije u najboljim odnosima, kako bi spasili kćer jedinicu.', '/vH82hkfbpCJaw4ibSYOTLY0EP6k.jpg'),
(193, 5, 569094, 'Spider-Man: Putovanje kroz Spider-svijet', 'Nakon ponovnog ujedinjenja s Gwen Stacy, Brooklynov prijateljski nastrojeni Spider-Man iz susjedstva katapultira se preko Multiverzuma, gdje susreće tim Spider-ljudi zaduženih za zaštitu njegovog post', '/hTFdZpsAJef47GPFiATVNCkN03c.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `wishlist`
--

CREATE TABLE `wishlist` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `idfilma` text NOT NULL,
  `poster_path` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `administratori`
--
ALTER TABLE `administratori`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `komentari`
--
ALTER TABLE `komentari`
  ADD PRIMARY KEY (`id`),
  ADD KEY `korisnik_id` (`korisnik_id`);

--
-- Indexes for table `korisnici`
--
ALTER TABLE `korisnici`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `watchlist`
--
ALTER TABLE `watchlist`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `wishlist`
--
ALTER TABLE `wishlist`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `administratori`
--
ALTER TABLE `administratori`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `komentari`
--
ALTER TABLE `komentari`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `korisnici`
--
ALTER TABLE `korisnici`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `watchlist`
--
ALTER TABLE `watchlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=195;

--
-- AUTO_INCREMENT for table `wishlist`
--
ALTER TABLE `wishlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `komentari`
--
ALTER TABLE `komentari`
  ADD CONSTRAINT `komentari_ibfk_1` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnici` (`id`);

--
-- Constraints for table `watchlist`
--
ALTER TABLE `watchlist`
  ADD CONSTRAINT `watchlist_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `korisnici` (`id`);

--
-- Constraints for table `wishlist`
--
ALTER TABLE `wishlist`
  ADD CONSTRAINT `wishlist_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `korisnici` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
