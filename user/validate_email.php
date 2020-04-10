<?php

/*
BASICS

Parses the query of a URL to allow the user to verify their email
*/

require_once("../inc/boinc_db.inc");
require_once("../inc/util.inc");
require_once("../inc/email.inc");
require_once("../inc/xml.inc");
require_once("../inc/user_util.inc");
require_once("../inc/team.inc");



date_default_timezone_set("UTC");


$user_email = BoincDb::escape_string($_GET['email_addr']);
$secret_key = BoincDb::escape_string($_GET['validate_key']);



// Checks if the email has been verified
$user_data = BoincUser::lookup("email_addr = '$user_email'", "email_verification");
$email_verified_yet = $user_data->date_verified;


// User does not exist
if (! is_null($email_verified_yet)){
    echo "User '$user_email' does not have a BOINC@TACC account or this email has already been verified.";
    exit();
} 

$email_validation_key = $user_data->validation_key;

if ($email_validation_key == $secret_key){

    $current_UTC_date = date("Y-m-d H:i:s", time());

    // Sets the validation key as 1
    $db = BoincDb::get();
    $db->update_aux('email_verification', "date_verified='".$current_UTC_date."' WHERE email_addr = '$user_email'");

    $user_signup_email = $user_data->email_addr;
    $user_signup_name = $user_data->name;


    // Creates account
    make_user($user_data->email_addr, $user_data->name, $user_data->passwd_hash, $user_data->country, $user_data->postal_code,
                $user_data->project_prefs, $user_data->teamid);


    echo "Your email has been verified<br>Please click <a href=\"/login_form.php\">here</a> to login to your account";

} else {
    echo "Incorrect validation key";
    exit();
}



?>
