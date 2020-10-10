#!/usr/bin/env python3

"""
BASICS

Updates statistics for users, hosts, teams
"""


import gzip
import mysql.connector as mysql_con
import os
import time
import hashlib




# Escapes XML characters: <, >
# Transforms
# Returns the escaped string
def escape_xml(s1):
    return s1.replace("<", "  &lt;").replace(">", "&gt;")




# --------------------
# tables.xml
# --------------------

boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
cursor = boinc_db.cursor(buffered=True)
cursor.execute("SELECT (SELECT COUNT(*) FROM user), (SELECT COUNT(*) FROM team), (SELECT COUNT(*)FROM host), (SELECT SUM(total_credit) FROM user)")

[user_count, team_count, host_count, credit_count] = cursor.next()


tables_xml = """<tables>
    <update_time>{update_time:d}</update_time>
    <nusers_total>{nusers_total:d}</nusers_total>
    <nteams_total>{nteams_total:d}</nteams_total>
    <nhosts_total>{nhosts_total:d}</nhosts_total>
    <total_credit>{total_credit:.4f}</total_credit>
    <applications>
        <application>
            <name>autodock-vina_boinc2docker</name>
        </application>
        <application>
            <name>bedtools_boinc2docker</name>
        </application>
        <application>
            <name>blast_boinc2docker</name>
        </application>
        <application>
            <name>bowtie_boinc2docker</name>
        </application>
        <application>
            <name>gromacs_boinc2docker</name>
        </application>
        <application>
            <name>htseq_boinc2docker</name>
        </application>
        <application>
            <name>mpi-lammps_boinc2docker</name>
        </application>
        <application>
            <name>namd_boinc2docker</name>
        </application>
        <application>
            <name>openfoam6_boinc2docker</name>
        </application>
        <application>
            <name>opensees_boinc2docker</name>
        </application>
    </applications>
    <badges> </badges>
</tables>"""

with open("/home/boincadm/project/html/user/stats/tables.xml", "w") as tables_xml_file:
    tables_xml_file.write(tables_xml.format(update_time=int(time.time()), nusers_total=user_count,
                                            nteams_total=team_count, nhosts_total=host_count, total_credit=credit_count))


cursor.close()
boinc_db.close()


# --------------------
# Gathers information about only those users who agreed to have their statistics collected
# --------------------

# userid_agrees_to_export_stats = {userid:True (bool)}
userid_agrees_to_export_stats ={}

boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
cursor = boinc_db.cursor(buffered=True)
cursor.execute("SELECT userid FROM latest_consent WHERE consent_type_id=2 AND consent_flag=1")

for row in cursor:
    userid_agrees_to_export_stats[row[0]] = True 

cursor.close()
boinc_db.close()



# screen_name_to_random_name = {screen_name (str): random_name (str)}
screen_name_to_random_name = {}

boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
cursor = boinc_db.cursor(buffered=True)
cursor.execute("SELECT email_id, random_name FROM screen_name_anonymization")

for row in cursor:
    screen_name_to_random_name[row[0]] = escape_xml(row[1])

cursor.close()
boinc_db.close()



# userdata_by_userid = { userid (int):{username (str), teamid (int), random_name (str), country (str), create_time (int), total_credit (float),
#                 expavg_credit (float), expavg_time (float), cpid (str)} ...
# }
userdata_by_userid = {}

# username_to_userid = { username (str): userid (str), ...}
username_to_userid = {}

ordered_userids = []

boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
cursor = boinc_db.cursor(buffered=True)
cursor.execute("SELECT id, name, country, create_time, total_credit, expavg_credit, expavg_time, cross_project_id, teamid, email_addr FROM user")

