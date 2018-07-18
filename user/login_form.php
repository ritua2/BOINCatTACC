<?php
// This file is part of BOINC.
// http://boinc.berkeley.edu
// Copyright (C) 2008 University of California
//
// BOINC is free software; you can redistribute it and/or modify it
// under the terms of the GNU Lesser General Public License
// as published by the Free Software Foundation,
// either version 3 of the License, or (at your option) any later version.
//
// BOINC is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
// See the GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with BOINC.  If not, see <http://www.gnu.org/licenses/>.

require_once("../inc/db.inc");
require_once("../inc/util.inc");
require_once("../inc/account.inc");

check_get_args(array("next_url"));

$next_url = get_str('next_url', true);
$next_url = urldecode($next_url);
$next_url = sanitize_local_url($next_url);
$next_url = urlencode($next_url);

$u = "login_form.php?next_url=".$next_url;
redirect_to_secure_url($u);

$user = get_logged_in_user(false);
if ($user) {
    page_head("Already logged in");
    row2("You are logged in as $user->name",
        ".  <a href=\"logout.php?".url_tokens($user->authenticator)."\">Log out</a>"
    );
    page_tail();
    exit;
}

//Added by Gerald Joshua
page_head(null, null, null, null,  null, "Log In");

echo "
	<a data-toggle='tooltip'  style='margin-left: 36%;font-size: 24px;border-bottom:1px dotted #000;text-decoration: none;' title='Those interested in supporting R&D activities of researchers and scholars using TACC resources are invited to join the TACC-2-BOINC project as volunteers and the job for volunteers are to donate their spare compute-cycles to the TACC-2-BOINC projects.'>Log In as a Volunteer</a>";//End of edit by Gerald Joshua
echo "<br>";
if (0) {
echo '
    <a href="openid_login.php?openid_iden<a href=\"create_account_form.php?next_url=$next_url\">tifier=https://www.google.com/accounts/o8/id"><img src=img/google-button.png></a>
    <a href="openid_login.php?openid_identifier=http://yahoo.com"><img src=img/yahoo-button.png></a>
    <br>
';
}
echo "<br>";
login_form($next_url);

$config = get_config();
if (!parse_bool($config, "disable_account_creation")
    && !parse_bool($config, "no_web_account_creation")
) {
    echo"<!-- <center><h1>Or <a href=\"create_account_form.php?next_url=$next_url\">Create an Account</h1></a></center> --><br />
";
}
/*
//Added by Gerald Joshua, second Login button placement edited by Thomas Johnson
echo "<a data-toggle='tooltip'  style='margin-left: 35%;font-size: 24px;border-bottom:1px dotted #000;text-decoration: none;' title='All active users of TACC resources are eligible to run jobs through the TACC-2-BOINC infrastructure and qualify as researchers.'>Log In as a Researcher</a>
	<div style='margin-left: 35.45%;margin-top: 10px;'><a href='https://portal.tacc.utexas.edu/home?p_p_id=58&p_p_lifecycle=0&p_p_state=maximized&p_p_mode=view&saveLastPath=0&_58_struts_action=%2Flogin%2Flogin' class='btn btn-success'>Log In</a></div>";
//End of Gerald Joshua's edit
*/

echo "
    <script type=\"text/javascript\">
        document.f.email_addr.focus();
    </script>
";

page_tail();
?>
