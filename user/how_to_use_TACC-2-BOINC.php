<?php
//Added by Thomas
require_once("../inc/util.inc");

//Edited by Joshua
page_head(null, null, null, null,  null, "The User-Guide of BOINC@TACC");
echo "<br /><font size=+3>".tra("How Can TACC/XSEDE Researchers Use BOINC@TACC?")."</font>";
echo '<p>'.tra("To submit jobs as a researcher, you could either use the job submission interface available on this website, or you could submit the jobs after logging in to the Stampede2/Lonestar5 systems at TACC.").'</p>';

echo "<h3>".tra("Directions to Submit Jobs Through the Website")."</h3>";
echo '<p>'.tra("For submitting jobs through this website, you should first run the registration script from the Stampede2/Lonestar5 systems at least once. Click ").'<a href="https://github.com/ritua2/TACC-2-BOINC/blob/master/stampede2-backend/register-boinc.sh">'.tra("this link").'</a>'.tra(" and copy the registration script, paste the script in a file on Stampede2 or Lonestar5, change the permission on the file (chmod +x filename.sh), and run the script (./filename.sh). After this:").'</p>';
echo '<ol>
        <li>'.tra("Log in as a Researcher using your TACC portal credentials.").'</li>
        <li>'.tra("Go to the Job Submission page.").'</li>
        <li>'.tra('Choose the location of the docker image. If the docker image is provided by BOINC@TACC, keep the radio-button for the "List of BOINC@TACC docker images" selected. If the docker image is on Docker Hub and not supported by BOINC@TACC, click the radio button for Docker Hub.').'</li>
        <li>'.tra("(Only for docker images supported by BOINC@TACC) Select the docker image needed to run the job from the drop-down below 'List of BOINC@TACC docker images' and select the desired docker image.").'</li>
        <li>'.tra('(Only for non-BOINC@TACC docker images) Type in the name of the desired docker image as it appears on Docker Hub (not the URL). Then select the "Check if it exists on docker hub" button and the BOINC@TACC system will check if the docker image exists or not.').'</li>
        <li>'.tra("Type in the list of commands necessary to run the file. Hit enter after each command.").'</li>
        <li>'.tra('Select whether the input files will be uploaded as a TAR file or as a ZIP file. Then browse to the desired TAR or ZIP file on your local machine using the "Browse" button. Then select the file, and click the "Submit the Job" button.').'</li>
        <li>'.tra("Congrats, your job is submitted!").'</li>
    </ol>';


echo "<h3>".tra("Directions to Submit Jobs Directly Through Stampede2/Lonestar5")."</h3>";
echo '<p>'.tra("For submitting jobs directly from Stampede2/Lonestar5 systems, please run the BOINC@TACC job submission script available ").'<a href="https://github.com/ritua2/TACC-2-BOINC/blob/master/stampede2-backend/stampede_2_BOINC2.sh">'.tra("here.").'</a>';

echo '<p><span style="font-weight: bold;">'.tra("Please note:").'</span>'.tra(" you will not be able to login to Stampede2/Lonestar5 if you do not already have an existing project allocation on TACC resources. Please visit the following visit to learn more about the process of requesting allocation on TACC resources: ").'<a href="https://portal.tacc.utexas.edu/">https://portal.tacc.utexas.edu/</a>';

echo '<p><h3>'.tra('Video demonstration of the BOINC@TACC infrastructure:').'</h3></p>';
//iframe code from https://www.w3schools.com/html/tryit.asp?filename=tryhtml_youtubeiframe
echo '<iframe width="560" height="315" src="https://www.youtube.com/embed/UH9mJjZstO4" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>';

echo "<h3>".tra("Step-by-Step Instructions for Running the OpenSees Application from the Job Submission Page.")."</h3>";

echo "<ol>
<li>".tra("Get the sample input files from the following paths:")."<p></p>
curl http://opensees.berkeley.edu/wiki/images/a/a1/ElasticFrame.tcl<p></p>
curl http://opensees.berkeley.edu/wiki/images/3/3d/MomentCurvature.tcl</li>
<br>
<li> ".tra("Create a directory named")." \"data\" ".tra("and copy the files inside this directory, and create a *.zip or a *.tar file for this data directory")."<p></p>
cp ElasticFrame.tcl /data/ElFram.tcl<p></p>
cp MomentCurvature.tcl /data/MomCurv.tcl </li>
<br>
<li>".tra("Select OpenSees from the drop-down list")."</li>
<br>
<li> ".tra("Enter the commands to run OpenSees in the text-box available through the web-interface")."<p></p>
OpenSees < ./data/MomCurv.tcl<p></p>
OpenSees < ./data/ElFram.tcl</li>
<br>
<li> ".tra("Upload the data.zip or data.tar file created in step # 2")."</li>
<br>
<li>".tra("Click on job-submit button.")."</li></ol>";
//End of Joshua's edit
page_tail();
//End of the edit by Thomas
?>