for row in cursor:
    [userid, screen_name, country, create_time, total_credit, expavg_credit, expavg_time, cpid, teamid, email_addr] = row

    random_name = screen_name_to_random_name[email_addr]
    m = hashlib.md5()
    cpidemail=cpid+email_addr
    m.update(cpidemail.encode('utf-8'))
    enc_cpid=m.hexdigest()

    if userid not in userid_agrees_to_export_stats:
        userdata_by_userid[userid] = {"random_name":random_name, "exports":False}
        continue

    # random_name was already escaped as the value in screen_name_to_random_name
    userdata_by_userid[userid] = {"username":escape_xml(screen_name), "teamid":teamid, "random_name":random_name, "exports":True, "country":escape_xml(country), "create_time":create_time,
                                    "total_credit":total_credit, "expavg_credit":expavg_credit, "expavg_time":expavg_time, "cpid":enc_cpid, "teamid":teamid}
    ordered_userids.append(userid)


cursor.close()
boinc_db.close()

# Forces an ordered list of users
ordered_userids = sorted(ordered_userids)


with gzip.open("/home/boincadm/project/html/user/stats/user.gz", mode="wt", compresslevel=9, encoding="utf_8") as user_file:
    user_file.write("<?xml version=\"1.0\" encoding=\"utf_8\"?>\n")
    user_file.write("<users>\n")

    for a_userid in ordered_userids:

        this_user_data = userdata_by_userid[a_userid]
        name_shown = this_user_data["random_name"]
        country = this_user_data["country"]
        create_time = this_user_data["create_time"]
        total_credit = this_user_data["total_credit"]
        expavg_credit = this_user_data["expavg_credit"]
        expavg_time = this_user_data["expavg_time"]
        cpid = this_user_data["cpid"]
        teamid = this_user_data["teamid"]

        individual_volunteer_data = """<user>
 <id>{u_id:d}</id>
 <name>{u_name:s}</name>
 <country>{u_country:s}</country>
 <create_time>{u_create_time:d}</create_time>
 <total_credit>{u_total_credit:.4f}</total_credit>
 <expavg_credit>{u_expavg_credit:.4f}</expavg_credit>
 <expavg_time>{u_expavg_time:.4f}</expavg_time>
 <cpid>{u_cpid:s}</cpid>
 <teamid>{u_teamid:d}</teamid>
 <has_profile/>
</user>\n"""
        
        user_file.write(individual_volunteer_data.format(u_id=a_userid, u_name=name_shown, u_country=country, u_create_time=create_time,
                        u_total_credit=total_credit, u_expavg_credit=expavg_credit, u_expavg_time=expavg_time, u_cpid=cpid, u_teamid=teamid))

    user_file.write("</users>\n")


# --------------------
# Teams
# --------------------

ordered_teamids = []
teamdata_by_teamid = {}

boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
cursor = boinc_db.cursor(buffered=True)
cursor.execute("SELECT id, type, name, userid, total_credit, expavg_credit, expavg_time, create_time, description, country FROM team")

for row in cursor:
    [teamid, teamtype, name, userid, total_credit, expavg_credit, expavg_time, create_time, description, country] = row

    founder_name = userdata_by_userid[userid]["random_name"]
    teamdata_by_teamid[teamid] = {"id":teamid, "name":escape_xml(name), "type":teamtype, "userid":userid, "total_credit":total_credit, "founder_name":founder_name,
                                    "expavg_credit":expavg_credit, "expavg_time":expavg_time, "create_time":create_time, "description":escape_xml(description), "country":escape_xml(country)}
    ordered_teamids.append(teamid)


cursor.close()
boinc_db.close()



# Forces an ordered list of users
ordered_teamids = sorted(ordered_teamids)


