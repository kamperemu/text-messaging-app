create database textapp;
use textapp;

create table details(
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username char(50) unique NOT NULL ,
    password char(50) NOT NULL
);

select * from details;
show tables;
drop table details;
desc details;
delete from details;

insert into details values ('ram','raj');