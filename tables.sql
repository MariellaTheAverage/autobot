create table if not exists orders (
    oid int not null AUTO_INCREMENT,
    address varchar(100) not null,
    phone varchar(20),
    item varchar(300) not null default "-",
    usrid int not null,
    taken bit(1) not null default 0,
    assigned bit(1) default 0,
    driverid int,
    primary key (oid),
    foreign key (driverid) references drivers(uid)
)

create table if not exists drivers (
    uid int not null,
    pickupcnt int not null,
    primary key (uid)
)