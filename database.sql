drop database if exists CavoshCafe;
create database CavoshCafe;
use CavoshCafe;

create table Distrito(
  id int primary key auto_increment,
  Detalle char(30) unique );
  
create table Categoria(
  id int primary key auto_increment,
  Detalle char(30) unique );

create table FormaPago(
  id int primary key auto_increment,
  Detalle char(30) unique );

create table Cliente (
  id int primary key auto_increment,
  Nombres char(30) not null,
  Correo char(30) unique,
  Passwordd char(20) not null );

CREATE TABLE CodigoVerificacion (
  id INT PRIMARY KEY AUTO_INCREMENT,       
  idCliente INT NOT NULL,
  Codigo CHAR(4) NOT NULL,
  FechaCaducidad DATETIME NOT NULL,  
  FOREIGN KEY (idCliente) REFERENCES Cliente(id)
);

create table Producto ( 
  id int primary key auto_increment,
  idCategoria int references Categoria(id),
  Detalle char(30) not null,
  Precio decimal(6,2) not null,
  Descripcion text );

create table ProductoFavorito ( 
  idCliente int references Cliente(id),
  idProducto int references producto(id) );

create table Cafe ( 
  id int primary key auto_increment,
  idDistrito int references Distrito(id),
  Horario char(30) not null,
  Direccion char(100) not null,
  Latitud char(20) not null,
  Longitud char(20) not null,
  GoogleMap text );
  
create table Pedido ( 
  id int primary key auto_increment,
  idCafe int references Cafe(id),
  idCliente int references Cliente(id),
  idFormaPago int references FormaPago(id),
  Estado char(1) not null,					-- S - Solicitado , P - Preparación, L - Listo
  FechaVenta datetime,
  FechaEntrega datetime,
  Total decimal(6,2),
  Descuento decimal(6,2) ) ;

create table PedidoDetalle ( 
  id int primary key auto_increment,
  idPedido int references Pedido(id),
  idProducto int references Producto(id),
  Detalle char(100),
  Cantidad int not null,
  Precio decimal(6,2),
  SubTotal decimal(6,2) );
  

insert Distrito(Detalle) values ('Lima'),('Independencia'),('San Isidro'),('Miraflores');
insert Categoria(Detalle) values ('Hot drinks'),('Cold drinks'),('Sandwichs');

insert Producto values
	(null,1,'Caramel Macchiato',4.00,'Caramel Macchiato'),
    (null,1,'Vanilla Latte',3.00,'Vanilla Late'),
    (null,1,'Traditional Capuccino',5.00,'Traditional Capuccino'),
    (null,1,'White Chocolate Mocha',6.00,'White Chocolate Mocha');

