<?php


// This file is part of BOINC.
// http://boinc.berkeley.edu
// Copyright (C) 2017 University of California
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



// Functions for changing anonymous usernames
// Must be called after the database connection functions have been provided: inc/boinc_db.inc



// Returns true if a user is using its anonymous username
function using_anonymous_username($username){

    $sanitized_username =  BoincDb::escape_string($username);
    $user_data = BoincUser::lookup("name = '$sanitized_username'", "screen_name_anonymization");

    // Checks if both the random name and original random name are similar
    $current_random_name = $user_data->random_name;
    $orig_random_name = $user_data->original_random_name;

    if ($current_random_name == $orig_random_name){
        return TRUE;
    }

    return FALSE;

}



// Changes to show the real username
function use_real($username){

    $sanitized_username =  BoincDb::escape_string($username);
    $user_data = BoincUser::lookup("name = '$sanitized_username'", "screen_name_anonymization");

    // Checks if both the random name and original random name are similar
    $current_random_name = $user_data->random_name;
    $orig_random_name = $user_data->original_random_name;

    $db = BoincDb::get();
    $db->update_aux('screen_name_anonymization', "random_name='$sanitized_username' WHERE name='$sanitized_username'");
}


// Changes to the original show anonymous username
function use_anonymous($username){

    $sanitized_username =  BoincDb::escape_string($username);
    $user_data = BoincUser::lookup("name = '$sanitized_username'", "screen_name_anonymization");

    // Checks if both the random name and original random name are similar
    $current_random_name = $user_data->random_name;
    $orig_random_name = $user_data->original_random_name;

    $db = BoincDb::get();
    $db->update_aux('screen_name_anonymization', "random_name=original_random_name WHERE name='$sanitized_username'");
}





?>