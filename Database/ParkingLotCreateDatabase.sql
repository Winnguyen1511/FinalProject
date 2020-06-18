-- Create tables:
-- 1) ParkingLotTmp: CORE
-- RFID cannot be duplicate over each parking lot
-- because we cannot have the same RFID card for 
-- > 2 vehicles.

CREATE TABLE Parking
(
    RFID    char(64),
    ParkingLotID    char(6),
    PlateNumber     VARCHAR(15),
    PlateImgURL     VARCHAR(255),
    CheckInTime TIMESTAMP,
    CONSTRAINT PK_ParkingTmp_RFID_ParkingLotID
    PRIMARY KEY(RFID, ParkingLotID)
);

-- drop TABLE parking;

-- 2) ParkingLotHistory: CORE

CREATE TABLE History
(
    ParkingID SERIAL,
    ParkingTime TIMESTAMP,
    RFID    char(64),
    PlateNumber VARCHAR(15),
    PlateImgURL VARCHAR(255),
    StaffID     char(6),
    ParkingLotID    char(6),
    CameraID    char(6),
    CheckInTime TIMESTAMP,
    CheckOutTime    TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0),
    CONSTRAINT  PK_History_ParkingID
    primary key(ParkingID)
);

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