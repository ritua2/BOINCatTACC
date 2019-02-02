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



echo '<pre style="word-break:normal;white-space:normal;margin-left:20%;margin-right: 20%;"><style="text-align:left;"><p style="font-size:14px;font-weight: normal;"><span style="font-weight:bold;">'.tra('February 1st, 2019:').'</span>'.tra('Due to a database configuration issue, the BOINC@TACC project was unable to serve jobs to the volunteers for about a week. The issue has been mostly resolved now and the job scheduler is working as expected. We will be restoring the database content related to the volunteers by February 5, 2019. The data related to the researchers has not been impacted.').' </p>';

echo '</style></pre></br>';



echo '<pre style="word-break:normal;white-space:normal;margin-left:20%;margin-right: 20%;"><style="text-align:left;"><p style="font-size:14px;font-weight: normal;"><span style="font-weight:bold;">'.tra('January 1st, 2019:').'</span>'.tra('The TACC-2-BOINC project has been renamed to BOINC@TACC').' </p>';

echo '</style></pre></br>';


//List of News Updates
echo '<pre style="word-break:normal;white-space:normal;margin-left:20%;margin-right: 20%;"><style="text-align:left;"><p style="font-size:14px;font-weight: normal;"><span style="font-weight:bold;">'.tra('July 30th, 2018:').'</span>'.tra('TACC-2-BOINC project goes live today. Volunteers are now invited to join the project and donate the compute cycles. Individual volunteers can create their accounts on the TACC-2-BOINC website and download the BOINC client for donating compute-cycles on their devices or VMs that they own in the cloud. Institutional volunteers, can email Ritu Arora at rauta@tacc.utexas.edu, to learn more about donating compute cycles.').' </p>';

echo '<p style="font-size:14px;font-weight: normal;">'.tra('TACC-2-BOINC can be used by the TACC researchers to run applications written in C, C++, Fortran, Python, Bash. The software infrastructure behind TACC-2-BOINC relies on the availability of the applications as Docker images. TACC researchers have the option of using the pre-built Docker images of the following applications that are maintained by us: Autodock-Vina, Bedtools, BLAST, Bowtie, GROMACS, HTSeq, LAMMPS, NAMD, and OpenSees. Researchers can also choose to run any other publicly available image in Docker Hub. If the researchers are not familiar with containerization, they can provide their source code with the instructions to build the executable, and our software framework can create the Docker image for them.').'</p>';

echo '<p style="font-size:14px;font-weight: normal;">'.tra('Happy computing with TACC-2-BOINC!').'</p></style></pre></br>';

page_tail();
//End of Gerald Joshua's Edit

?>

