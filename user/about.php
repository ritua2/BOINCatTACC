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

//Added by Joshua, copied from Thomas' code from project.inc
echo '<style>
/* Popup container - can be anything you want */
.popup {
    position: relative;
    display: inline-block;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

/* The actual popup */
.popup .popuptext {
    visibility: hidden;
    width: 32vw;
    background-color: #068fce;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 8px 0;
    position: absolute;
    z-index: 1;
    /*Updated by Gerald Joshua so that the tooltip will show right below the text
    and that way there will be no more overlap between navbar and tooltip*/
    top: 150%;
    margin-left: -80px;
}

/* Toggle this class - hide and show the popup */
.popup .show {
    visibility: visible;
    -webkit-animation: fadeIn 1s;
    animation: fadeIn 1s;
    /*Added by Joshua: Create more space between the tooltip edge and the text inside the tooltip */
    padding: 15px;
    /*End of the edit by Joshua */
}
/* Add animation (fade in the popup) */
@-webkit-keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity:1 ;}
}
//End of the edit by Joshua
</style>';

//Page Title
//Thomas Johnson's edit to Gerald Joshua's edit: Rmoved the centering alignment tag
echo '<h3>'.tra("Project Overview").'</h3><p></p>';

//Project Overview
//Thomas Johnson's edit to Gerald Joshua's edit: Removed style that set fixed size fo the font for project overview
//Edited by Joshua: Updated the text for BOINC@TACC
echo tra("Volunteer Computing (VC) is a form of computing that is done using donated compute-cycles. The BOINC@TACC project integrates supercomputing with VC. It provides the capability of routing *qualified* High-Throughput Computing (HTC) jobs from the supercomputers at the Texas Advanced Computing Center (TACC) to the volunteered devices running either the ").'<a  class="popup" data-toggle="tooltip" onclick="myFunction()" style="border-bottom: 1px dotted #000;text-decoration: none;">BOINC <span class="popuptext" style="left: -500%;" id="Popup"> <span class="close">&times;</span>BOINC is an open-source software platform for volunteer computing and it has a client-server architecture. Once a BOINC client is downloaded on a device (desktop, laptop, phone, tablet, or a VM running in the cloud) owned by a volunteer or an institution, the BOINC server starts sending computational tasks to the client when it is plugged in to the power supply and is available to accept tasks. Upon the completion of the tasks, the results are gathered from the clients participating in the computations, and are uploaded to the BOINC server, from where they are then forwarded to the researchers.</span></a>'.tra(" clients or another component that is a part of the BOINC@TACC software infrastructure. This integration of VC with supercomputing can potentially help those researchers/scholars who are running low on compute-time allocations on the TACC supercomputers, or are interested in reducing the turnaround time of their jobs when the supercomputers are over-subscribed.").'
<br /><br />'.tra("
To participate in the BOINC@TACC project, volunteers can either download the ").'<a href="./join.php">BOINC</a>'.tra(" clients on their devices (such as laptops, desktops, and servers), or they can download another software provided by the BOINC@TACC project on their VMs in the cloud. Additional information on the software for volunteering the VMs in the cloud can be sought by sending an email to ritu.arora@utsa.edu. After downloading the required software (for the devices or the VMs), the volunteers would need to register on the BOINC@TACC website by going ").'<a href="./create_account_form.php">here</a>.
<br /><br />'.tra("The researchers interested in using the BOINC@TACC infrastructure, can learn more about how to use it by following the steps in the ").'<a href="./how_to_use_TACC-2-BOINC.php">user-guide</a>
<br /><br />'.tra("The BOINC@TACC infrastructure relies on the availability of the researchers' applications as Docker images. The researchers have the option of running the pre-built Docker images of the following applications that are maintained by the BOINC@TACC project team: Autodock-Vina, Bedtools, BLAST, Bowtie, GROMACS, HTSeq, LAMMPS, NAMD, and OpenSees. The researchers can also choose any other publicly available image in Docker Hub and run it through the BOINC@TACC infrastructure. If the researchers are not familiar with containerization, they can use the software framework provided by the BOINC@TACC project to automatically create the Docker images. Currently, the BOINC@TACC project supports the automatic dockerization of applications written in C, C++, Fortran, Python, or Bash.").'
<br /><br />'.tra('For all questions regarding the BOINC@TACC project, please feel free to contact Dr. Ritu Arora at ritu.arora@utsa.edu, with "BOINC@TACC" included in the subject-line.');
echo "<br/>";
//End of Joshua Edit

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



echo tra("<h3>Current Team Members</h3>") .'<br>
<div class="container">
<div class="row">

  <div class="col-md-2">
    <div class="card" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
      <img src="/img1/Collin_cropped.jpg" alt="Collin" class="img-responsive">
      <div class="info" style="padding: 10px 10px;">
        <h4><a href="https://www.linkedin.com/in/collin-weir">Collin Weir</a></h4>
        <p class="title">System<br> Admin I</p>
        <p>Networking, Security & Operations</p>
        </div>
    </div>
  </div>


  <div class="col-md-2">
    <div class="card" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
      <img src="/img1/ritu_2_2018_cropped.jpg" alt="Ritu" class="img-responsive">
      <div class="info" style="padding: 10px 10px;">
        <h4><a href="https://www.linkedin.com/in/ritu-arora-59b58ab">Ritu Arora</a></h4>
        <p class="title"><strong>Project PI</strong></p><br/>
        <p>Software Design and Architecture</p>
      </div>
    </div>
  </div>

   <div class="col-md-2">
    <div class="card" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
      <img src="/img1/saumya.jpeg" alt="Saumya" class="img-responsive">
      <div class="info" style="padding: 10px 10px;">
        <h4><a href="https://www.linkedin.com/in/saumyashah7/">Saumya Shah</a></h4>
        <p class="title"><strong>Software Engineer</strong></p><br/>
        <p>Software Development & Testing</p>
      </div>
    </div>
  </div>
  
   <div class="col-md-2">
    <div class="card" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
      <img src="/img1/jaidip_3.jpeg" alt="Jaidip" class="img-responsive">
      <div class="info" style="padding: 10px 10px;">
        <h4><a href="https://www.linkedin.com/in/j-d-p/">Jaidip Patel</a></h4>
        <p class="title"><strong>Software Engineer</strong></p><br/>
        <p>Software Development & Testing</p>
      </div>
    </div>
  </div>  

</div>
</div>
<br>
';


echo tra("<h3>Previous Team Members</h3>") .'<br>
<div class="container">
<div class="row">

  <div class="col-md-2">
    <div class="card" style="box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
      <div class="info" style="padding: 10px 10px;">
        <h4><a href="https://www.tacc.utexas.edu/about/directory/jason-allison">Jason Allison</a></h4>
        <p class="title"><strong>Senior Program Coordinator</strong></p><br/>
        <p>Testing</p>
      </div>
    </div>
  </div>

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


//Added by Joshua, copied from Thomas's code on index.php
echo '<script>
// When the user clicks on the `link` a popup appears
function myFunction() {
    var popup = document.getElementById("Popup");
    popup.classList.toggle("show");
}
</script>';

//End of the edit by Joshua
page_tail();
//End of Gerald Joshua's Edit

?>
