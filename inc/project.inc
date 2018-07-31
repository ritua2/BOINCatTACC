<?php

// Sample BOINC project web config file.
// Modify it to suit your project.
// Put your version in html/project/project.inc
//
// add tra() around visible strings to make them translatable
// see inc/translation.inc and
// https://boinc.berkeley.edu/trac/wiki/TranslateProject for details

require_once("../inc/util.inc");


//-------------- Project name and owner

define("PROJECT", "TACC-2-BOINC");//"REPLACE WITH PROJECT NAME"
define("COPYRIGHT_HOLDER", "University of Texas at Austin, All Rights Reserved.");//Second Argument: "REPLACE WITH COPYRIGHT HOLDER"

//-------------- URLs and directories

$master_url = parse_config(get_config(), "<master_url>");
define("URL_BASE", $master_url);
define("IMAGE_PATH", "../user_profile/images/");
define("IMAGE_URL", "user_profile/images/");
define("PROFILE_PATH", "../user_profile/");
define("PROFILE_URL", "user_profile/");
define("LANGUAGE_FILE", "languages.txt");

//-------------- contact info

define("SYS_ADMIN_EMAIL", "admin@$master_url");
define("UOTD_ADMIN_EMAIL", "admin@$master_url");
    // who gets emails about user of the day pool running low?
define("POST_REPORT_EMAILS", "moderator1@$master_url|moderator2@$master_url");
    // Email addresses separated by pipe ( | ) that will receive user reports
    // of offensive forum posts.

//-------------- Caching

//define("MEMCACHE_SERVERS", "127.0.0.1:11211");

//-------------- CSS styling

// add your own stylesheets (included after bootstrap)
//define("STYLESHEET", "aaa.css");
//define("STYLESHEET2", "bbb.css");

//-------------- enable/disable web features

define("FORUM_QA_MERGED_MODE", true);
    // Set to true to merge Message boards and Q&A section
define ("DISABLE_PROFILES", true);
    // enable profiles only after enabling reCAPTCHA
    // https://boinc.berkeley.edu/trac/wiki/ProtectionFromSpam
define("USE_STOPFORUMSPAM", true);
    // use http://www.stopforumspam.com to suppress spammer accounts
define("RPC_DEBUG", false);
    // Enables PHP error messages in public Web RPCs

//-------------- Project-specific preferences

define('COLOR_PREFS', false);
    // user can select screensaver color scheme
define('GFX_CPU_PREFS', false);
    // user can limit % CPU used by screensaver
    // (lower frame rate if exceeded)
    // This is probably irrelevant if your screensaver uses OpenGL
define('APP_SELECT_PREFS', false);
    // user can choose which apps to run
define('NON_GRAPHICAL_PREF', false);
    // user can choose to run faster non-graphical app versions if available
define('MAX_JOBS_PREF', false);
    // user can choose max # of jobs in progress
define('MAX_CPUS_PREF', false);
    // user can choose max # of CPUs to use

//-------------- PHPMailer

// If you use PHPMailer, uncomment the following
// and complete the function definition based on your SMTP server
// (not all fields may be needed)
//
if (0) {
function make_php_mailer() {
    $mail = new PHPMailer();
    $mail->IsSMTP();
    //$mail->Mailer = 'smtp';
    $mail->SMTPAuth = true;
    $mail->SMTPSecure = "tls";
    $mail->Host = "smtp.gmail.com";
    $mail->Port = 587;
    $mail->Username = "john.doe@gmail.com";
    $mail->Password = "xxx";
        // Google's application-specific password,
        // if you are using the 2-Step Verification: 16 characters, no spaces.
        // OR: Put here the regular Gmail password if you are not using the
        // 2-Step Verification with your Gmail account.
        // See https://support.google.com/accounts/answer/185833?hl=en";
    $mail->SetFrom('admin@boincproject.com', 'John Doe');
    $mail->AddReplyTo("admin@boincproject.com", "John Doe");
    $mail->From = "admin@boincproject.com";
    return $mail;
}
}

//-------------- Header and footer

