USE cw_pricing;

DROP TABLE If exists cw_pricing.category;

CREATE TABLE category(
	id INT NOT NULL AUTO_INCREMENT,
	category varchar(255) NOT NULL,
	PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE If exists cw_pricing.product;

CREATE TABLE product(
	id INT NOT NULL AUTO_INCREMENT,
	product varchar(255) NOT NULL,
	category_id INT NOT NULL,
	url varchar(255),
	PRIMARY KEY (id),
	FOREIGN KEY (category_id) REFERENCES cw_pricing.category(id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE If exists cw_pricing.price;

CREATE TABLE price(
	id INT NOT NULL AUTO_INCREMENT,
	timeStamp date NOT NULL,
	price numeric(15,2) NOT NULL,
	FOREIGN KEY (id) REFERENCES cw_pricing.product(id),
	PRIMARY KEY (id, timeStamp)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
