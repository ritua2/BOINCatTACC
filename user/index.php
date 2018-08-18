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

// This is a template for your web site's front page.
// You are encouraged to customize this file,
// and to create a graphical identity for your web site.
// by customizing the header/footer functions in html/project/project.inc
// and picking a Bootstrap theme
//
// If you add text, put it in tra() to make it translatable.
//
//In the files of the BOINC project, this file is named homepage.php

require_once("../inc/db.inc");
require_once("../inc/util.inc");
require_once("../inc/news.inc");
require_once("../inc/cache.inc");
require_once("../inc/uotd.inc");
require_once("../inc/sanitize_html.inc");
require_once("../inc/text_transform.inc");
require_once("../project/project.inc");
require_once("../inc/bootstrap.inc");

$config = get_config();
$no_web_account_creation = parse_bool($config, "no_web_account_creation");//Parses the web accounts to see if one has been created (true if so)
    
$stopped = web_stopped();
$user = get_logged_in_user(false);

// The panel at the top of the page
//
function panel_contents() {
}

function top() {
    global $stopped, $master_url, $user;
    if ($stopped) {
        echo '
            <p class="lead text-center">'
            .tra("%1 is temporarily shut down for maintenance.", PROJECT)
            .'</p>
        ';
    }
    //panel(null, 'panel_contents');
}

function left(){/*
    global $user, $no_web_account_creation, $master_url;
    panel(
//This is where the panel begins.
       tra("What is %1?", PROJECT),

        function() use($user) {
            global $no_web_account_creation, $master_url;
            if (NO_COMPUTING) {
                echo "
                    XXX is a research project that uses volunteers
                    to do research in XXX.
                ";
            } else {
                echo "
                    <p>
                    The TACC-2-BOINC project brings the power of volunteer 
                    computing to the researchers and scholars using TACC 
                    resources. By taking advantage of the computing cycles 
                    donated by the volunteers, researchers and scholars 
                    can supplement the compute cycles granted to them as 
                    part of the TACC/XSEDE allocation process.
                    </p>
                ";
            }
            echo "
                <ul>
                <li> <a href=#>Our research</a>
                <li> <a href=#>Our team</a>
                <li> <a href=#> About this research </a>
    			<li> <a href=#> Help! </a>
                </ul>
            ";
            
            Added two links to the Project panel which ere previously in the drop down menu:
            $x[] = array(tra("About %1", PROJECT), $url_prefix."about.php");
    		$x[] = array(tra("Help"), $url_prefix."help.php");
    		which will be :
    		<li> <a href="about.php"> About this research </a>
    		<li> <a href="help.php"> Help! </a>
            
            echo "</ul>";
            if (!$user) {
                if (NO_COMPUTING) {
                    echo "
                        <a href=\"create_account_form.php\">Create an account</a>
		    ";
                } else {
                    echo '<left><a href="join.php" class="btn btn-success"><font size=+1>'.tra('Join %1 as a Volunteer', PROJECT).'</font></a></left>
                  
  			  ';

                }
            }
        }
);
//This is where the panel ends.
    global $stopped;
    if (!$stopped) {
        $profile = get_current_uotd();
        if ($profile) {
            panel('User of the Day',
                function() use ($profile) {
                    show_uotd($profile);
                }
            );
        }
    }
*/}

function right() {/*
    panel(tra('News'),
        function() {
            include("motd.php");
            if (!web_stopped()) {
                show_news(0, 5);
            }
        }
    );
*/}

page_head(null, null, true);

//grid('top', 'left', 'right');

echo "<script>
// When the user clicks on the `link` a popup appears
function myFunction() {
    var popup = document.getElementById(\"Popup\");
    popup.classList.toggle(\"show\");
}
function myFunction2() {
    var popup = document.getElementById(\"Popup2\");
    popup.classList.toggle(\"show\");
}
function myFunction3() {
    var popup = document.getElementById(\"Popup3\");
    popup.classList.toggle(\"show\");
}
function myFunction4() {
    var popup = document.getElementById(\"Popup4\");
    popup.classList.toggle(\"show\");
}
function myFunction5() {
    var popup = document.getElementById(\"Popup5\");
    popup.classList.toggle(\"show\");
}
</script>";


page_tail(false, "", true);

?>