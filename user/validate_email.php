<?php

/*
BASICS

Parses the query of a URL to allow the user to verify their email
*/

require_once("../inc/boinc_db.inc");



$complete_query = $_SERVER['QUERY_STRING'];
$sanitized_query =  BoincDb::escape_string($complete_query);

$query_parts = explode("-", $sanitized_query);

$user_email = $query_parts[0];
$secret_key = $query_parts[1];



// Checks if the email has been verified
$user_data = BoincUser::lookup("email_addr = '$user_email'", "user");
$email_val = $user_data->email_validated;


// User does not exist
if ($email_val != '0'){
    echo "User '$user_email' does not have a BOINC@TACC account or this account has already been validated.";
    exit();
} 

$email_validation_key = $user_data->validation_key;

if ($email_validation_key == $secret_key){

    // Sets the validation key as 1
    $db = BoincDb::get();
    $db->update_aux('user', "email_validated=1 WHERE email_addr = '$user_email'");

    echo "Your email has been verified<br>Please click <a href=\"/login_form.php\">here</a> following link to login to your account";

} else {
    echo "Incorrect validation key";
    exit();
}



?>
