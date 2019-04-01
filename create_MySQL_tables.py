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
    job_id            BIGINT AUTO_INCREMENT UNIQUE,
    Command           VARCHAR(5000),
    Command_Errors    VARCHAR(5000),
    computation_time  DOUBLE,
    Date_Sub          DATETIME,
    Date_Run          DATETIME,
    download_time     DOUBLE,
    Error             VARCHAR(255),
    GPU               bool,
    Image             VARCHAR(255),
    mirror_ip         VARCHAR(255),
    Notified          VARCHAR(255),
    public              bool,
    priority          VARCHAR(255),
    received_time     DATETIME,
    status            VARCHAR(255),
    Token             VARCHAR(255),
    volcon_id         VARCHAR(255),

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

    PRIMARY KEY (researcher_id)
    )
    """)



# Creates orgs tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS organizations (
    researcher_id         BIGINT AUTO_INCREMENT UNIQUE,
    token                 VARCHAR(255),
    email                 VARCHAR(255),
    username              VARCHAR(255), # username given by the user
    allocation            VARCHAR(255),

    PRIMARY KEY (researcher_id)
    )
    """)


boinc_db.commit()
cursor.close()
boinc_db.close()
