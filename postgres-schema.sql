create table users (
	user_id serial4 not null primary key,
	email text not null,
	first_name text not null,
	last_name text not null,
	hash text not null,

	created_by integer null,
	created_at timestamp with time zone not null default now(),
	updated_by integer null,
	updated_at timestamp with time zone not null default now(),
	deleted_by integer null,
	deleted_at timestamp with time zone null
);

alter table users 
	add constraint users_created_by_fk
		foreign key (created_by) references users (user_id);

alter table users 
	add constraint users_updated_by_fk
		foreign key (updated_by) references users (user_id);

alter table users 
	add constraint users_deleted_by_fk
		foreign key (deleted_by) references users (user_id);

create table roles (
	role_id serial4 not null primary key,
	name text not null,

	created_by integer null,
	created_at timestamp with time zone not null default now(),
	updated_by integer null,
	updated_at timestamp with time zone not null default now(),
	deleted_by integer null,
	deleted_at timestamp with time zone null,
	
	constraint roles_created_by_fk
		foreign key (created_by) references users (user_id),
	constraint roles_updated_by_fk
		foreign key (updated_by) references users (user_id),
	constraint roles_deleted_by_fk
		foreign key (deleted_by) references users (user_id)
);

create table user_roles (
	user_role_id serial4 not null primary key,
	role_id serial4 not null,
	user_id serial4 not null,

	created_by integer null,
	created_at timestamp with time zone not null default now(),
	updated_by integer null,
	updated_at timestamp with time zone not null default now(),
	deleted_by integer null,
	deleted_at timestamp with time zone null,
	
	constraint roles_user_roles_fk 
		foreign key (role_id) references roles (role_id),
	constraint users_user_roles_fk 
		foreign key (user_id) references users (user_id),
	constraint user_roles_created_by_fk
		foreign key (created_by) references users (user_id),
	constraint user_roles_updated_by_fk
		foreign key (updated_by) references users (user_id),
	constraint user_roles_deleted_by_fk
		foreign key (deleted_by) references users (user_id)
);

create table user_codes (
	user_code_id serial4 not null primary key,
	user_id serial4 not null,
	code text not null,

	created_by integer null,
	created_at timestamp with time zone not null default now(),
	updated_by integer null,
	updated_at timestamp with time zone not null default now(),
	deleted_by integer null,
	deleted_at timestamp with time zone null,
	
	constraint users_user_codes_fk 
		foreign key (user_id) references users (user_id),
	constraint user_codes_created_by_fk
		foreign key (created_by) references users (user_id),
	constraint user_codes_updated_by_fk
		foreign key (updated_by) references users (user_id),
	constraint user_codes_deleted_by_fk
		foreign key (deleted_by) references users (user_id)
);

create table categories (
	category_id serial4 not null primary key,
	name text not null,

	created_by integer null,
	created_at timestamp with time zone not null default now(),
	updated_by integer null,
	updated_at timestamp with time zone not null default now(),
	deleted_by integer null,
	deleted_at timestamp with time zone null,
	
	constraint user_codes_created_by_fk
		foreign key (created_by) references users (user_id),
	constraint user_codes_updated_by_fk
		foreign key (updated_by) references users (user_id),
	constraint user_codes_deleted_by_fk
		foreign key (deleted_by) references users (user_id)
);

create table products (
	product_id serial4 not null primary key,
	name text not null,
	price decimal not null,
	is_active boolean null,
	category_id integer null,

	created_by integer null,
	created_at timestamp with time zone not null default now(),
	updated_by integer null,
	updated_at timestamp with time zone not null default now(),
	deleted_by integer null,
	deleted_at timestamp with time zone null,
	
	constraint categories_products_fk
		foreign key (category_id) references categories (category_id),
	constraint user_codes_created_by_fk
		foreign key (created_by) references users (user_id),
	constraint user_codes_updated_by_fk
		foreign key (updated_by) references users (user_id),
	constraint user_codes_deleted_by_fk
		foreign key (deleted_by) references users (user_id)
);

create table customers (
	customer_id serial4 not null primary key,
	name text not null,
	internal_id text null,
	address text null,
	city text null,
	phone text null,
	
	created_by integer null,
	created_at timestamp with time zone not null default now(),
	updated_by integer null,
	updated_at timestamp with time zone not null default now(),
	deleted_by integer null,
	deleted_at timestamp with time zone null,
	
	constraint user_codes_created_by_fk
		foreign key (created_by) references users (user_id),
	constraint user_codes_updated_by_fk
		foreign key (updated_by) references users (user_id),
	constraint user_codes_deleted_by_fk
		foreign key (deleted_by) references users (user_id)
);
