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

include_once("../inc/util.inc");
include_once("../inc/user_util.inc");


$user = validate_post_make_user();

// In success case, redirect to a fixed page so that user can
// return to it without getting "Repost form data" stuff

if ($user) {
    // User was created
    echo "<br>An automated email has been sent to the provided email address for verification.";
} else {
    echo "<br>Could not create user";
}

?>