// Put your project title and logo here
// If you include any links, prepend URL with $prefix
// if you need to open divs here close them in project_footer()
//For getting the footer to stay down on the page
//https://css-tricks.com/fun-viewport-units/
function project_banner($title, $prefix, $is_main) {
	echo '<div class="container-fluid">
	<!--<div class="row">-->
  <div class="col-md-6" style=" margin-left: -2%;">

<a href="index.php" class="svg"><img class="img-responsive" src="./img1/TACC-2-BOINC.svg" style="max-width:100%;height:104px;"></a>

	</div>
	<div class="col-md-6">
<a href="https://boinc.berkeley.edu/">
		<img class="img-responsive" style="width: 186px; margin-bottom: 23px; position:relative; right:-180px; top:6px; margin-right: 345px; float:right;" src="./img1/boincLogo_cropped.jpg" alt="Boinc Logo">
	      </a>
	      <a href="https://www.tacc.utexas.edu/">
		<img class="img-responsive" style="width: 230px; position: absolute; top: 4px; right: -50px; float: right;" src="./img1/taccLogo.png" alt="TACC Logo">
	      </a>
	</div>
	<!--</div>-->
        </div>
					';
    sample_navbar(secure_url_base(), get_logged_in_user(false), false);
    if ($title) {
        echo "<h2>$title</h2>\n";
        /*
        New line character causes space between nav-bar and the image below it.
        */
    }
    /*
    Means of creating the two columns
    https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_two_columns
    Adding a dividing border between the columns
    https://stackoverflow.com/questions/3313456/css-borders-between-table-columns-only
    */
    /*
    For the popups
    https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_popup
    */
    /*
    Reference for handling text box over an image
    https://www.w3schools.com/howto/howto_css_image_text_blocks.asp
    */
    if ($is_main) {
      echo '<style>
* {
    box-sizing: border-box;
}

/* Create two equal columns that floats next to each other */
.column {
    float: left;
    width: 50%;
    padding: 10px;
    border-right: solid;
}
.column:last-child
{
    border-right: none;
}
/* Clear floats after the columns */
.row:after {
    content: "";
    display: table;
    clear: both;
    width: 100%;
}
.footer
{
    overflow: hidden;
}
/* Popup container - can be anything you want */
.popup {
    position: relative;
    display: inline-block;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

/* The actual popup */
.popup .popuptext {
    visibility: hidden;
    width: 32vw;
    background-color: #068fce;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 8px 0;
    position: absolute;
    z-index: 1;
    /*Updated by Gerald Joshua so that the tooltip will show right below the text
    and that way there will be no more overlap between navbar and tooltip*/
    top: 150%;
    /*Updated by Gerald Joshua so that the tooltip will be visible enough in the screen of user without needing
    to scroll to the right*/
    left: -40%;
    /*End of the edit by Joshua*/
    margin-left: -80px;
}

/*Commented out by Gerald Joshua, since no arrow is needed
// Popup arrow
.popup .popuptext::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 25%;
    margin-left: -5px;
    border-width: px;
    border-style: solid;
    border-color: #174b63 transparent transparent transparent;
}
End of the Edit by Joshua*/

/* Toggle this class - hide and show the popup */
.popup .show {
    visibility: visible;
    -webkit-animation: fadeIn 1s;
    animation: fadeIn 1s;
    /*Added by Joshua: Create more space between the tooltip edge and the text inside the tooltip */
    padding: 15px;
    /*End of the edit by Joshua */
}
/* Add animation (fade in the popup) */
@-webkit-keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity:1 ;}
}
/*Close button for popups courtesy of https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_modal
.close {
    color: #fff;
    position:absolute;
    top:0;
    right:0;
    font-size: 28px;
    font-weight: bold;
}

.close:hover,
.close:focus {
    color: #fff;
    text-decoration: none;
    cursor: pointer;
}
</style>';
//Get rid of the `bold` effect on`text box https://jalbum.net/forum/thread.jspa?threadID=37879

        echo '<!-- <div style="position: absolute; z-index: 1; top: 29%;left: 12%;right: 12%;text-align: center;font-weight:bold;font-size: 60px;color: white;"> -->
			<!-- Welcome to TACC-2-BOINC! -->
<!-- </div> -->
		<!-- Small Summary about Boinc -->

    <img class="img-responsive" style="height: 23vh;width: 100%;" src="img1/stampedecropped.jpg">
		<div class="container-fluid" style="position: relative;
  /*Edited by Joshua: Increase the z-index so that the tooltip can be fully shown to the screen*/
  z-index: 5;/*End of the edit by Joshua*/
  top: 30%;
  left: 0%;
  right: 3%;
  text-align: left;
  /*font-weight:bold;Commented out for font size responsive to viewport size (Thomas Johnson)*/
  font-size: 1.2em;
  background-color: #E9E9E9;
  /*opacity: 0.75*/
  filter: alpha(opacity=50);
  padding: 1em;
  border-radius: 0px;">


			<div  class="col-md-6" style="border-right:solid black;">			<span style="font-weight:normal;font-size:calc(12px + (22 - 12) * ((100vw - 300px) / (3000 - 300)));"><p>BOINC is an open-source software platform for volunteer computing.
			BOINC has a client-server architecture. Once a BOINC client is downloaded on a device
			(desktop, laptop, phone, and a tablet) owned by a
<a class="popup" data-toggle="tooltip" onclick="myFunction()" style="border-bottom: 1px dotted #000;text-decoration: none;">volunteer<span class="popuptext" id="Popup"><span class="close">&times;</span>Those interested in supporting R&D activities of researchers and scholars using TACC resources are invited to join the TACC-2-BOINC project as volunteers and the job for volunteers are to donate their spare compute-cycles to the TACC-2-BOINC projects.</span></a>,
			the BOINC server starts sending computational tasks to the client when it is plugged in to the power supply
			and is available to accept tasks. Upon the completion of the tasks,
			the results are gathered from the clients participating in the computations,
			and are uploaded to the BOINC server, from where they are then forwarded to the <a  class="popup" data-toggle="tooltip" onclick="myFunction2()" style="border-bottom: 1px dotted #000;text-decoration: none;"> researchers <span class="popuptext" id="Popup2"> <span class="close">&times;</span>All active users of TACC resources are eligible to run jobs through the TACC-2-BOINC infrastructure and qualify as researchers.The TACC-2-BOINC project brings the power of </span></a>.</p><p>The TACC-2-BOINC project brings the power of volunteer computing to the </span>
      </div>
			<div class="col-md-6"> <span style="font-weight:normal;font-size:1.15vw;"><span style="font-weight:normal;font-size:calc(12px + (22 - 12) * ((100vw - 300px) / (3000 - 300)));"><a class="popup" data-toggle="tooltip" onclick="myFunction3()" style="border-bottom: 1px dotted #000;text-decoration: none;">researchers<span class="popuptext" id="Popup3"><span class="close">&times;</span> All active users of TACC resources are eligible to run jobs through the TACC-2-BOINC infrastructure and qualify as researchers. </span></a> using TACC resources.
			By taking advantage of the computing cycles donated by the <a class="popup" data-toggle="tooltip" onclick="myFunction4()" style="border-bottom: 1px dotted #000;text-decoration: none;">volunteers<span class="popuptext" id="Popup4"><span class="close">&times;</span>Those interested in supporting R&D activities of researchers and scholars using TACC resources are invited to join the TACC-2-BOINC project as volunteers and the job for volunteers are to donate their spare compute-cycles to the TACC-2-BOINC projects.</span></a>, the
			<a class="popup" data-toggle="tooltip" onclick="myFunction5()" style="border-bottom: 1px dotted #000;text-decoration: none;">researchers<span class="popuptext" id="Popup5"><span class="close">&times;</span>All active users of TACC resources are eligible to run jobs through the TACC-2-BOINC infrastructure and qualify as researchers.</span></a> can supplement the compute cycles granted to them as part of the TACC/XSEDE allocation process.</p><p> At present, only those users who have active allocation on TACC resources are allowed to submit jobs through the TACC-2-BOINC infrastructure.</p><p>To sign-up as a volunteer, click <a href="./create_account_form.php">here.</a></p>
      <p>To learn how to use TACC-2-BOINC, please click <a href="./how_to_use_TACC-2-BOINC.php">here</a>.</p></span>
      </div>

		</div>
    ';//water.jpg was a placeholder
    }
    /*
    https://upload.wikimedia.org/wikipedia/commons/1/14/Coyote_closeup.jpg
    Image recovered from Wikipedia Commons.
    Labeled for reuse.
    Previous image was img/water.jpg
    */
    /*
    This nav-bar was originally below the image:
    sample_navbar(secure_url_base(), get_logged_in_user(false), false);
    if ($title) {
        echo "<h2>$title</h2>\n";
    }
    */
}
//$fixed_navbar = true;

