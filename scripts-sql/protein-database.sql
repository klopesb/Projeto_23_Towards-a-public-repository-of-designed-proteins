-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema protein_database
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `protein_database` DEFAULT CHARACTER SET utf8mb3 ;
USE `protein_database` ;

-- -----------------------------------------------------
-- Table `protein_database`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protein_database`.`categories` (
  `id_category` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_category`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `protein_database`.`design`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protein_database`.`design` (
  `id_design` INT NOT NULL AUTO_INCREMENT,
  `design_name` VARCHAR(45) NULL DEFAULT NULL,
  `pdb_id` VARCHAR(45) NULL DEFAULT NULL,
  `ref_link` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_design`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `protein_database`.`protocol`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protein_database`.`protocol` (
  `id_protocol` INT NOT NULL AUTO_INCREMENT,
  `protocol_name` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_protocol`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `protein_database`.`used_techniques`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protein_database`.`used_techniques` (
  `id_techniques` INT NOT NULL AUTO_INCREMENT,
  `fk_id_design` INT NOT NULL,
  `technique_name` VARCHAR(45) NULL DEFAULT NULL,
  `technique_type` ENUM('experimental', 'computational') NULL DEFAULT NULL,
  `ref_doc` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_techniques`, `fk_id_design`),
  INDEX `fk_used_techniques_design1_idx` (`fk_id_design` ASC) VISIBLE,
  UNIQUE INDEX `id_techniques_UNIQUE` (`id_techniques` ASC) VISIBLE,
  CONSTRAINT `fk_used_techniques_design1`
    FOREIGN KEY (`fk_id_design`)
    REFERENCES `protein_database`.`design` (`id_design`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `protein_database`.`assays`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protein_database`.`assays` (
  `id_assays` INT NOT NULL AUTO_INCREMENT,
  `fk_id_protocol` INT NOT NULL,
  `fk_id_category` INT NOT NULL,
  `fk_id_design` INT NOT NULL,
  `fk_id_techniques` INT NOT NULL,
  `assay_name` VARCHAR(45) NULL DEFAULT NULL,
  `success_validation` TINYINT(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id_assays`, `fk_id_protocol`, `fk_id_category`, `fk_id_design`, `fk_id_techniques`),
  INDEX `fk_assays_protocol_idx` (`fk_id_protocol` ASC) VISIBLE,
  INDEX `fk_assays_categories1_idx` (`fk_id_category` ASC) VISIBLE,
  INDEX `fk_assays_design1_idx` (`fk_id_design` ASC) VISIBLE,
  INDEX `fk_assays_used_techniques1_idx` (`fk_id_techniques` ASC) VISIBLE,
  CONSTRAINT `fk_assays_categories1`
    FOREIGN KEY (`fk_id_category`)
    REFERENCES `protein_database`.`categories` (`id_category`),
  CONSTRAINT `fk_assays_design1`
    FOREIGN KEY (`fk_id_design`)
    REFERENCES `protein_database`.`design` (`id_design`),
  CONSTRAINT `fk_assays_protocol`
    FOREIGN KEY (`fk_id_protocol`)
    REFERENCES `protein_database`.`protocol` (`id_protocol`),
  CONSTRAINT `fk_assays_used_techniques1`
    FOREIGN KEY (`fk_id_techniques`)
    REFERENCES `protein_database`.`used_techniques` (`id_techniques`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `protein_database`.`computational_results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protein_database`.`computational_results` (
  `id_computational_results` INT NOT NULL AUTO_INCREMENT,
  `fk_id_techniques` INT NOT NULL,
  `fk_id_design` INT NOT NULL,
  `result_file` MEDIUMBLOB NULL DEFAULT NULL,
  PRIMARY KEY (`id_computational_results`, `fk_id_techniques`, `fk_id_design`),
  INDEX `fk_computational_results_used_techniques1_idx` (`fk_id_techniques` ASC, `fk_id_design` ASC) VISIBLE,
  CONSTRAINT `fk_computational_results_used_techniques1`
    FOREIGN KEY (`fk_id_techniques` , `fk_id_design`)
    REFERENCES `protein_database`.`used_techniques` (`id_techniques` , `fk_id_design`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `protein_database`.`experimental_results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protein_database`.`experimental_results` (
  `id_experimental_results` INT NOT NULL AUTO_INCREMENT,
  `fk_id_techniques` INT NOT NULL,
  `fk_id_design` INT NOT NULL,
  `result_file` MEDIUMBLOB NULL DEFAULT NULL,
  PRIMARY KEY (`id_experimental_results`, `fk_id_techniques`, `fk_id_design`),
  INDEX `fk_experimental_results_used_techniques1_idx` (`fk_id_techniques` ASC, `fk_id_design` ASC) VISIBLE,
  CONSTRAINT `fk_experimental_results_used_techniques1`
    FOREIGN KEY (`fk_id_techniques` , `fk_id_design`)
    REFERENCES `protein_database`.`used_techniques` (`id_techniques` , `fk_id_design`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `protein_database`.`sequences`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protein_database`.`sequences` (
  `id_sequences` INT NOT NULL AUTO_INCREMENT,
  `fk_id_design` INT NOT NULL,
  `chain_id` VARCHAR(45) NULL DEFAULT NULL,
  `sequence` TEXT NULL DEFAULT NULL,
  `length` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_sequences`, `fk_id_design`),
  INDEX `fk_sequences_design1_idx` (`fk_id_design` ASC) VISIBLE,
  CONSTRAINT `fk_sequences_design1`
    FOREIGN KEY (`fk_id_design`)
    REFERENCES `protein_database`.`design` (`id_design`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `protein_database`.`specific_property`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protein_database`.`specific_property` (
  `id_sp` INT NOT NULL AUTO_INCREMENT,
  `fk_id_category` INT NOT NULL,
  `sp_name` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_sp`, `fk_id_category`),
  INDEX `fk_specific_property_categories1_idx` (`fk_id_category` ASC) VISIBLE,
  UNIQUE INDEX `id_sp_UNIQUE` (`id_sp` ASC) VISIBLE,
  CONSTRAINT `fk_specific_property_categories1`
    FOREIGN KEY (`fk_id_category`)
    REFERENCES `protein_database`.`categories` (`id_category`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `protein_database`.`unit`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protein_database`.`unit` (
  `id_unit` INT NOT NULL AUTO_INCREMENT,
  `unit_name` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id_unit`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `protein_database`.`unit_has_specific_property`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `protein_database`.`unit_has_specific_property` (
  `fk_id_unit` INT NOT NULL,
  `fk_id_sp` INT NOT NULL,
  PRIMARY KEY (`fk_id_unit`, `fk_id_sp`),
  INDEX `fk_unit_has_specific_property_specific_property1_idx` (`fk_id_sp` ASC) VISIBLE,
  INDEX `fk_unit_has_specific_property_unit1_idx` (`fk_id_unit` ASC) VISIBLE,
  CONSTRAINT `fk_unit_has_specific_property_specific_property1`
    FOREIGN KEY (`fk_id_sp`)
    REFERENCES `protein_database`.`specific_property` (`id_sp`),
  CONSTRAINT `fk_unit_has_specific_property_unit1`
    FOREIGN KEY (`fk_id_unit`)
    REFERENCES `protein_database`.`unit` (`id_unit`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
