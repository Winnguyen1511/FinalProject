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

-- drop table Parking;
-- alter table Parking
-- add CheckInTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0);
--drop column checkintime;
-- drop TABLE parking;

-- 2) ParkingLotHistory: CORE

CREATE TABLE History
(
    ParkingID SERIAL,
    RFID    char(64),
    PlateNumber VARCHAR(15),
    PlateImgURL VARCHAR(255),
    StaffID     char(6),
    ParkingLotID    char(6),
    CameraID    char(6),
    InOrOut     BOOLEAN,
    CheckTime   timestamp,
    CONSTRAINT  PK_History_ParkingID
    primary key(ParkingID)
);
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

ALTER TABLE history
add CheckOutTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0);


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
    CONSTRAINT PK_Staff_StaffID
    PRIMARY KEY(StaffID)
);
-- drop TABLE Staff;

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
    CONSTRAINT  PK_CameraList_CameraID
    PRIMARY KEY(CameraID, ParkingLotID)
);

-- alter TABLE cameralist
-- add ParkingLotID CHAR(6);

-- alter TABLE cameralist
-- add CONSTRAINT  PK_CameraList_CameraID
-- primary key(CameraID, ParkingLotID);
-- drop CONSTRAINT  PK_CameraList_CameraID;

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
