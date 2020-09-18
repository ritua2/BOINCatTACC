<?php

// Sample BOINC project web config file.
// Modify it to suit your project.
// Put your version in html/project/project.inc
//
// add tra() around visible strings to make them translatable
// see inc/translation.inc and
// https://boinc.berkeley.edu/trac/wiki/TranslateProject for details

require_once("../inc/util.inc");
//Added by Gerald Joshua: Autoloader needs to be loaded so SMTP class could be found
require_once("../inc/phpmailer/PHPMailerAutoload.php");
//End of Joshua's Edit


// NEW
header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
header("Cache-Control: no-store, no-cache, must-revalidate");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");

// END NEW

//-------------- Project name and owner

define("PROJECT", "BOINC@TACC");//"REPLACE WITH PROJECT NAME"
define("COPYRIGHT_HOLDER", "University of Texas at Austin, All Rights Reserved.");//Second Argument: "REPLACE WITH COPYRIGHT HOLDER"

//-------------- URLs and directories

$master_url = parse_config(get_config(), "<master_url>");
define("URL_BASE", $master_url);
define("IMAGE_PATH", "../user_profile/images/");
define("IMAGE_URL", "user_profile/images/");
define("PROFILE_PATH", "../user_profile/");
define("PROFILE_URL", "user_profile/");
define("LANGUAGE_FILE", "languages.txt");
define("SECURE_URL_BASE", "https://boinc.tacc.utexas.edu/");


//-------------- contact info

define("SYS_ADMIN_EMAIL", "admin@$master_url");
define("UOTD_ADMIN_EMAIL", "admin@$master_url");
    // who gets emails about user of the day pool running low?
define("POST_REPORT_EMAILS", "moderator1@$master_url|moderator2@$master_url");
    // Email addresses separated by pipe ( | ) that will receive user reports
    // of offensive forum posts.
/*Addedby Joshua*/
define("EMAIL_FROM", "automatedresult.noreply@gmail.com");
    //Alias email address
define("EMAIL_FROM_NAME", "BOINC@TACC");
    //Alias email name
define("NO_REPLY_EMAIL", "no-reply@tacc.utexas.edu");
    //Alias email name

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
define("TEAM_CREATE_NEED_CREDIT", true);
    // Added by Joshua: Users won't be able to create teams unless they have credit

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
//Commented out by Gerald Joshua since BOINC@TACC will be using SMTP server
//to send forgot password emails 
//if (0) {
function make_php_mailer() {

    //Added by Joshua: Get the environment variables
    global $forgot_password_email;
    global $forgot_password_pass;
    global $forgot_password_reply;

    //Updated the code below so it will BOINC@TACC email
    $mail = new PHPMailer();
    $mail->IsSMTP();
    //$mail->Mailer = 'smtp';
    $mail->SMTPAuth = true;
    $mail->SMTPSecure = "tls";
    $mail->Host = "smtp.gmail.com";
    $mail->Port = 587;
    $mail->Username = getenv('FORGOT_PASSWORD_EMAIL');
    $mail->Password = getenv('FORGOT_PASSWORD_PASS');
        // Google's application-specific password,
        // if you are using the 2-Step Verification: 16 characters, no spaces.
        // OR: Put here the regular Gmail password if you are not using the
        // 2-Step Verification with your Gmail account.
        // See https://support.google.com/accounts/answer/185833?hl=en";
    $mail->SetFrom(EMAIL_FROM, EMAIL_FROM_NAME);
    $mail->AddReplyTo(NO_REPLY_EMAIL, EMAIL_FROM_NAME);
    $mail->From = EMAIL_FROM;
    return $mail;
}
//}
//End of the edit by Joshua

//-------------- Header and footer

