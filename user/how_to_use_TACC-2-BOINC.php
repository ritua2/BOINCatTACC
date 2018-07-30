<?php
//Added by Thomas
require_once("../inc/util.inc");

//Edited by Joshua
page_head(null, null, null, null,  null, "The \"How-to\" of TACC-2-BOINC");
echo "<br /><font size=+3>".tra("How to Use TACC-2-BOINC?")."</font>";
echo '<p>'.tra("To submit jobs as a researcher, you could either use the job submission interface available on this website, or you could submit the jobs after logging in to the Stampede2/Lonestar5 systems at TACC.").'</p>';


echo "<h3>".tra("Directions to Submit Jobs Through the Website")."</h3>";
echo '<p>'.tra("For submitting jobs through this website, you should first run the registration script from the Stampede2/Lonestar5 systems at least once. Click ").'<a href="https://github.com/ritua2/TACC-2-BOINC/blob/master/stampede2-backend/register-boinc.sh">'.tra("this link").'</a>'.tra(" and copy the registration script, paste the script in a file on Stampede2 or Lonestar5, change the permission on the file (chmod +x filename.sh), and run the script (./filename.sh). After this:").'</p>';
echo '<ol>
        <li>'.tra("Log in as a Researcher using your TACC portal credentials.").'</li>
        <li>'.tra("Go to the Job Submission page.").'</li>
        <li>'.tra('Choose the location of the docker image. If the docker image is provided by TACC-2-BOINC, keep the radio-button for the "List of TACC-2-BOINC docker images" selected. If the docker image is on Docker Hub and not supported by TACC-2-BOINC, click the radio button for Docker Hub.').'</li>
        <li>'.tra("(Only for docker images supported by TACC-2-BOINC) Select the docker image needed to run the job from the drop-down below 'List of TACC-2-BOINC docker images' and select the desired docker image.").'</li>
        <li>'.tra('(Only for non-TACC-2-BOINC docker images) Type in the name of the desired docker image as it appears on Docker Hub (not the URL). Then select the "Check if it exists on docker hub" button and the TACC-2-BOINC system will check if the docker image exists or not.').'</li>
        <li>'.tra("Type in the list of commands necessary to run the file. Hit enter after each command.").'</li>
        <li>'.tra('Select whether the input files will be uploaded as a TAR file or as a ZIP file. Then browse to the desired TAR or ZIP file on your local machine using the "Browse" button. Then select the file, and click the "Submit the Job" button.').'</li>
        <li>'.tra("Congrats, your job is submitted!").'</li>
    </ol>';


echo "<h3>".tra("Directions to Submit Jobs Directly Through Stampede2/Lonestar5")."</h3>";
echo '<p>'.tra("For submitting jobs directly from Stampede2/Lonestar5 systems, please run the TACC-2-BOINC job submission script available ").'<a href="https://github.com/ritua2/TACC-2-BOINC/blob/master/stampede2-backend/stampede_2_BOINC2.sh">'.tra("here.").'</a>';

echo '<p><span style="font-weight: bold">'.tra("Please note:").'</span>'.tra(" you will not be able to login to Stampede2/Lonestar5 if you do not already have an existing project allocation on TACC resources. Please visit the following visit to learn more about the process of requesting allocation on TACC resources: ").'<a href="https://portal.tacc.utexas.edu/">https://portal.tacc.utexas.edu/</a>';
//End of Joshua's edit
page_tail();
//End of the edit by Thomas
?>
