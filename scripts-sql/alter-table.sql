alter table assays
add assay_name VARCHAR(45),
add success_validation boolean;

ALTER table categories
add category_name varchar(45);

alter table computational_results
add result_file mediumblob;

alter table experimental_results
add result_file mediumblob;

alter table design
add design_name varchar(45),
add pdb_id varchar(45),
add ref_link varchar(45);

alter table protocol
add protocol_name varchar(45);

alter table sequences
add chain_id varchar(45),
add sequence text,
add length varchar(45);

alter table specific_property
add sp_name varchar(45);

alter table unit
add unit_name varchar(45);

UPDATE unit SET unit_name = '°C' WHERE id_unit = 1;
UPDATE unit SET unit_name = 's⁻¹' WHERE id_unit = 2;

ALTER TABLE unit
MODIFY COLUMN unit_name VARCHAR(20);

alter table used_techniques
add technique_name varchar(45),
add technique_type enum('experimental', 'computational'),
add ref_doc varchar(45);

-- alter tables to put AI on PK 
alter table used_techniques
modify column id_used_techniques int not null auto_increment;

-- select all FK 
SELECT 
    CONSTRAINT_NAME, 
    TABLE_NAME, 
    COLUMN_NAME, 
    REFERENCED_TABLE_NAME, 
    REFERENCED_COLUMN_NAME
FROM 
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE 
    TABLE_SCHEMA = 'protein_database' -- Nome do seu banco de dados
    AND REFERENCED_TABLE_NAME IS NOT NULL;

select * from protocol;

SELECT id_used_techniques, design_id_design FROM used_techniques;



