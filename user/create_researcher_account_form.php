<?php
// This file is part of BOINC.
// http://boinc.berkeley.edu
// Copyright (C) 2014 University of California
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

//Edited by Thomas Johnson III

require_once('../inc/boinc_db.inc');
require_once('../inc/util.inc');
require_once('../inc/account.inc');
require_once('../inc/countries.inc');
require_once('../inc/translation.inc');
require_once('../inc/recaptchalib.php');

page_head(
    null, null, null, null, boinc_recaptcha_get_head_extra(), "Create a Researcher Account"//Keeps the tab title as Create Account without making the tab title subject to changes in the <body>
);

echo '<meta name = "viewport" content = "width=device-width, initial-scale=1.0">';

//'<div style ="position:relative; left:36%;"> Original div used for spacing, caused issues as the div always retains the same amount of area in a webpage
echo '<a data-toggle="tooltip" style="margin-left: 36%; border-bottom: 1px dotted #000;text-decoration: none;"
title="All active users of TACC resources are eligible to run jobs
through the TACC-2-BOINC infrastructure and qualify as researchers."><font size=+3>'.tra("Create a Researcher Account").'</font></a>';//Repositions the `Create Account text on the webpage

echo '<br></br>';// Keeps the text from running into each other

echo '<span style="position:relative; left:36.335%;"><a href="https://portal.tacc.utexas.edu/account-request" class="btn btn-success"><font
>'.tra('Create Researcher Account').'</font></a></span>';////Establishes the Button for `Become a Researcher`, has positioning alterations
//echo '<center><font size=+2>'.tra("Become a Researcher:").'</font></center>'; //Code that was originally used when Thomas was separating the accounts' elements
//Using the tool-tip script that Joshua utilized on index.php
/*echo*/ /*attribute href of html tag a was removed by Gerald Joshua*//*'<font size=+1 style = "position:relative; left:36%;"><a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none;"
title="All active users of TACC resources are eligible to run jobs
through the TACC-2-BOINC infrastructure and qualify as researchers.
">'.tra("Become a Researcher:").'</a></font>';//Establishes the Tooltip for `Become a Researcher`, has positioning and font size alterations
echo '<br>';//Separation for aesthetic appeal
echo '<div>';
echo '<span style="position:relative; left:36.335%;"><a href="https://portal.tacc.utexas.edu/account-request" class="btn btn-success"><font
>'.tra('Create Researcher Account').'</font></a></span>';////Establishes the Button for `Become a Researcher`, has positioning alterations
*/
 //based off of https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_input_checked code
/*echo '<form action="" method="get">
  <input type="checkbox" name="Accept" value="Acceptance">I have read and Accept the Terms and Agreements or using TACC-2-BOINC and related BOINC software.
</form>';
*/
echo '<br>';//Separation

//https://stackoverflow.com/questions/21523730/html-checkbox-submit-button-by-agreeing-on-terms-and-condition
//The script for the Javascript button
//The button is by default disabled and only upon having the checkbox clicked does it become usable
/*
echo '<script>
 function disableSubmit() {
  document.getElementById("submit").disabled = true;
 }

  function activateButton(element) {

      if(element.checked) {

        document.getElementById("submit").disabled = false;
       }
       else  {
        document.getElementById("submit").disabled = true;
      }

  }
</script>';
*/
echo '</div>';
page_tail();
?>