with gzip.open("/home/boincadm/project/html/user/stats/team.gz", mode="wt", compresslevel=9, encoding="utf_8") as team_file:
    team_file.write("<?xml version=\"1.0\" encoding=\"utf_8\"?>\n")
    team_file.write("<teams>\n")

    for a_teamid in ordered_teamids:

        this_team_data = teamdata_by_teamid[a_teamid]
        teamtype = this_team_data["type"]
        name = this_team_data["name"]
        userid = this_team_data["userid"]
        total_credit = this_team_data["total_credit"]
        expavg_credit = this_team_data["expavg_credit"]
        expavg_time = this_team_data["expavg_time"]
        founder_name = this_team_data["founder_name"]
        create_time = this_team_data["create_time"]
        description = this_team_data["description"]
        country = this_team_data["country"]

        
        team_data = """<team>
 <id>{t_id:d}</id>
 <type>{t_type:d}</type>
 <name>{t_name:s}</name>
 <userid>{t_userid:d}</userid>
 <total_credit>{t_total_credit:.4f}</total_credit>
 <expavg_credit>{t_expavg_credit:.4f}</expavg_credit>
 <expavg_time>{t_expavg_time:.4f}</expavg_time>
 <founder_name>{t_founder_name:s}</founder_name>
 <create_time>{t_create_time:d}</create_time>
 <description>{t_description:s}</description>
 <country>{t_country:s}</country>
</team>\n"""

        team_file.write(team_data.format(t_id=a_teamid, t_type=teamtype, t_name=name, t_userid=userid,
                                        t_total_credit=total_credit, t_expavg_credit=expavg_credit,
                                        t_expavg_time=expavg_time, t_founder_name=founder_name,
                                        t_create_time=create_time, t_description=description, t_country=country))

    team_file.write("</teams>\n")



# --------------------
# Hosts
# --------------------

ordered_hostids = []
hostdata_by_hostid = {}
userid_agrees_to_export_hosts_stats ={}

boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
cursor = boinc_db.cursor(buffered=True)
cursor.execute("select id from user where show_hosts=1")

for row in cursor:
    userid_agrees_to_export_hosts_stats[row[0]] = True 

cursor.close()
boinc_db.close()

boinc_db = mysql_con.connect(host = os.environ['URL_BASE'].split('/')[-1], port = 3306, user = os.environ["MYSQL_USER"], password = os.environ["MYSQL_UPASS"], database = 'boincserver')
cursor = boinc_db.cursor(buffered=True)
cursor.execute("""SELECT id, userid, total_credit, expavg_credit, expavg_time, p_vendor, p_model, os_name, os_version,
                    create_time, rpc_time, timezone, p_ncpus, p_fpops, p_iops,
                    p_membw, m_nbytes, m_cache, m_swap, d_total, d_free, n_bwup, n_bwdown, avg_turnaround, credit_per_cpu_sec, host_cpid
                    FROM host""")

for row in cursor:
    [hostid, userid, total_credit, expavg_credit, expavg_time, p_vendor, p_model, os_name, os_version,
        create_time, rpc_time, timezone, ncpus, p_fpops, p_iops,
        p_membw, m_nbytes, m_cache, m_swap, d_total, d_free, n_bwup, n_bwdown, avg_turnaround, credit_per_cpu_sec, host_cpid] = row

    if userid not in userid_agrees_to_export_stats:
        continue
    if userid not in userid_agrees_to_export_hosts_stats:
        continue

    hostdata_by_hostid[hostid] = {"id":hostid, "userid":userid, "total_credit":total_credit, "expavg_credit":expavg_credit,
                                "expavg_time":expavg_time, "p_vendor":escape_xml(p_vendor), "p_model":escape_xml(p_model),
                                "os_name":escape_xml(os_name), "os_version":escape_xml(os_version), "create_time":create_time,
                                "rpc_time":rpc_time, "timezone":timezone, "ncpus":ncpus, "p_fpops":p_fpops,
                                "p_iops":p_iops, "p_membw":p_membw, "m_nbytes":m_nbytes, "m_cache":m_cache,
                                "m_swap":m_swap, "d_total":d_total, "d_free":d_free, "n_bwup":n_bwup,
                                "n_bwdown":n_bwdown, "avg_turnaround":avg_turnaround, "credit_per_cpu_sec":credit_per_cpu_sec,
                                "host_cpid":host_cpid}
    ordered_hostids.append(hostid)


cursor.close()
boinc_db.close()


# Forces an ordered list of users
ordered_hostids = sorted(ordered_hostids)


