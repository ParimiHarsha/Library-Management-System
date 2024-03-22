DROP DATABASE IF EXISTS LibraryManagementSystem;
CREATE DATABASE LibraryManagementSystem;
USE LibraryManagementSystem;

create table  Publisher
(     
ID integer AUTO_INCREMENT,
NAME varchar(100) not null,
CITY varchar(50),
ZIP numeric(10),
PRIMARY KEY(ID)
);

create table Writer
(
ID integer AUTO_INCREMENT,
Name varchar(100) not null,
Age numeric(10),
Gender char(1) not null,
Qualification varchar(50),
PRIMARY KEY(ID)
);

create table Books
(
ID integer AUTO_INCREMENT,
Name varchar(500),
ISBN varchar(30) not null,
Writer_ID integer,
Publisher_ID integer,
PRIMARY KEY(ID),
FOREIGN KEY(Publisher_ID) REFERENCES Publisher(ID) ON DELETE CASCADE,
FOREIGN KEY(Writer_ID) REFERENCES Writer(ID) ON DELETE CASCADE
);


create table Branch
(
ID integer AUTO_INCREMENT,
Street varchar(50),
City varchar(50) not null,
State varchar(10) not null,
Zip numeric(10),
PRIMARY KEY(ID)
);

create table Reader
(
ID integer AUTO_INCREMENT,
Name varchar(100) not null,
Email varchar(100),
Phone varchar(20),
City varchar(50),
Zip numeric(10),
PRIMARY KEY(ID)
);

create table Loaned
(
Reader_ID integer  not null,
Book_ID integer not null,
Branch_ID integer not null,
Issue_Date date,
Return_Date date,
PRIMARY KEY(Reader_ID, Book_ID),
FOREIGN KEY(Reader_ID) REFERENCES Reader(ID) ON DELETE CASCADE,
FOREIGN KEY(Book_ID) REFERENCES Books(ID) ON DELETE CASCADE,
FOREIGN KEY(Branch_ID) REFERENCES Branch(ID) ON DELETE CASCADE
);
