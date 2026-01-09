USE livestock_app;

INSERT INTO administrative_level (name) VALUES
('Huyện'),
('Xã');

INSERT INTO administrative_unit (name, administrative_id, level_id) VALUES 
('Đông Anh', NULL, 1),
('Cầu Giấy', NULL, 1),
('Hoàn Kiếm', NULL, 1);

INSERT INTO administrative_unit (name, administrative_id, level_id) VALUES 
-- Xã thuộc Đông Anh
('Xã Thụy Lâm', 1, 2),
('Xã Dục Tú', 1, 2),
('Xã Liên Hà', 1, 2),

-- Xã thuộc Cầu Giấy
('Phường Dịch Vọng', 2, 2),
('Phường Nghĩa Đô', 2, 2),
('Phường Quan Hoa', 2, 2),

-- Xã thuộc Hoàn Kiếm
('Phường Tràng Tiền', 3, 2),
('Phường Lý Thái Tổ', 3, 2),
('Phường Phan Chu Trinh', 3, 2);

INSERT INTO permissions (name, code, description) VALUES
('Quản lý người dùng', 'USER_MANAGE', 'CRUD người dùng'),
('Quản lý nhóm', 'GROUP_MANAGE', 'CRUD nhóm người dùng'),
('Quản lý phân quyền', 'PERMISSION_MANAGE', 'Gán quyền'),
('Quản lý đơn vị hành chính', 'ADMIN_UNIT_MANAGE', 'CRUD đơn vị hành chính'),
('Xem lịch sử', 'HISTORY_VIEW', 'Xem lịch sử hệ thống'),
('Quản lý giống vật nuôi', 'SPECIES_MANAGE', 'CRUD giống'),
('Quản lý nguồn gen', 'GEN_MANAGE', 'CRUD nguồn gen'),
('Quản lý cơ sở', 'FACILITY_MANAGE', 'CRUD cơ sở'),
('Quản lý thức ăn', 'FOOD_MANAGE', 'CRUD thức ăn'),
('Quản lý chất cấm', 'SUBSTANCE_MANAGE', 'CRUD chất cấm'),
('Xem báo cáo', 'REPORT_VIEW', 'Xem báo cáo');

INSERT INTO `group` (name, description) VALUES
('ADMIN', 'Quản trị hệ thống'),
('OFFICER', 'Cán bộ quản lý'),
('VIEWER', 'Chỉ xem dữ liệu');

INSERT INTO group_permissions (group_id, permissions_id)
SELECT 1, id FROM permissions;

INSERT INTO group_permissions (group_id, permissions_id)
SELECT 2, id FROM permissions
WHERE code IN (
    'SPECIES_MANAGE',
    'GEN_MANAGE',
    'FACILITY_MANAGE',
    'FOOD_MANAGE',
    'SUBSTANCE_MANAGE',
    'REPORT_VIEW'
);

INSERT INTO group_permissions (group_id, permissions_id)
SELECT 3, id FROM permissions
WHERE code IN (
    'REPORT_VIEW',
    'HISTORY_VIEW'
);

INSERT INTO user (fullname, email, phone, status, unit_id)
VALUES ('Administrator', 'admin@system.local', '0000000000', 1, 3);

INSERT INTO account (username, password, user_id)
VALUES (
    'admin',
    '$2b$12$E/vdYnBMDe9oL1wrEdFNiu5rf3JyWiIQN1zrC9XcMJsTfQUQoT16.',
    1,
);

INSERT INTO user_groups (user_id, group_id)
VALUES (1, 1);

INSERT INTO activities_history (account_id, activities)
VALUES (1, 'Khởi tạo hệ thống');

INSERT INTO user (fullname, email, phone, status, unit_id) VALUES 
	('Officer', 'officer@gmail.local', '0000000001', 2, 2),
    ('viewer', 'viewer@gmail.local', '0000000032', 3, 2),
    ('admin2', 'admin2@system.local', '0000032354', 1, 1);


INSERT INTO account (username, password, user_id) VALUES
('officer', '$2b$12$8t10lp.DnuoFzBBt887zB.ixskfOu0uACCTHi1090sj4sXT34wouS', 2),
('viewer', '$2b$12$Mz5WxvP69hl0L03JUZwKuOL1nngM6TeNr5p/HXjVWIXsVV3z6oEAW', 3),
('admin2', '$2b$12$3/91KjHCqXhbXjrzO6eHVOvQvtILn8xyb5Rg4amLsQNZ8IxMIZGza', 4);

UPDATE user SET status = 1 WHERE id = 1;
UPDATE user SET status = 1 WHERE id IN ('1', '2', '3', '4');