// Put your project title and logo here
// If you include any links, prepend URL with $prefix
// if you need to open divs here close them in project_footer()
//For getting the footer to stay down on the page
//https://css-tricks.com/fun-viewport-units/
function project_banner($title, $prefix, $is_main) {
    echo '<div class="container-fluid" style="background-color:#003399; margin-left:-15px; margin-right:-15px; margin-bottom:0px; padding-bottom:0px; padding-top:10px;">
    <!--<div class="row">-->
<a href="/index.php"><img class="img-responsive" style="float: left; margin:2px 0px -5px 27px; padding: 0px; height:50px;" src="https://www.tacc.utexas.edu/documents/1084364/1748789/boinc-white.png/" /></a>
<!--  <div class="col-md-6" style=" margin-left: -2%;margin-top:1%;">

<a href="index.php" class="svg"><img class="img-responsive" src="./img1/boincattacc3x.png" style="margin-top: .5em;max-width:400px;height:58px;"></a>

    </div>
    <div class="col-md-6">
<a href="https://boinc.berkeley.edu/">
        <img class="img-responsive" style="width: 186px; margin-bottom: 23px; position:relative; right:-180px; top:6px; margin-right: 345px; float:right;" src="./img1/boincLogo_cropped.jpg" alt="Boinc Logo">
          </a>
          <a href="https://www.tacc.utexas.edu/">
        <img class="img-responsive" style="width: 230px; position: absolute; top: 4px; right: -50px; float: right;" src="./img1/taccLogo.png" alt="TACC Logo">
          </a>
    </div>-->
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
    /*Updated by Gerald Joshua so that there will be no horizontal scroll bar*/
    margin-left: -120px;
    /*End of the edit by Joshua*/
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

   <!-- <img class="img-responsive" style="margin-top:2.9%; height: 23vh;width: 100%;" src="img1/stampedecropped_1.jpg">-->
<div class="container-fluid" style="position: relative; z-index: 5; 
margin:-7px -36px 15px -36px; 
padding:45px 76px 35px 76px; 
text-align: left; 
font-size: 1.2em; 
background-color: #d6d3c4;
filter: alpha(opacity=50);
border-radius: 0px;">

<div class="col-md-12">
        <div  class="col-md-6">
    <h1 style="margin-top:7px;">VOLUNTEER COMPUTING</h1>
        <p>Contribute your extra computing power to open science. By running BOINC while your system is idle you will be powering discoveries that change the world.</p>
        <br />
    <p><a href="/create_account_form.php"><span style="padding:20px; border: solid 1px #000000; text-decoration: none;">JOIN BOINC&#64;TACC</span></a></p>
<br /><!--<p>Already joined? <a href="">Login Now!</a></p>--></div>
    <div  class="col-md-6">
    <img src="https://www.tacc.utexas.edu/documents/1084364/1748789/stampede-boinc.jpg/" class="img-responsive" />
    </div>
        </div>
</div>

<div class="container-fluid" style="position: relative; z-index: 5; 
margin:0px 0px -10px 0px;
padding:20px 40px 5px 40px;
text-align: left;
font-size: 1em;
background-color: #ffffff;
filter: alpha(opacity=50);
border-radius: 0px;">

<div class="col-md-12">
        <div  class="col-md-6">
        <p><b>What is BOINC&#64;TACC?</b><br />It is a project based on the Volunteer Computing (VC)  model. It helps TACC/XSEDE researchers in running applications from a wide range of scientific domains (such as, aerospace engineering, computational biology, and earthquake engineering) on the laptops, desktops, tablets, or cloud-based Virtual Machines (VMs) owned by volunteers.</p>
    <p><b>How can volunteers help?</b><br />Volunteers can help scientific research by signing up for the BOINC&#64;TACC project and allowing it to run applications on their computers and VMs. They may also need to download the required software from this website. To volunteer, <b><a href="/create_account_form.php">join BOINC&#64;TACC</a></b> after reading the <b><a href="/info.php">project policies</a></b>.</p>
        </div>
        <div  class="col-md-6">
<p><b>How do researchers benefit?</b><br />This project helps the 
    <a class="popup" data-toggle="tooltip" onclick="myFunction3()" style="text-decoration: none;">
        researchers 
        <span class="popuptext" style="left: 70%;" id="Popup3">
            <span class="close">&times;</span>
                All active users of TACC resources are eligible to run jobs through the BOINC@TACC infrastructure and qualify as researchers.
        </span>
    </a> 

    in supplementing the compute-cycles available through their <a href="https://portal.tacc.utexas.edu/allocations-overview" target="_blank">TACC</a>/<a href="https://portal.xsede.org/" target="_blank">XSEDE</a> allocations. With BOINC&#64;TACC, researchers can run small high-throughput computing jobs that involve small amounts of data transfer and processing without spending their active allocations. For details on using the BOINC&#64;TACC infrastructure, <a href="/how_to_use_TACC-2-BOINC.php">click here</a>.</p>
<p><b>How is BOINC&#64;TACC implemented?</b><br />
It leverages the 

    <a  class="popup" data-toggle="tooltip" onclick="myFunction4()" style="text-decoration: none;">
        BOINC 
        <span class="popuptext" style="left: -150%; top:=0%;" id="Popup4"> 
            <span class="close">&times;</span>
            BOINC is an open-source software platform for volunteer computing and it has a client-server architecture. Once a BOINC client is downloaded on a device (desktop, laptop, phone, tablet, or a VM running in the cloud) owned by a volunteer or an institution, the BOINC server running at TACC will start sending computational tasks to the client when it is plugged in to the power supply and is available to accept tasks. Upon the completion of the tasks, the results are gathered from the clients participating in the computations, and are uploaded to the BOINC server, from where they are then forwarded to the researchers.
            </span>
    </a>

    middleware and extends it to support the job submissions from supercomputers, uses the VMs in the cloud, and automatically creates Docker images of the source-code written in selected languages. The project source code is available on <a href="https://github.com/ritua2/BOINCatTACC" target="_blank">Github</a>.</p>        </div>
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
        <footer style="position:relative; margin-left: -15px; margin-right: -15px; margin-bottom: 0px; margin-top:0px; background-color: #323f48; padding: 15px 10px 15px 30px; text-align:center; color:#fff;height=105px;">
        <div class="container-fluid">
<a href="https://www.nsf.gov/"><img class="nsfLogo" src="./img1/nsf.jpg" width="65" height="65" alt="NSF Logo" style="float:left; border:none; margin-right:10px; margin-top"></a>
<p style="margin:13px 5px 5px 5px; font-size:12px; font-weight:bold; text-align:left; color: #cccccc;"> BOINC@TACC has been generously funded by <a href="https://www.nsf.gov/awardsearch/showAward?AWD_ID=1664022&HistoricalAwards=false" style="color: #cccccc;" target="_blank">NSF award #1664022</a></p>
<p style="margin:5px; font-size:12px; text-align:left; color: #cccccc;">&copy;2019 All Rights Reserved &nbsp;|&nbsp; <a href="https://boinc.berkeley.edu/" style="color: #cccccc;" target="_blank">BOINC</a> &nbsp;|&nbsp; <a href="https://www.tacc.utexas.edu/" style="color: #cccccc;" target="_blank">TACC</a> &nbsp;|&nbsp; <a href="https://www.utexas.edu/" style="color: #cccccc;" target="_blank">University of Texas at Austin</a></p>
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