"""
BASICS

Creates the necessary MySQL tables
"""



import mysql.connector as mysql_con
import os




boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
cursor = boinc_db.cursor(buffered=True)

# Creates VolCon jobs table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS volcon_jobs (
    job_id               BIGINT AUTO_INCREMENT UNIQUE,
    client_ip            VARCHAR(255),
    Command              VARCHAR(5000),
    Command_Errors       VARCHAR(20000),
    computation_time     DOUBLE,
    Date_Sub             DATETIME,
    Date_Run             DATETIME,
    download_time        DOUBLE,
    Error                VARCHAR(255),
    GPU                  bool,
    Image                VARCHAR(255),
    mirror_ip            VARCHAR(255),
    Notified             VARCHAR(255),
    origin               VARCHAR(255),
    public               bool,
    priority             VARCHAR(255),
    received_time        DATETIME,
    results_path_apache  VARCHAR(255),
    results_path_reef    VARCHAR(255),
    status               VARCHAR(255),
    tags                 VARCHAR(255),
    Token                VARCHAR(255),
    username             VARCHAR(255),
    volcon_id            VARCHAR(255),

    PRIMARY KEY (job_id)
    )
    """)



# Creates user table
# Note: researcher_id is only used as a primary key and not used for anything internally
cursor.execute("""
    CREATE TABLE IF NOT EXISTS researcher_users (
    researcher_id         BIGINT AUTO_INCREMENT UNIQUE,
    token                 VARCHAR(255),
    email                 VARCHAR(255),
    username              VARCHAR(255), # username given by the user
    allocation            VARCHAR(255),
    organization          VARCHAR(255),

    PRIMARY KEY (researcher_id)
    )
    """)



# Creates orgs tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS organizations (
    org_id                BIGINT AUTO_INCREMENT UNIQUE,
    org_name              VARCHAR(255) UNIQUE,
    org_key               VARCHAR(255) UNIQUE,

    PRIMARY KEY (org_id)
    )
    """)



# Random name table
cursor.execute("""
    CREATE TABLE screen_name_anonymization (
        name                  VARCHAR(255) UNIQUE,
        random_name           VARCHAR(255) UNIQUE,
        original_random_name  VARCHAR(255) UNIQUE,
        export_stats          VARCHAR(255),
        email_id              VARCHAR(254) UNIQUE
    )
    """)



# Signup table for email verification
cursor.execute("""
    CREATE TABLE email_verification (
        email_addr            VARCHAR(254) UNIQUE,
        name                  VARCHAR(254) UNIQUE,
        passwd_hash           VARCHAR(254),
        country               VARCHAR(254),
        postal_code           VARCHAR(254),
        project_prefs         BLOB,
        teamid               INT(11),
        validation_key        VARCHAR(254),
        date_signup           DATETIME,
        date_verified         DATETIME
    )
    """)



# Boinc2docker jobs
cursor.execute("""
    CREATE TABLE boinc2docker_jobs (
        job_id               BIGINT AUTO_INCREMENT UNIQUE,
        username             VARCHAR(254),
        token                VARCHAR(254),
        tags                 VARCHAR(254),
        Image                VARCHAR(254),
        Command              VARCHAR(20000),
        date_processed       DATETIME,
        date_run             DATETIME,
        date_notified        DATETIME,
        boinc_application    VARCHAR(254),
        boinc_error          VARCHAR(254),
        origin               VARCHAR(254),
        status               VARCHAR(254),
        results_path_apache  VARCHAR(255),
        results_path_reef    VARCHAR(255),

        PRIMARY KEY (job_id)
    )
    """)



cursor.execute("""
    CREATE TRIGGER update_email AFTER INSERT ON user
    FOR EACH ROW UPDATE screen_name_anonymization
    SET email_id= (select email_addr from user where user.name = screen_name_anonymization.name) where email_id is NULL
""")

cursor.execute("""
    ALTER TABLE screen_name_anonymization ADD CONSTRAINT fk_email FOREIGN KEY (email_id) REFERENCES user (email_addr) ON DELETE CASCADE ON UPDATE CASCADE
""")

cursor.execute("""
    CREATE TRIGGER update_name AFTER UPDATE ON user FOR EACH ROW
    UPDATE screen_name_anonymization SET name= (select name from user
    where user.email_addr = screen_name_anonymization.email_id) where email_id is NULL;
""")

cursor.execute("""
    CREATE TRIGGER update_name2 AFTER UPDATE ON user FOR EACH ROW UPDATE screen_name_anonymization
    SET name= (select name from user where user.email_addr = screen_name_anonymization.email_id) where email_id is NULL;
""")

# Unique names
cursor.execute("ALTER TABLE user ADD UNIQUE (name)")
cursor.execute("ALTER TABLE screen_name_anonymization ADD UNIQUE (name)")


boinc_db.commit()
cursor.close()
boinc_db.close()
