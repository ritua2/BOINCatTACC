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
//Beginning of Thomas Johnson's edit
page_head(null, null, null, null, null, tra('About'));
//End of Thomas Johnson's edit

//Page Title
//Thomas Johnson's edit to Gerald Joshua's edit: Rmoved the centering alignment tag
echo '<h3>'.tra("Project Overview").'</h3><p></p>';

//Project Overview
//Thomas Johnson's edit to Gerald Joshua's edit: Removed style that set fixed size fo the font for project overview
echo tra("Volunteer computing (VC) uses donated computing time to do scientific computing, and, BOINC is the most common software framework for VC. Essentially, donors of computing time download BOINC clients on their devices (such as laptops, desktops, and servers), and then register to donate at specific websites supporting VC projects. There are multiple such project websites in the community, and the TACC-2-BOINC website is one of them.
<br /><br />
Through the TACC-2-BOINC website (the website of our VC project), we are providing the capability of routing *qualified* High-Throughput Computing (HTC) jobs from the supercomputers at the Texas Advanced Computing Center (TACC) to the volunteered devices running the BOINC clients for the project. This integration of VC with supercomputing can potentially help those researchers/scholars who are running low on allocations of compute-time on our supercomputers, or are interested in reducing the turnaround time of their jobs when our supercomputers are over-subscribed. We are funded by NSF (under award # 1664022) to develop the BOINC-based VC conduit that can be used by other supercomputing facilities as well.").'
<br />';

echo tra("<p></p> For all questions, please feel free to contact Ritu Arora at rauta@tacc.utexas.edu, with \"TACC-2-BOINC\" included in the subject-line.");
echo "<br/>";

/*Commented out by Gerald Joshua since the pictures are now available
//Principal investigator
//Beginning of Thomas Johnson's edit on Gerald Joshua's edit: Provided a table that mimics the style and format of the stats.php page
//.tra("<h3>Principal Investigator of %1",PROJECT).":</h3>

     //<li><a href=\"https://www.tacc.utexas.edu/about/directory/ritu-arora\">".tra("Ritu Arora")."</a></ul>";
	echo "<tr><td>".tra("<h3>Project Team</h3>") .'<ul>
     <li><a href="https://www.linkedin.com/in/anubhawn/">'.tra("Anubhaw  Nand").'</a> (Graduate Student Intern, Software Development & Testing)
     <li><a href="https://www.linkedin.com/in/carlos-redondo-albertos">'.tra("Carlos Redondo").'</a> (Undergraduate Student Intern, Software Development & Testing)
     <li><a href="https://www.linkedin.com/in/geraldjoshua">'.tra("Gerald Joshua").'</a> (Undergraduate Student Intern, Software Development & Testing)
     <li><a href="https://www.tacc.utexas.edu/about/directory/ritu-arora">'.tra("Ritu Arora").'</a> (<strong>Project PI</strong>, Software Design and Architecture)
     <li><a href ="http://nia.ecsu.edu/sp/1617/johnson/">'.tra("Thomas Johnson").'</a> (Undergraduate Student Intern, Software Development & Testing)
</ul></tr></td>';
*/

/*Source of Team Website Template
https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_team
*/
/*
Bootstrap example for reference:
https://bootsnipp.com/snippets/featured/profile-card
*/
/*
Restructured due to div bug by Thomas
*/


echo tra("<h3>Project Team</h3>") .'<br>
<div class="container">
<div class="row">

  <div class="col-md-2">
    <div class="card" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
      <img src="/img1/Anubhaw_cropped.jpg" alt="Anubhaw" class="img-responsive">
      <div class="info" style="padding: 10px 10px;">
        <h4><a href="https://www.linkedin.com/in/anubhawn/">Anubhaw Nand</a></h4>
        <p class="title">Graduate Student Intern</p>
        <p>Software Development & Testing</p>
        </div>
    </div>
  </div>

  <div class="col-md-2">
    <div class="card" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
      <img src="/img1/Carlos_2018_cropped.jpg" alt="Carlos" class="img-responsive">
        <div class="info" style="padding: 10px 10px;">
        <h4><a href="https://www.linkedin.com/in/carlos-redondo-albertos">Carlos Redondo</a></h4>
        <p class="title">Undergraduate Student Intern</p>
        <p>Software Development & Testing</p>
        </div>
    </div>
  </div>

  <div class="col-md-2">
    <div class="card" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
      <img src="/img1/gerald_joshua_cropped.jpg" alt="Joshua" class="img-responsive">
      <div class="info" style="padding: 10px 10px;">
        <h4><a href="https://www.linkedin.com/in/geraldjoshua">Gerald Joshua</a></h4>
        <p class="title">Undergraduate Student Intern</p>
        <p>Software Development & Testing</p>
        </div>
    </div>
  </div>

<!-- Added by Gerald Joshua, copied from above -->
  <div class="col-md-2">
    <div class="card" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
      <img src="/img1/ritu_2_2018_cropped.jpg" alt="Ritu" class="img-responsive">
      <div class="info" style="padding: 10px 10px;">
        <h4><a href="https://www.tacc.utexas.edu/about/directory/ritu-arora">Ritu Arora</a></h4>
        <p class="title"><strong>Project PI</strong></p><br/>
        <p>Software Design and Architecture</p>
      </div>
    </div>
  </div>

  <div class="col-md-2">
    <div class="card" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
      <img src="/img1/Thomas_cropped.jpg" alt="Thomas" class="img-responsive">
      <div class="info" style="padding: 10px 10px;">
        <h4><a href ="http://nia.ecsu.edu/sp/1617/johnson/">Thomas Johnson</a></h4>
        <p class="title">Undergraduate Student Intern</p>
        <p>Software Development & Testing</p>
      </div>
    </div>
  </div>

</div>
</div>
<br>
';

//"/img/Thomas.jpg.jpeg.JPG"
//"/img/Joshua.jpg.jpeg"
//"/img/Anubhaw.jpg.jpeg"
/*
echo '<center><h1>'.tra("Principal Investigator of the Project").'</h1></center>';
echo '<center><span style="font-size: 24px; font-weight: bold;"><a href="https://www.tacc.utexas.edu/about/directory/ritu-arora">Ritu Arora</a></span></center>'.tra("Project Team") .'<ul>
     <li>Anubhaw  Nand (Graduate Student Intern, Software Development & Testing)
     <li><a href="https://www.linkedin.com/in/carlos-redondo-albertos">'.tra("Carlos Redondo").'</a> (Undergraduate Student Intern, Software Development & Testing)
     <li><a href="https://www.linkedin.com/in/geraldjoshua">'.tra("Gerald Joshua").'</a> (Undergraduate Student Intern, Software Development & Testing)
     <li><a href="https://www.tacc.utexas.edu/about/directory/ritu-arora">'.tra("Ritu Arora").'</a> (Design and Architecture)
     <li><a href =\"http://nia.ecsu.edu/sp/1617/johnson/\">'.tra("Thomas Johnson").'</a> (Undergraduate Student Intern, Software Development & Testing)
</ul></tr></td>';
*/

//Project Overview
/*
echo '<center><h1>'.tra("Project Team: ").'</h1></center>';
echo '<div style="font-size: 18px;"><center>
	Anubhaw Nand (Graduate Student Intern, Software Development & Testing)<br />
<a href="https://www.linkedin.com/in/carlos-redondo-albertos">Carlos Redondo</a> (Undergraduate Student Intern, Software Development & Testing)<br />
<a href="https://www.linkedin.com/in/geraldjoshua">Gerald Joshua</a> (Undergraduate Student Intern, Software Development & Testing)<br />
<a href="https://www.tacc.utexas.edu/about/directory/ritu-arora">Ritu Arora</a> (Design and Architecture)<br />
<a href ="http://nia.ecsu.edu/sp/1617/johnson/">Thomas Johnson</a> (Undergraduate Student Intern, Software Development & Testing)<br />
</center></div><br />';
*/
/*
Thomas Johnson linked Thomas Johnson's and Carlos Redondo's personal pages
*/
page_tail();
//End of Gerald Joshua's Edit

?>
