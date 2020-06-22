-- Create tables:
-- 1) ParkingLotTmp: CORE
-- RFID cannot be duplicate over each parking lot
-- because we cannot have the same RFID card for 
-- > 2 vehicles.

CREATE TABLE Parking
(
    RFID    char(12),
    ParkingLotID    char(6),
    PlateNumber     VARCHAR(15),
    PlateImgURL     VARCHAR(255),
    CheckInTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0),
    CONSTRAINT PK_Parking_RFID_ParkingLotID
    PRIMARY KEY(RFID, ParkingLotID)
);
drop TABLE Parking;
alter table Parking
add ParkingLotID char(6);

alter table parking
add CONSTRAINT PK_Parking_RFID_ParkingLotID
PRIMARY KEY(RFID, ParkingLotID);
-- alter table Parking
-- add StaffID char(6);

-- drop table Parking;
-- alter table Parking
-- add CheckInTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0);
--drop column checkintime;
-- drop TABLE parking;

-- 2) ParkingLotHistory: CORE

CREATE TABLE History
(
    ParkingID SERIAL,
    RFID    char(12),
    ParkingLotID char(6),
    PlateNumber VARCHAR(15),
    PlateImgURL VARCHAR(255),
    StaffID     char(6),
    CameraID    char(6),
    InOrOut     BOOLEAN,
    CheckTime   timestamp,
    CONSTRAINT  PK_History_ParkingID
    primary key(ParkingID)
);
-- alter table History
-- add ParkingLotID char(6);
-- alter table history
-- drop column CheckInTime;
-- ALTER TABLE history
-- Drop column CheckOutTime;
-- ALTER TABLE history
-- add InOrOut BOOLEAN;
-- ALTER TABLE history
-- add CheckTime timestamp;


-- ALTER TABLE history
-- add CheckInTime TIMESTAMP;

-- ALTER TABLE history
-- add CheckInTime TIMESTAMP;



-- alter TABLE history
-- drop column CheckInTime;
-- ALTER TABLE history
-- drop COLUMN CheckInOut; 
-- alter TABLE History
-- drop column ParkingTime;
-- 3) Staff:
-- Can add birthday, PersonalID,...
-- address, 
create  TABLE StaffList
(
    StaffID     char(6),
    StaffFullname   VARCHAR(30),
    parkinglotid char(6),
    CONSTRAINT PK_Staff_StaffID
    PRIMARY KEY(StaffID)
);
-- drop TABLE Staff;
-- alter table stafflist
-- add parkinglotid char(6);
-- 4)  ParkingLot:
create TABLE ParkingLotList
(
    ParkingLotID    CHAR(6),
    ParkingLotName  VARCHAR(40),
    CONSTRAINT  PK_ParkingLotList_ParkingLotID
    PRIMARY KEY(ParkingLotID)
);

insert into parkinglotlist
(ParkingLotID, ParkingLotName)
VALUES
(
    'PKL001',
    'Parking Lot 1'
);
-- TRUNCATE TABLE parkinglotlist;
-- 5) CameraList:

create TABLE CameraList
(
    CameraID    CHAR(6),
    ParkingLotID    CHAR(6),
    CameraBrand VARCHAR(20),
    CameraSpec  VARCHAR(40),
    InOrOut     BOOLEAN,
    CONSTRAINT  PK_CameraList_CameraID
    PRIMARY KEY(CameraID)
);
alter table CameraList add InOrOut     BOOLEAN;
-- TRUNCATE table CameraList;
-- drop table cameralist;
-- alter table History
-- add RFID char(12);
-- alter TABLE cameralist
-- add ParkingLotID CHAR(6);

-- alter TABLE cameralist
-- add CONSTRAINT  PK_CameraList_CameraID
-- primary key(CameraID, ParkingLotID);
-- drop CONSTRAINT  PK_CameraList_CameraID;

-- create TABLE RFIDList
-- (
--     RFID    char(12),
--     ParkingLotID char(6),
--     BarCode char()
-- );

-- drop table rfidlist;
insert into Parking
(RFID, ParkingLotID, PlateNumber, PlateImgURL)
VALUES
(
    '123456',
    'PKL001',
    '43A12345',
    '/home/khoa/img' 
);

insert into Parking
(RFID, ParkingLotID, PlateNumber, PlateImgURL)
VALUES
(
    '111111',
    'PKL001',
    '43A12346',
    '/home/khoa/img'
);

insert into Parking
(RFID, ParkingLotID, PlateNumber, PlateImgURL)
VALUES
(
    '12345999',
    'PKL002',
    '92A99999',
    '/home/khoa/img'
);


-- Add foreign key:
alter table stafflist
add CONSTRAINT FK_STAFFLIST_PARKINGLOTLIST_ParkingLotID
foreign key (ParkingLotID) REFERENCES ParkingLotList(ParkingLotID) ON DELETE CASCADE;

alter table cameralist
add CONSTRAINT FK_CAMERALIST_PARKINGLOTLIST_ParkingLotID
foreign key (ParkingLotID) REFERENCES ParkingLotList(ParkingLotID) ON DELETE CASCADE;

alter table rfidlist
add CONSTRAINT FK_RFIDLIST_PARKINGLOTLIST_ParkingLotID
foreign key (ParkingLotID) REFERENCES ParkingLotList(ParkingLotID) ON DELETE CASCADE;


-- foreign key 2 core tables: parking & history
alter table parking
add CONSTRAINT FK_PARKING_PARKINGLOTLIST_ParkingLotID 
FOREIGN KEY(ParkingLotID) REFERENCES parkingLotList(ParkingLotID) ON DELETE CASCADE;

alter table history
add constraint FK_HISTORY_PARKINGLOTLIST_ParkingLotID
foreign key(ParkingLotID) references parkingLotList(ParkingLotID) ON DELETE CASCADE;

alter table history
add constraint FK_HISTORY_STAFFLIST_StaffID
foreign key(StaffID) references StaffList(StaffID);

alter table history
add constraint FK_HISTORY_CAMERALIST_CameraID
foreign key(CameraID) references CameraList(CameraID);


-- alter table history
-- drop constraint FK_HISTORY_CAMERALIST_CameraID
