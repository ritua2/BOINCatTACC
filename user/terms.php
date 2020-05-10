<?php
// This file is part of BOINC.
// http://boinc.berkeley.edu
// Copyright (C) 2008 University of California
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

/* 
Constructed by Thomas Johnson III
Terms of Use for Volunteers page for the TACC-2-BOINC website
Link located on the Sign Up Page
Required to be read before anyone can join as a Volunteer
*/
require_once('../inc/boinc_db.inc');
require_once('../inc/util.inc');
require_once('../inc/account.inc');
require_once('../inc/countries.inc');
require_once('../inc/translation.inc');
require_once('../inc/recaptchalib.php');

page_head(
    null, null, null, null, boinc_recaptcha_get_head_extra(), tra("Terms of Use")
);

echo '<align="left"><h3>'.tra("Terms of Use").'</h3>';
/*Edited by Joshua*/
echo '<p>Thanks a lot for donating the computing cycles to the TACC-2-BOINC project!';

echo '<br><br>';

echo '1) We will be saving the following data related to the computing cycles donated by you: Email Address, Screen Name, Password, ';

echo 'Country. We will be anonymizing your screen name for displaying your contributions on the leaderboard. We will notify you '; 

echo 'about the anonymized name assigned to your volunteer profile. If you would like to have your screen-name displayed on the leaderboard (instead of your anonymized name), please send us an email at ritu.arora@utsa.edu .';

echo '<br><br>';

echo '2) We guarantee the erasure of the aforementioned information from our server/s should you desire to do so after opting out as a '; 

echo 'volunteer. Please send an email at the following address to request the erasure of your data: ritu.arora@utsa.edu';

echo '<br><br>';

echo '3) Joining the TACC-2-BOINC project requires downloading the BOINC client and completing the sign-up process on the TACC-2-BOINC '; 

echo 'website. You are welcome to adjust the default settings of the BOINC client to start and stop running it as per your desire.';

echo '<br><br>';

echo '4) By joining the TACC-2-BOINC project as a volunteer, you would be donating the computing cycles of your devices and would be ';

echo 'footing the electricity bill associated with this donation.';

echo '<br><br>';

echo '5) The TACC-2-BOINC project team and/or the University of Texas at Austin would not be liable for any charges incurred with the '; 

echo 'aforementioned donation of computing cycles.</p></align>';  
/*End of the edit by Joshua*/
page_tail();
?>