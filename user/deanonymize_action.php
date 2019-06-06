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

//Edited by Thomas Johnson III

require_once("../inc/util.inc");
require_once("../inc/user.inc");
require_once("../inc/boinc_db.inc");
require_once("../inc/deanonymize_user.inc");




check_get_args(array());

// show the home page of logged-in user

$user = get_logged_in_user();
$user = get_other_projects($user);


// To show the real username
if(isset($_POST['show_real_username'])) {
   
   $real_username = $user->name;
   use_real($real_username);
   // Returns to the home page
    echo'<script type="text/javascript">window.location="/home.php"</script>';


   exit();
}





// To show an anonymous username
if(isset($_POST['show_anonymous_username'])) {
   
   $real_username = $user->name;
   use_anonymous($real_username);
   // Returns to the home page
   echo'<script type="text/javascript">window.location="/home.php"</script>';

   exit();
}






?>