function project_footer($show_return, $show_date, $prefix) {
    // If you include any links, prepend URL with $prefix
    //
    //TACC Logo Edit
    //Thomas Johnson (Footer at the bottom of the page)
    //For getting the footer to stay down on the page
    //https://css-tricks.com/fun-viewport-units/
    echo '
    <div id="footer">
        <footer style="position:relative; margin-left: -15px; margin-right: -15px; bottom: 0;left:0; right:0; background-color: #174b63; padding: 10px; text-align:center; color:#fff;height=105px;">
        <div class="container-fluid">
                        <span style="font-size:20px; font-weight:bold;"> This project has been generously funded by the National
 Science Foundation (NSF) Award #1664022.
                <a href="https://www.nsf.gov/">
                                                <img class="nsfLogo" src="./img1/nsf.jpg" width="65" height="65" alt="NSF Logo">
                                        </a>
                        </span>
                <div class="container-fluid">
                <span> &copy;'.gmdate("Y ").COPYRIGHT_HOLDER.'</span>
                </div>
        </div>
        </footer>
        </div>
    ';
    /*
    Original code for the logos of TACC and BOINC
    <a class="brand boinc-logo" href="https://boinc.berkeley.edu/"><img align="middle" border="0" src="'.secure_url_base().'img/pb_boinc.gif" alt="Powered by BOINC"></a>
        <div style= "width: 210px; height: 80px; padding: 9px; background-color: #047ef6; color: #047ef6">
<img class="center" src="https://www.tacc.utexas.edu/tacc-new-theme/images/logo.svg" width="200" height="55" alt="TACC Logo" background-color=#73b2f22>
</div>
    */

    /*
    Updated version of the code:
    <div style= "width: 304px; height: 63px; padding: 5px; background-color: #047ef6; color: #047ef6">
        <a class="brand boinc-logo" href="https://boinc.berkeley.edu/"><img align="middle" border="0" src="'.secure_url_base().'img/pb_boinc.gif" alt="Powered by BOINC"></a>
<img class="center" src="https://www.tacc.utexas.edu/tacc-new-theme/images/logo.svg" width="180" height="40" alt="TACC Logo" background-color=#73b2f22></img>

</div>
    */
    if ($show_date) {
        $t = time_str(time());
        echo "<center><small>".tra("Generated")." $t</small><center>\n";
    }
}

