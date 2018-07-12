<?php
/*
Thomas Hilton Johnson III
TACC-2-BOINC File Submission Webpage
7/6/2018
Allow for File Submission to TACC-2-BOINC Website
*/

require_once('../inc/boinc_db.inc');
require_once('../inc/util.inc');
require_once('../inc/account.inc');
require_once('../inc/countries.inc');
require_once('../inc/translation.inc');
require_once('../inc/recaptchalib.php');

page_head(
    null, null, null, null, boinc_recaptcha_get_head_extra(), tra("File Upload ")
);

echo '<font size=+3 style ="position:relative; left:36%;">'.tra("File Upload").'</font>';

page_tail();
?>
