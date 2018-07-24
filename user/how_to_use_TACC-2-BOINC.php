<?php
require_once("../inc/util.inc");

page_head(null, null, null, null,  null, "The \"How\" of TACC-2-BOINC");

echo "<font size=+3>".tra("How to Use TACC-2-BOINC?")."</font>";
echo "<br>";
echo tra("To submit jobs as a researcher, you could either use the job
submission interface available on this website, or you could submit
the jobs after logging in to the Stampede2/Lonestar5 systems at TACC.
For submitting, jobs through this website, you should first run the
<a href=\"https://github.com/ritua2/TACC-2-BOINC/blob/master/stampede2-backend/register-boinc.sh\">verification script</a> from the Stampede2/Lonestar5 systems at least once.
For submitting jobs directly from Stampede2/Lonestar5 systems, please
run the TACC-2-BOINC <a href=\"https://github.com/ritua2/TACC-2-BOINC/blob/master/user/job_submission.php\">TACC-2-BOINC job submission script</a>. You will not be able to
login to Stampede2/Lonestar5 if you do not already have an existing
project allocation on TACC resources. Please visit the following visit
to learn more about the process of requesting access to TACC resources:
<a href=\"https://portal.tacc.utexas.edu/\">https://portal.tacc.utexas.edu/</a>")
page_tail();
?>
