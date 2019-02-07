CREATE TABLE boincserver.screen_name_anonymization (
	name VARCHAR(254) NOT NULL,
	random_name VARCHAR(254) NOT NULL
);

ALTER TABLE screen_name_anonymization ADD COLUMN (email_id VARCHAR (254));
CREATE TRIGGER update_email AFTER INSERT ON user FOR EACH ROW UPDATE screen_name_anonymization SET email_id= (select email_addr from user where user.name = screen_name_anonymization.name) where email_id is NULL;
ALTER TABLE screen_name_anonymization ADD CONSTRAINT fk_email FOREIGN KEY (email_id) REFERENCES user (email_addr) ON DELETE CASCADE ON UPDATE CASCADE;
