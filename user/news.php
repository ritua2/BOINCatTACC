<?php
// This file is part of BOINC.
// http://boinc.berkeley.edu
// Copyright (C) 2016 University of California
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

//Added by Gerald Joshua by copying site_search.php

require_once("../inc/util.inc");

page_head(null, null, null, null, null, "News");

//Page Title
echo '<center><h1>News</h1></center><br />';

echo '<pre style="word-break:normal;white-space:normal;margin-left:20%;margin-right: 20%;"><style="text-align:left;"><p style="font-size:14px;font-weight: normal;"><span style="font-weight:bold;">'.tra('October 9th, 2020:').'</span>'.tra('Dear Volunteers and Researchers,<br><br>
                We are happy to announce that BOINC@TACC is back into production. There are still few action-items that are pending (such as the cross-project id related issue during export and downloading cross-project certificate) and we are working through them one by one. Also, we would like to urge you to remove and re-attach the project from BOINC manager since the keys have been changed.<br><br>Thanks for your patience and support!<br>
BOINC@TACC Team').' </p>';

echo '</style></pre></br>';


echo '<pre style="word-break:normal;white-space:normal;margin-left:20%;margin-right: 20%;"><style="text-align:left;"><p style="font-size:14px;font-weight: normal;"><span style="font-weight:bold;">'.tra('September 3rd, 2020:').'</span>'.tra('Project updates:
                We are still testing the settings on BOINC@TACC and it is not yet production ready. We will share an announcement once we are back to normal operations. We would encourage our users to wait before they create their accounts. Thanks!').' </p>';

echo '</style></pre></br>';


echo '<pre style="word-break:normal;white-space:normal;margin-left:20%;margin-right: 20%;"><style="text-align:left;"><p style="font-size:14px;font-weight: normal;"><span style="font-weight:bold;">'.tra('April 12th, 2020:').'</span>'.tra('Project updates:<ol>
        <li>Researchers will be submitting several million Autodock Vina jobs for SARS-COV2 drug screening using BOINC@TACC: <a href="https://www.utep.edu/newsfeed/campus/utep-school-of-pharmacy-developing-covid-19-vaccine,-drug-treatments-using-supercomputing.html">https://www.utep.edu/newsfeed/campus/utep-school-of-pharmacy-developing-covid-19-vaccine,-drug-treatments-using-supercomputing.html</a>.</li>
        <li>The information for joining the project is avilable at the following link: <a href="/join.php">https://boinc.tacc.utexas.edu/join.php</a></li>
        <li>Certain versions of Virtual Box (e.g., 6.1.4 and 6.1.2) are having compatibility issues with the BOINC client used for processing BOINC@TACC jobs on certain operating systems. We do not have a solution for this right now but will update the users as soon as we have further information. Right now, Virtual Box version 5 is guaranteed to work.</li>
        <li>We are working on exporting the BOINC statistics for the volunteers who choose to do so, and will post an update once we have finished this task.</li>
    </ol>').' </p>';

echo '</style></pre></br>';


echo '<pre style="word-break:normal;white-space:normal;margin-left:20%;margin-right: 20%;"><style="text-align:left;"><p style="font-size:14px;font-weight: normal;"><span style="font-weight:bold;">'.tra('May 29th, 2019:').'</span>'.tra('Dear All,<br><br>

We are happy to announce that we have TACC-branded gifts for top-10 volunteers as of May 29, 2019, calculated by recent average credit. If you are in the top-10 list - pasted below - and are comfortable in sharing your mailing address for receiving the gifts, please send your address to ritu.arora@utsa.edu.<br><br>

List of top-10 volunteers:<br><br>

Rank Name<br>
<b>1</b>  fsu95OTBmn<br>
<b>2</b>  VqOBVSxU66<br>
<b>3</b>  WIODAJAjcN<br>
<b>4</b>  UagA6nNtYD<br>
<b>5</b>  DrBob<br>
<b>6</b>  a4luBHEdoa<br>
<b>7</b>  Hans Sveen<br>
<b>8</b>  XXYjDCp4sK<br>
<b>9</b>  eG7kHKxeTJ<br>
<b>10</b> HOg09POs7b<br>
<br>
Thanks,<br><br>

BOINC@TACC team').' </p>';

echo '</style></pre></br>';


echo '<pre style="word-break:normal;white-space:normal;margin-left:20%;margin-right: 20%;"><style="text-align:left;"><p style="font-size:14px;font-weight: normal;"><span style="font-weight:bold;">'.tra('April 18th, 2019:').'</span>'.tra('A manuscript on BOINC@TACC has been published by Springer. Thanks to all the volunteers for making it possible. More information about the article is available at  <a href="https://link.springer.com/chapter/10.1007/978-981-13-7729-7_8"> https://link.springer.com/chapter/10.1007/978-981-13-7729-7_8</a>').' </p>';

echo '</style></pre></br>';



echo '<pre style="word-break:normal;white-space:normal;margin-left:20%;margin-right: 20%;"><style="text-align:left;"><p style="font-size:14px;font-weight: normal;"><span style="font-weight:bold;">'.tra('February 1st, 2019:').'</span>'.tra('Due to a database configuration issue, the BOINC@TACC project was unable to serve jobs to the volunteers for about a week. The issue has been mostly resolved now and the job scheduler is working as expected. We will be restoring the database content related to the volunteers by February 5, 2019. The data related to the researchers has not been impacted.').' </p>';

echo '</style></pre></br>';



echo '<pre style="word-break:normal;white-space:normal;margin-left:20%;margin-right: 20%;"><style="text-align:left;"><p style="font-size:14px;font-weight: normal;"><span style="font-weight:bold;">'.tra('January 1st, 2019:').'</span>'.tra('The TACC-2-BOINC project has been renamed to BOINC@TACC').' </p>';

echo '</style></pre></br>';


//List of News Updates
echo '<pre style="word-break:normal;white-space:normal;margin-left:20%;margin-right: 20%;"><style="text-align:left;"><p style="font-size:14px;font-weight: normal;"><span style="font-weight:bold;">'.tra('July 30th, 2018:').'</span>'.tra('TACC-2-BOINC project goes live today. Volunteers are now invited to join the project and donate the compute cycles. Individual volunteers can create their accounts on the TACC-2-BOINC website and download the BOINC client for donating compute-cycles on their devices or VMs that they own in the cloud. Institutional volunteers, can email Ritu Arora at ritu.arora@utsa.edu, to learn more about donating compute cycles.').' </p>';

echo '<p style="font-size:14px;font-weight: normal;">'.tra('TACC-2-BOINC can be used by the TACC researchers to run applications written in C, C++, Fortran, Python, Bash. The software infrastructure behind TACC-2-BOINC relies on the availability of the applications as Docker images. TACC researchers have the option of using the pre-built Docker images of the following applications that are maintained by us: Autodock-Vina, Bedtools, BLAST, Bowtie, GROMACS, HTSeq, LAMMPS, NAMD, and OpenSees. Researchers can also choose to run any other publicly available image in Docker Hub. If the researchers are not familiar with containerization, they can provide their source code with the instructions to build the executable, and our software framework can create the Docker image for them.').'</p>';

echo '<p style="font-size:14px;font-weight: normal;">'.tra('Happy computing with TACC-2-BOINC!').'</p></style></pre></br>';

page_tail();
//End of Gerald Joshua's Edit

?>