insert Cafe values
	( null, 1, 'Abierto 10:00 am - 22:00pm', 'Jirón de la Unión 498, Lima 15001','-12.0469936','-77.0346338','https://www.google.com/maps/place/Starbucks/@-12.0469936,-77.0346338,17z/data=!3m1!4b1!4m6!3m5!1s0x9105c8b60d3db227:0xda3ef878f70a8230!8m2!3d-12.0469989!4d-77.0320589!16s%2Fg%2F11gzzh2z1?entry=ttu&g_ep=EgoyMDI1MTEwNC4xIKXMDSoASAFQAw%3D%3D' ),
    ( null, 2, 'Abierto 10:00 am - 22:00pm', 'C.C. Mega Plaza, Av. Alfredo Mendiola 3698, Independencia 15311','-11.9906997','77.0633648','https://www.google.com/maps/place/Starbucks/@-12.0469936,-77.0346338,17z/data=!3m1!4b1!4m6!3m5!1s0x9105c8b60d3db227:0xda3ef878f70a8230!8m2!3d-12.0469989!4d-77.0320589!16s%2Fg%2F11gzzh2z1?entry=ttu&g_ep=EgoyMDI1MTEwNC4xIKXMDSoASAFQAw%3D%3D' ),
    ( null, 3, 'Abierto 10:00 am - 22:00pm', 'Av. Dos de Mayo 880, San Isidro 15073','-12.0963319','-77.0477833','https://www.google.com/maps/place/Starbucks+-+Dos+de+Mayo/@-12.0963319,-77.0477833,15z/data=!4m22!1m15!4m14!1m6!1m2!1s0x9105c8595f993f67:0x5d9dcecfd1e997b3!2sStarbucks+-+Dos+de+Mayo!2m2!1d-77.0404439!2d-12.0914463!1m6!1m2!1s0x9105c8595f993f67:0x5d9dcecfd1e997b3!2sAv.+Dos+de+Mayo+880,+San+Isidro+15073!2m2!1d-77.0404439!2d-12.0914463!3m5!1s0x9105c8595f993f67:0x5d9dcecfd1e997b3!8m2!3d-12.0914463!4d-77.0404439!16s%2Fg%2F1pty1tpq6?entry=ttu&g_ep=EgoyMDI1MTEwNC4xIKXMDSoASAFQAw%3D%3D' ),
    ( null, 4, 'Abierto 10:00 am - 22:00pm', 'Av. José Larco 632, Miraflores 15074','-12.11673','-77.0339569','https://www.google.com/maps/place/Starbucks/@-12.11673,-77.0339569,16z/data=!4m22!1m15!4m14!1m6!1m2!1s0x9105c8193e556995:0x8f9753de25c7d79d!2sStarbucks!2m2!1d-77.029382!2d-12.1232982!1m6!1m2!1s0x9105c8193e556995:0x8f9753de25c7d79d!2sAv.+Jos%C3%A9+Larco+632,+Miraflores+15074!2m2!1d-77.029382!2d-12.1232982!3m5!1s0x9105c8193e556995:0x8f9753de25c7d79d!8m2!3d-12.1232982!4d-77.029382!16s%2Fg%2F11cm03cjfs?entry=ttu&g_ep=EgoyMDI1MTEwNC4xIKXMDSoASAFQAw%3D%3D' );

create view view_getCafes as select * from Cafe order by id;

create procedure sp_getCliente(in _correo char(30), in _passwordd char(20))
	select * from Cliente where Correo = _correo and Passwordd = _passwordd;

create procedure sp_getCafes()
	select * from Cafe order by id;

create procedure sp_getCodigoVerificacion( in _correo char(30) )
	select * from CodigoVerificacion where Correo = _Correo order by FechaCaducidad desc limit 1;

delimiter //
create procedure sp_setCliente(in _id int, in _nombres char(30), in _correo char(30), in _passwordd char(20) )
	if ( _id = 0 ) then
		begin
            declare _count int;
			select count(*) into _count from Cliente where Correo = _correo;
			if ( _count = 0 ) then
				insert Cliente values ( null, _nombres, _correo, _passwordd );
                select last_insert_id() as insertID;
			  else select "Correo ya está registrado" as 'error';
			end if;
        end;
	  else 
		begin
			update Cliente set Nombres = _nombres, Correo = _correo, Passwordd = _passwordd where id = _id;
			if ( row_count() = 0 ) then
				select "Cliente no esta registrado" as 'error';
            end if;
		end;
    end if;
//

create procedure sp_setCodigoVerificacion( in _correo char(30), in _codigo char(4), in fechaCaducidad date )
	insert CodigoVerificacion values ( _correo, _codigo, _fechaCaducidad );

delimiter //
create procedure sp_getClienteCodigo(in _correo char(30))
	begin
		declare _count int;
		select count(*) into _count from Cliente where Correo = _correo;
		if ( _count = 0 ) then
			select "Correo no está registrado" as 'error';
		  else 
			begin
                declare _id int;
                declare _codigo int;
                declare _fechaAdd time;
                
                set _fechaAdd = date_add( now(), interval 5 minute );
				set _codigo = floor( rand() * (9999 - 1000 + 1) + 1000 );
                
                set _id = (select id from Cliente where Correo = _correo);
				insert CodigoVerificacion values ( _id, _codigo, _fechaAdd );
				select _codigo as codigo;
            end;
		end if;
	end;
//

-- call sp_setCliente("0","omar","oaemdl@gmail.com","1234")
-- call sp_getCliente("oaemdl@gmail.com","1234")
-- call sp_getClienteCodigo("oaemdl@gmail.com")

select * from CodigoVerificacion