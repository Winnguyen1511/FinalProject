-- 1) Parking Lot List:
insert into parkinglotlist
(ParkingLotID, ParkingLotName)
VALUES
('PKL001', 'Parking Lot 1');

insert into parkinglotlist
(ParkingLotID, ParkingLotName)
VALUES
('PKL002', 'Parking Lot 2');

insert into parkinglotlist
(ParkingLotID, ParkingLotName)
VALUES
('PKL003', 'Parking Lot 1');

-- 2) Staff List:
insert into StaffList
(StaffID, StaffFullname, ParkingLotID)
VALUES
('STF001', 'Nguyen Huynh Dang Khoa', 'PKL001');

insert into StaffList
(StaffID, StaffFullname, ParkingLotID)
VALUES
('STF002', 'Nguyen Van A', 'PKL001');

insert into StaffList
(StaffID, StaffFullname, ParkingLotID)
VALUES
('STF003', 'Nguyen Van B', 'PKL002'); 

-- 3) CameraList: 

insert into CameraList
(CameraID,ParkingLotID,CameraBrand, CameraSpec, InOrOut)
VALUES
('CM0001', 'PKL001','Logitech','', TRUE);

insert into CameraList
(CameraID,ParkingLotID,CameraBrand, CameraSpec, InOrOut)
VALUES
('CM0002', 'PKL001','Logitech','', FALSE);

insert into CameraList
(CameraID,ParkingLotID,CameraBrand, CameraSpec, InOrOut)
VALUES
('CM0003', 'PKL002','Sony','', TRUE);