//-------------- Ops access control

// Authorize access to administrative pages.
// You can check for login, IP address, or whatever you want.
//
function auth_ops_example() {
    // if running from cmdline, skip checks
    //
    if (!$_SERVER['REMOTE_ADDR']) {
        return;
    }

    // example: require login as a particular user (id 1 in this case)
    //
    if (0) {
        auth_ops_userid(array(1));
        return;
    }

    // example: require that logged-in user have ADMIN or DEV flags
    // set in their forum_prefs.privilege
    //
    if (0) {
        auth_ops_privilege();
        return;
    }
}

//-------------- Customizable functions

function show_profile_heading1() {
    return tra("Your personal background.");
}

function show_profile_question1() {
    return tra("Tell us about yourself. You could tell us where you're from, your age, occupation, hobbies, or anything else about yourself.");
}

function show_profile_heading2() {
    return tra("Your opinions about %1", PROJECT);
}

function show_profile_question2() {
    return tra("Tell us your thoughts about %1<ol>
    <li>Why do you run %1?
    <li>What are your views about the project?
    <li>Any suggestions?
    </ol>", PROJECT);
}

function project_workunit($wu){
    // shown in the workunit page
}

function project_user_summary($user){
    // shown in the user summary page
}

function project_user_page_private($user){
    // shown in the private account page
}

function project_forum_post_rules() {
    // additional forum post rules
    return "";
}

//-------------- Support for per-app credit

if (0) {

// show project-specific credit on user/team pages
//
function show_app_credit_user($user, $app_name, $appids) {
    $t = 0;
    $a = 0;
    $n = 0;
    foreach ($appids as $appid) {
        $cu = BoincCreditUser::lookup(
            "userid=$user->id and appid=$appid and credit_type=0"
        );
        if ($cu) {
            $t += $cu->total;
            $a += $cu->expavg;
            $n += $cu->njobs;
        }
    }
    row2("$app_name credit",
        format_credit_large($t)." total, ".
        format_credit($a)." average".
        " ($n tasks)"
    );
}
function show_app_credit_team($team, $app_name, $appids) {
    $t = 0;
    $a = 0;
    $n = 0;
    foreach ($appids as $appid) {
        $ct = BoincCreditTeam::lookup(
            "teamid=$team->id and appid=$appid and credit_type=0"
        );
        if ($ct) {
            $t += $ct->total;
            $a += $ct->expavg;
            $n += $ct->njobs;
        }
    }
    row2("$app_name credit",
        format_credit_large($t)." total, ".
        format_credit($a)." average".
        " ($n tasks)"
    );
}

// a list of "sub-projects", used in the display of per-app credit and badges.
// A subproject is:
// - a set of 1 or more apps; an app can belong to at most 1 subproject.
// - a name, shown on the web site
// - a short name, used in badge names.  Don't use "total".
//
$sub_projects = array(
    array("name" => "Remote Test", "short_name" => "RT", "appids" => array(16)),
    array("name" => "Uppercase", "short_name" => "UC", "appids" => array(1, 25)),
);

function project_user_credit($user){
    global $sub_projects;
    foreach ($sub_projects as $sp) {
        show_app_credit_user($user, $sp["name"], $sp["appids"]);
    }
}

function project_team_credit($team) {
    global $sub_projects;
    foreach ($sub_projects as $sp) {
        show_app_credit_team($team, $sp["name"], $sp["appids"]);
    }
}

}   // if(0)
?>
