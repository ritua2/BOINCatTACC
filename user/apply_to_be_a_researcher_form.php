<?php

/*
Apply to be a Researcher webpage
6/27/2018
Thomas Hilton Johnson III
BOINC Project
Based off of create_account_form.php
*/


require_once('../inc/boinc_db.inc');
require_once('../inc/util.inc');
require_once('../inc/account.inc');
require_once('../inc/countries.inc');
require_once('../inc/translation.inc');
require_once('../inc/recaptchalib.php');

check_get_args(array("next_url", "teamid"));

$next_url = sanitize_local_url(get_str('next_url', true));

redirect_to_secure_url("http://$_SERVER[HTTP_HOST]/boincserver/apply_to_be_a_researcher_action.php?next_url=$next_url");

$config = get_config();
if (parse_bool($config, "disable_account_creation")) {
    error_page("This project has disabled account creation");
}

if (parse_bool($config, "no_web_account_creation")) {
    error_page("This project has disabled Web account creation");
}

page_head(
    tra("Apply to be a Researcher"), null, null, null, boinc_recaptcha_get_head_extra()
);

//If statement below offers path to the link provided by join button of man page
//Does not affect text responsible for gaining information for sign up

if (!NO_COMPUTING) {
    echo "<p class=\"lead\">"
        .tra(
            "If you already have an account and want to run %1 on this computer, %2 go here %3.",
            PROJECT,
            '<a href=join.php>',
            '</a>'
        )
        ."</p>
    ";
}

//When comented out affects team id
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

//function for creating an account
function researcher_validation_form($teamid, $next_url) {
    global $recaptcha_public_key;
    form_input_hidden('next_url', $next_url);

    if ($teamid) {
        form_input_hidden('teamid', $teamid);
    }

    // Using invitation codes to restrict access?
    //
    if (defined('INVITE_CODES')) {
        form_input_text(
            sprintf('<span title="%s">%s</span>',
                tra("An invitation code is required to create an account."),
                tra("Invitation code")
            ),
            "invite_code"
        );
    }
//The code that governs the PHP inputs for account information
    form_input_text(
        sprintf('<span title="%s">%s</span>',
            tra("Submit your first name."),
            tra("First Name (No spaces, commas, etc.)")
        ),
        $name = "name"
    );
    form_input_text(
        sprintf('<span title="%s">%s</span>',
            tra("Submit your last name."),
            tra("Last Name (No spaces, commas etc.)")
        ),
        $last_name="last_name"
    );
    form_input_text(
        sprintf('<span title="%s">%s</span>',
            tra("Must be a valid address of the form 'name@domain'."),
            tra("Email address (Nospaces, commas, etc.)")
        ),
        $email="email"
    );
    form_input_text(
        sprintf('<span title="%s">%s</span>',
            tra("Allocation should be an integer number."),
            tra("Allocation (Should only be an integer)")
        ),
        $allocation="allocation"
    );
    /*
    $min_passwd_length = parse_element(get_config(), "<min_passwd_length>");
    if (!$min_passwd_length) {
        $min_passwd_length = 6;
    }

    form_input_text(
        sprintf('<span title="%s">%s</span>',
            tra("Must be at least %1 characters", $min_passwd_length),
            tra("Password")
        ),
        "passwd", "", "password",'id="passwd"',passwd_visible_checkbox("passwd")
    );
    form_select(
        sprintf('<span title="%s">%s</span>',
            tra("Select the country you want to represent, if any."),
            tra("Country")
        ),
        "country",
        country_select_options()
    );
    */
    echo shell_exec("Curl -F name:\". $name . \" -F last_name:\"$last_name\" -F email:\"$email\" -F allocation:\"$allocation\" http://129.114.16.64:5054/boincserver/v2/api/request_user_token echo ' '");

}

/*
//Dominates the form submittig information
//Track down the dependencies governing this specifically
form_start("create_account_action.php","post");
create_account_form($teamid, $next_url);
if ($recaptcha_public_key) {
    form_general("", boinc_recaptcha_get_html($recaptcha_public_key));
}
//
*/

//Needs to be altered to send the validation to the currect address
form_start("apply_to_be_researcher_form.php","post");
researcher_validation_form($teamid, $next_url);
if ($recaptcha_public_key) {
    form_general("", boinc_recaptcha_get_html($recaptcha_public_key));
}
//Needs to be altered to send the validation to the correct address
form_submit(tra("Send Validation to Become a Researcher"));
//--====
form_end();

page_tail();

$cvs_version_tracker[]="\$Id$";  //Generated automatically - do not edit
?>

