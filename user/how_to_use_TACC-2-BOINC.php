<?php
require_once("../inc/util.inc");

page_head(null, null, null, null,  null, "The \"How\" of TACC-2-BOINC");

echo "<font size=+3>".tra("How to Use TACC-2-BOINC?")."</font>";
echo "<br><br>";
echo tra("<style=\"text-align: center;\"><p>For submitting, jobs through this website, you should 
        first run the verification script from the Stampede2/Lonestar5 systems at least once. Click 
        this link and copy the <a href=\"https://github.com/ritua2/TACC-2-BOINC/blob/master/stampede2-backend/register-boinc.sh\"> verification script</a>, paste the script in a file on Stampede2's or 
        Lonestar5's, change the permission on the file (chmod +x filename.sh), and run the script.</p>
    <ol><h4>Directions to Submit Jobs Through the Website</h4>
        <li>Log in as a Researcher using your TACC portal credentials.</li>
        <li>Go to the Job Submission page.</li>
        <li>Choose the location of the docker image. If the docker image is hosted on TACC-2-BOINC,
        keep the radio button for the \"List of TACC-2-BOINC docker images\" selected. If the docker image is on Docker Hub and not a pre-made
        docker image supported by TACC-2-BOINC, click radio button for \"Docker Hub.\"</li>
        <li><ul>
        <li>(Only for docker images supported by TACC-2-BOINC) Select the docker image needed to the run the job
        from the drop-down below 'List of TACC-2-BOINC docker images' and select the desired docker 
        image.</li>
        <li>(Only for non-TACC-2-BOINC docker images) Type in the name of the desired docker image
        as it appears on Docker Hub, not the URL. Then select the \"Check if it exists on docker hub\"
        button and the TACC-2-BOINC system will check if the docker image exists or not.</li>
        </ul></li>
        <li>Type in the list of commands necessary to run the file. Hit enter after each command.</li>
        <li>Select whether the input files will be TAR or ZIP. Then browse to the desired TAR or ZIP 
        file on your local machine using the \"Browse\" button. Then select the file, and click the 
        \"Submit the Job\" button.</li>
        <li>Congrats, your job is submitted.</li>
    </ol>

<p>Directions to Submit Jobs Directly Through Stampede2/Lonestar5</p>

    <ol>
        <li>For submitting jobs directly from Stampede2/Lonestar5 systems, please
        run the <a href=\"https://github.com/ritua2/TACC-2-BOINC/blob/master/user/job_submission.php\">TACC-2-BOINC job submission script</a>.</li>
    </ol>
<p>Please note: you will not be able to login to Stampede2/Lonestar5 if you do not already have 
an existing project allocation on TACC resources. Please visit the following visit to learn more 
about the process of requesting access to TACC resources:
<a href=\"https://portal.tacc.utexas.edu/\">https://portal.tacc.utexas.edu/</a>.</p></style>");
page_tail();
?>
