-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema pd_database
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema pd_database
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pd_database` DEFAULT CHARACTER SET utf8 ;
USE `pd_database` ;

-- -----------------------------------------------------
-- Table `pd_database`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pd_database`.`categories` (
  `id_categories` INT NOT NULL,
  `category_name` VARCHAR(45) NULL,
  PRIMARY KEY (`id_categories`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pd_database`.`design`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pd_database`.`design` (
  `id_design` INT NOT NULL,
  `design_name` VARCHAR(45) NULL,
  `organism` VARCHAR(45) NULL,
  `ref_link` VARCHAR(45) NULL,
  `design_type` ENUM('De Novo Design', 'Protein Engineering') NULL,
  PRIMARY KEY (`id_design`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pd_database`.`used_techniques`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pd_database`.`used_techniques` (
  `id_techniques` INT NOT NULL,
  `technique_name` VARCHAR(45) NULL,
  `fk_id_design` INT NOT NULL,
  PRIMARY KEY (`id_techniques`, `fk_id_design`),
  INDEX `fk_used_techniques_design1_idx` (`fk_id_design` ASC) VISIBLE,
  UNIQUE INDEX `id_techniques_UNIQUE` (`id_techniques` ASC) VISIBLE,
  CONSTRAINT `fk_used_techniques_design1`
    FOREIGN KEY (`fk_id_design`)
    REFERENCES `pd_database`.`design` (`id_design`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pd_database`.`protocol`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pd_database`.`protocol` (
  `id_protocol` INT NOT NULL,
  `protocol_name` VARCHAR(45) NULL,
  PRIMARY KEY (`id_protocol`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pd_database`.`assays`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pd_database`.`assays` (
  `id_assays` INT NOT NULL,
  `assay_name` VARCHAR(45) NULL,
  `success_validation` TINYINT NULL,
  `fk_id_categories` INT NOT NULL,
  `fk_id_design` INT NOT NULL,
  `fk_id_techniques` INT NOT NULL,
  `fk_id_protocol` INT NOT NULL,
  PRIMARY KEY (`id_assays`, `fk_id_categories`, `fk_id_design`, `fk_id_techniques`, `fk_id_protocol`),
  INDEX `fk_assays_categories_idx` (`fk_id_categories` ASC) VISIBLE,
  INDEX `fk_assays_design1_idx` (`fk_id_design` ASC) VISIBLE,
  INDEX `fk_assays_used_techniques1_idx` (`fk_id_techniques` ASC) VISIBLE,
  INDEX `fk_assays_protocol1_idx` (`fk_id_protocol` ASC) VISIBLE,
  CONSTRAINT `fk_assays_categories`
    FOREIGN KEY (`fk_id_categories`)
    REFERENCES `pd_database`.`categories` (`id_categories`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_assays_design1`
    FOREIGN KEY (`fk_id_design`)
    REFERENCES `pd_database`.`design` (`id_design`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_assays_used_techniques1`
    FOREIGN KEY (`fk_id_techniques`)
    REFERENCES `pd_database`.`used_techniques` (`id_techniques`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_assays_protocol1`
    FOREIGN KEY (`fk_id_protocol`)
    REFERENCES `pd_database`.`protocol` (`id_protocol`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pd_database`.`specific_property`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pd_database`.`specific_property` (
  `id_sp` INT NOT NULL,
  `sp_name` VARCHAR(45) NULL,
  `fk_id_categories` INT NOT NULL,
  PRIMARY KEY (`id_sp`, `fk_id_categories`),
  INDEX `fk_specific_property_categories1_idx` (`fk_id_categories` ASC) VISIBLE,
  CONSTRAINT `fk_specific_property_categories1`
    FOREIGN KEY (`fk_id_categories`)
    REFERENCES `pd_database`.`categories` (`id_categories`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pd_database`.`sequences`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pd_database`.`sequences` (
  `id_sequences` INT NOT NULL,
  `sequence` TEXT NOT NULL,
  `length` VARCHAR(45) NULL,
  `chain_id` VARCHAR(45) NULL,
  PRIMARY KEY (`id_sequences`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pd_database`.`computational_results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pd_database`.`computational_results` (
  `id_computational_results` INT NOT NULL,
  `result_value` FLOAT NOT NULL,
  `fk_id_techniques` INT NOT NULL,
  `fk_id_design` INT NOT NULL,
  `fk_id_sequences` INT NOT NULL,
  PRIMARY KEY (`id_computational_results`, `fk_id_techniques`, `fk_id_design`, `fk_id_sequences`),
  INDEX `fk_computational_results_used_techniques1_idx` (`fk_id_techniques` ASC, `fk_id_design` ASC) VISIBLE,
  INDEX `fk_computational_results_sequences1_idx` (`fk_id_sequences` ASC) VISIBLE,
  CONSTRAINT `fk_computational_results_used_techniques1`
    FOREIGN KEY (`fk_id_techniques` , `fk_id_design`)
    REFERENCES `pd_database`.`used_techniques` (`id_techniques` , `fk_id_design`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_computational_results_sequences1`
    FOREIGN KEY (`fk_id_sequences`)
    REFERENCES `pd_database`.`sequences` (`id_sequences`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pd_database`.`experimental_results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pd_database`.`experimental_results` (
  `id_experimental_results` INT NOT NULL,
  `result_value` FLOAT NOT NULL,
  `fk_id_techniques` INT NOT NULL,
  `fk_id_design` INT NOT NULL,
  `fk_id_sequences` INT NOT NULL,
  PRIMARY KEY (`id_experimental_results`, `fk_id_techniques`, `fk_id_design`, `fk_id_sequences`),
  INDEX `fk_experimental_results_used_techniques1_idx` (`fk_id_techniques` ASC, `fk_id_design` ASC) VISIBLE,
  INDEX `fk_experimental_results_sequences1_idx` (`fk_id_sequences` ASC) VISIBLE,
  CONSTRAINT `fk_experimental_results_used_techniques1`
    FOREIGN KEY (`fk_id_techniques` , `fk_id_design`)
    REFERENCES `pd_database`.`used_techniques` (`id_techniques` , `fk_id_design`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_experimental_results_sequences1`
    FOREIGN KEY (`fk_id_sequences`)
    REFERENCES `pd_database`.`sequences` (`id_sequences`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pd_database`.`unit`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pd_database`.`unit` (
  `id_unit` INT NOT NULL,
  `unit_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_unit`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pd_database`.`unit_has_specific_property`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pd_database`.`unit_has_specific_property` (
  `fk_id_unit` INT NOT NULL,
  `fk_id_sp` INT NOT NULL,
  `fk_id_categories` INT NOT NULL,
  PRIMARY KEY (`fk_id_unit`, `fk_id_sp`, `fk_id_categories`),
  INDEX `fk_unit_has_specific_property_specific_property1_idx` (`fk_id_sp` ASC, `fk_id_categories` ASC) VISIBLE,
  INDEX `fk_unit_has_specific_property_unit1_idx` (`fk_id_unit` ASC) VISIBLE,
  CONSTRAINT `fk_unit_has_specific_property_unit1`
    FOREIGN KEY (`fk_id_unit`)
    REFERENCES `pd_database`.`unit` (`id_unit`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_unit_has_specific_property_specific_property1`
    FOREIGN KEY (`fk_id_sp` , `fk_id_categories`)
    REFERENCES `pd_database`.`specific_property` (`id_sp` , `fk_id_categories`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pd_database`.`sequences_has_assays`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pd_database`.`sequences_has_assays` (
  `fk_id_sequences` INT NOT NULL,
  `fk_id_assays` INT NOT NULL,
  `fk_id_categories` INT NOT NULL,
  `fk_id_design` INT NOT NULL,
  `fk_id_techniques` INT NOT NULL,
  `fk_id_protocol` INT NOT NULL,
  PRIMARY KEY (`fk_id_sequences`, `fk_id_assays`, `fk_id_categories`, `fk_id_design`, `fk_id_techniques`, `fk_id_protocol`),
  INDEX `fk_sequences_has_assays_assays1_idx` (`fk_id_assays` ASC, `fk_id_categories` ASC, `fk_id_design` ASC, `fk_id_techniques` ASC, `fk_id_protocol` ASC) VISIBLE,
  INDEX `fk_sequences_has_assays_sequences1_idx` (`fk_id_sequences` ASC) VISIBLE,
  CONSTRAINT `fk_sequences_has_assays_sequences1`
    FOREIGN KEY (`fk_id_sequences`)
    REFERENCES `pd_database`.`sequences` (`id_sequences`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_sequences_has_assays_assays1`
    FOREIGN KEY (`fk_id_assays` , `fk_id_categories` , `fk_id_design` , `fk_id_techniques` , `fk_id_protocol`)
    REFERENCES `pd_database`.`assays` (`id_assays` , `fk_id_categories` , `fk_id_design` , `fk_id_techniques` , `fk_id_protocol`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