with gzip.open("/home/boincadm/project/html/user/stats/host.gz", mode="wt", compresslevel=9, encoding="utf_8") as host_file:
    host_file.write("<?xml version=\"1.0\" encoding=\"utf_8\"?>\n")
    host_file.write("<hosts>\n")

    for a_hostid in ordered_hostids:

        this_user_data = hostdata_by_hostid[a_hostid]
        userid = this_user_data["userid"]
        total_credit = this_user_data["total_credit"]
        expavg_credit = this_user_data["expavg_credit"]
        expavg_time = this_user_data["expavg_time"]
        p_vendor = this_user_data["p_vendor"]
        p_model = this_user_data["p_model"]
        os_name = this_user_data["os_name"]
        os_version = this_user_data["os_version"]
        create_time = this_user_data["create_time"]
        rpc_time = this_user_data["rpc_time"]
        timezone = this_user_data["timezone"]
        ncpus = this_user_data["ncpus"]
        p_fpops = this_user_data["p_fpops"]
        p_iops = this_user_data["p_iops"]
        p_membw = this_user_data["p_membw"]
        m_nbytes = this_user_data["m_nbytes"]
        m_cache = this_user_data["m_cache"]
        m_swap = this_user_data["m_swap"]
        d_total = this_user_data["d_total"]
        d_free = this_user_data["d_free"]
        n_bwup = this_user_data["n_bwup"]
        n_bwdown = this_user_data["n_bwdown"]
        avg_turnaround = this_user_data["avg_turnaround"]
        credit_per_cpu_sec = this_user_data["credit_per_cpu_sec"]
        host_cpid = this_user_data["host_cpid"]
        
        team_data = """<host>
  <id>{h_id:d}</id>
  <userid>{h_userid:d}</userid>
  <total_credit>{h_total_credit:.4f}</total_credit>
  <expavg_credit>{h_expavg_credit:.4f}</expavg_credit>
  <expavg_time>{h_expavg_time:.4f}</expavg_time>
  <p_vendor>{h_p_vendor:s}</p_vendor>
  <p_model>{h_p_model:s}</p_model>
  <os_name>{h_os_name:s}</os_name>
  <os_version>{h_os_version:s}</os_version>
  <create_time>{h_create_time:d}</create_time>
  <rpc_time>{h_rpc_time:d}</rpc_time>
  <timezone>{h_timezone:d}</timezone>
  <ncpus>{h_ncpus:d}</ncpus>
  <p_fpops>{h_p_fpops:.4f}</p_fpops>
  <p_iops>{h_p_iops:.4f}</p_iops>
  <p_membw>{h_p_membw:.4f}</p_membw>
  <m_nbytes>{h_m_nbytes:.4f}</m_nbytes>
  <m_cache>{h_m_cache:.4f}</m_cache>
  <m_swap>{h_m_swap:.4f}</m_swap>
  <d_total>{h_d_total:.4f}</d_total>
  <d_free>{h_d_free:.4f}</d_free>
  <n_bwup>{h_n_bwup:.4f}</n_bwup>
  <n_bwdown>{h_n_bwdown:.4f}</n_bwdown>
  <avg_turnaround>{h_avg_turnaround:.4f}</avg_turnaround>
  <credit_per_cpu_sec>{h_credit_per_cpu_sec:.4f}</credit_per_cpu_sec>
  <host_cpid>{h_host_cpid:s}</host_cpid>
</host>\n"""
        
        host_file.write(team_data.format(h_id=a_hostid, h_userid=userid, h_total_credit=total_credit, h_expavg_credit=expavg_credit,
                                        h_expavg_time=expavg_time, h_p_vendor=p_vendor, h_p_model=p_model, h_os_name=os_name,
                                        h_os_version=os_version, h_create_time=create_time, h_rpc_time=rpc_time, h_timezone=timezone,
                                        h_ncpus=ncpus, h_p_fpops=p_fpops, h_p_iops=p_iops, h_p_membw=p_membw,
                                        h_m_nbytes=m_nbytes, h_m_cache=m_cache, h_m_swap=m_swap, h_d_total=d_total,
                                        h_d_free=d_free, h_n_bwup=n_bwup, h_n_bwdown=n_bwdown, h_avg_turnaround=avg_turnaround,
                                        h_credit_per_cpu_sec=credit_per_cpu_sec, h_host_cpid=host_cpid))

    host_file.write("</hosts>\n")
