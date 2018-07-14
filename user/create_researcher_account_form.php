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

echo "<br>";
echo "<div align=\"center\">";
echo "<font size=+1 align=\"center\">".tra("<p>TACC-2-BOINC uses the TACC Identity Service. To use TACC-2-BOINC you need to register for a TACC Account. With a TACC Account you will be able</p> <p>to access TACC-2-BOINC as well as additional services provided by TACC. See the TACC Website for more information.</p>")."</font>";
echo "</div>";
echo '<br></br>';// Keeps the text from running into each other
function create_researcher_account_form() {
    global $recaptcha_public_key;
/*    form_input_hidden('next_url', $next_url);

    if ($teamid) {
        form_input_hidden('teamid', $teamid);
    } */
echo "<div>";
form_input_text(
    sprintf('<span title="%s">%s</span>',
        tra("Your first name according government records."),
        '<!-- attribute href of html tag a was removed by Gerald Joshua --><a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none;"
        title="The first name that is listed for you on government records.
">'.tra("First Name").'</a>'
    ),
    "first_name"
);
echo "</div>";
form_input_text(
    sprintf('<span title="%s">%s</span>',
        tra("Your last name according government records."),
        '<!-- attribute href of html tag a was removed by Gerald Joshua --><a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none;"
        title="The last name that is listed for you on government records.
">'.tra("Last Name").'</a>'
    ),
    "last_name"
);

form_input_text(
    sprintf('<span title="%s">%s</span>',
        tra("Must be a valid address of the form 'name@domain'."),
        '<!-- attribute href of html tag a was removed by Gerald Joshua --><a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none;"
        title="The email address must be submitted in the form of `name@domain` and will
be used to contact you regarding any communications or related to this system,
website, etc.">'.tra("Email address").'</a>'
    ),
    "new_email_addr"
);

form_input_text(
    sprintf('<span title="%s">%s</span>',
        tra("The organization you are with."),
        '<!-- attribute href of html tag a was removed by Gerald Joshua --><a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none;"
        title="The organization that you are working under.">'.tra("Institution").'</a>'
    ),
    "institution"
);

form_select(
    sprintf('<span title="%s">%s</span>',
        tra("Country you live in."),
        '<!-- attribute href of html tag a was removed by Gerald Joshua --><a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none;"
        title="The country in which you are currently a resident.">'.tra("Country of Residence").'</a>'
    ),
    "country_residence", country_select_options()
);

form_select(
    sprintf('<span title="%s">%s</span>',
        tra("Your password check for the website."),
        '<!-- attribute href of html tag a was removed by Gerald Joshua --><a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none;"
        title="What country do you currently hold citizenship in?">'.tra("Country of Citizenship").'</a>'
    ),
    "country_citizen", country_select_options()
);

form_input_text(
    sprintf('<span title="%s">%s</span>',
        tra("Your username for the site."),
        '<!-- attribute href of html tag a was removed by Gerald Joshua --><a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none;"
        title="The username that will given to identify you on the site.
Note that it must be 3-8 characters in length, start with a letter
and can contain only lowercase letters, numbers, or underscore.">'.tra("Username").'</a>'
    ),
    "username_sys"
);


form_input_text(
    sprintf('<span title="%s">%s</span>',
        tra("Your password for the website."),
        '<!-- attribute href of html tag a was removed by Gerald Joshua --><a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none;"
        title="Look at the notes below for information
on creating a valid password.">'.tra("Password").'</a>'
    ),
    "password_sys"
);

form_input_text(
    sprintf('<span title="%s">%s</span>',
        tra("Your password check for the website."),
        '<!-- attribute href of html tag a was removed by Gerald Joshua --><a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none;"
        title="Make a secure passphrase for logging in as a
researcher.">'.tra("Password Check").'</a>'
    ),
    "passowrd_sys_check"
);
}
form_start(null,"post");
create_researcher_account_form();
form_end();
echo "<br>";
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
