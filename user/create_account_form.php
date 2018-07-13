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

check_get_args(array("next_url", "teamid"));

$next_url = sanitize_local_url(get_str('next_url', true));

redirect_to_secure_url("create_account_form.php?next_url=$next_url");

$config = get_config();
if (parse_bool($config, "disable_account_creation")) {
    error_page("This project has disabled account creation");
}

if (parse_bool($config, "no_web_account_creation")) {
    error_page("This project has disabled Web account creation");
}

page_head(
    null, null, null, null, boinc_recaptcha_get_head_extra(), "Create Account"//Keeps the tab title as Create Account without making the tab title subject to changes in the <body>
);

echo '<meta name = "viewport" content = "width=device-width, initial-scale=1.0">';

//'<div style ="position:relative; left:36%;"> Original div used for spacing, caused issues as the div always retains the same amount of area in a webpage
echo '<a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none; position:relative; left:36%;"
title="Those interested in supporting R&D activities of researchers
and scholars using TACC resources are invited to join the
TACC-2-BOINC project as volunteers and the job for volunteers are
to donate their spare compute-cycles to the TACC-2-BOINC projects.">
<font size=+3">'.tra("Create a Volunteer Account").'</font></a>';//Repositions the `Create Account text on the webpage

echo '<br>';// Keeps the text from running into each other

if (!NO_COMPUTING) {
    echo '<font size=+1 style ="position:relative; left:25%;">'//Alters the font size and repositions the text
        .tra(
            "If you already have an account and want to run %1 on this computer, %2 go here %3.",
            PROJECT,
            '<a href=join.php>',
            '</a>'
        )
        ."</font>
    ";
}

$teamid = get_int("teamid", true);
if ($teamid) {
    $team = BoincTeam::lookup_id($teamid);
    $user = BoincUser::lookup_id($team->userid);
    if (!$user) {
        error_page("Team $team->name has no founder");
        $teamid = 0;
    } else {
        echo "<b>".tra("This account will belong to the team %1 and will have the project preferences of its founder.", "<a href=\"team_display.php?teamid=$team->id\">$team->name</a>")."</b><p>";
    }
}

echo '<br>';

//Using the tool-tip script that Joshua utilized on index.php
/*echo /*attribute href of html tag a was removed by Gerald Joshua*//*'<a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none; position:relative; left:36%;"
title="Those interested in supporting R&D activities of researchers
and scholars using TACC resources are invited to join the
TACC-2-BOINC project as volunteers and the job for volunteers are
to donate their spare compute-cycles to the TACC-2-BOINC projects.">
<font size=+1>'.tra("Become a Volunteer:").'</font></a>';//Establishes the `Become a Volunteer` Tooltip with associated information, font size was manipulated as wel as position
*/
echo '<br>';

form_start("create_account_action.php","post");//Starts the form for information input for the Volunteer
create_account_form($teamid, $next_url);
if ($recaptcha_public_key) {
    form_general("", boinc_recaptcha_get_html($recaptcha_public_key));
}

//http://www.phphaven.com/article.php?id=77
//$agree;

//<input type="submit" /> Ignore
/*
echo '<center>'.form_submit(tra("Create Volunteer Account")).'</center>';
echo '<br>';
echo '<center><a href="http://129.114.16.64/boincserver/terms.php">Terms of Use for Volunteers.</a></center>';
echo '<center><form action="" method="post">
<input type="checkbox" name="agree" value="<?php echo htmlspecialchars($agree);?>"/> I hereby
agree to the Terms of Use regarding being a Volunteer in the TACC-2-BOINC project.
</form></center>';
*/
//If condition for check box
//isset is used for true or false (if else) scenario
//Without preset value, remains stuck in the else statement
//With preset value, button loses responsiveness (no creating account)
//https://stackoverflow.com/questions/37111029/php-what-does-checkbox-default-value-on
/*
if (isset($agree)) {
echo '<center>'.form_submit(tra("Create Volunteer Account")).'</center>';
}
else {
echo '<p>Agree to the Terms of use first.</p>';
}
*/

//echo '<div style ="position:relative; left:36%;">'.form_submit(tra("Create Volunteer Account")).'</div>';

//https://stackoverflow.com/questions/21523730/html-checkbox-submit-button-by-agreeing-on-terms-and-condition
//<center>'.form_submit(tra("Create Volunteer Account")).'</center>;
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
//
echo '<body onload="disableSubmit()">
<span style = "position:relative; left:35%;">
<a href="http://129.114.16.64/boincserver/terms.php">Terms of Use for Volunteers.</a>
<br>
 <input type="checkbox" name="terms" id="terms" onchange="activateButton(this)" >I have read and agree to the Terms of Use of being a BOINC Volunteer.
<br><form method="post" action="">
<br>
  <input class="btn btn-success" type="submit" name="submit" id="submit" value="Create Volunteer Account"></form>
  </span>';//Places the Javascript button which had to have a different position measurement than the other elements of the webpage (The button is a checkbox, once clicked allows for the creation of a Volunteer Account), Joshua assisted with class which made the button matche the rest in style
echo "<br>";
//--------=====---------========------------================--------------==========--------------=====-----------------====--
form_end();


//echo '<br>';
//echo '<center><font size=+2>'.tra("Become a Researcher:").'</font></center>'; //Code that was originally used when Thomas was separating the accounts' elements
//Using the tool-tip script that Joshua utilized on index.php
/*attribute href of html tag a was removed by Gerald Joshua*/
/*
echo '<font size=+1 style = "position:relative; left:36%;"><a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none;"
//title="All active users of TACC resources are eligible to run jobs
//through the TACC-2-BOINC infrastructure and qualify as researchers.
">'.tra("Become a Researcher:").'</a></font>';//Establishes the Tooltip for `Become a Researcher`, has positioning and font size alterations
echo '<br>';//Separation for aesthetic appeal
echo '<div>';
echo '<span style="position:relative; left:36.335%;"><a href="https://portal.tacc.utexas.edu/account-request" class="btn btn-success"><font
>'.tra('Create Researcher Account').'</font></a></span>';////Establishes the Tooltip for `Become a Researcher`, has positioning alterations
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
echo '</div>';
page_tail();//End of page

$cvs_version_tracker[]="\$Id$";  //Generated automatically - do not edit
?>
