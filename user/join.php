<?php

// This file is part of BOINC.
// http://boinc.berkeley.edu
// Copyright (C) 2016 University of California
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

require_once("../inc/util.inc");

function show_choose($is_old) {
    panel(null,
        function() use($is_old) {
            if ($is_old) {
                echo ' <a href="join.php">'.tra('I\'m new').'</a> &nbsp; |&nbsp; '.tra('I\'m a BOINC user').'
                ';
            } else {
                echo tra('I\'m new')
                    .' &nbsp; |&nbsp;  <a href="join.php?old=1">'
                    .tra('I\'m a BOINC user')
                    .'</a>
                ';
            }
        }
    );
}

function show_new() {
    global $master_url;
    panel(null,
        function() use ($master_url) {
            /*Edited by Joshua: We need ask the user to download virtual box before the 
            BOINC client software*/

            echo '<u><b>Mac and Linux users:</b></u>
                <ol>
                <li> <p>'
                .tra('Read our %1 Rules and Policies %2.', '<a href="info.php">', '</a>')
                .'</p><li>Go to the <a href="https://boinc.tacc.utexas.edu/create_account_form.php">Sign Up</a> page, create account. </li><li> <p>'
                .tra('Download %1 VirtualBox %2 (skip this step if you already have VirtualBox installed).', '<a href="https://www.virtualbox.org/wiki/Downloads">','</a>')
                .'</p>'
                .'<li> <p>'
                .tra('Download the BOINC desktop software.')
                    .'</p><p>
                    <a href="https://boinc.berkeley.edu/download_all.php" class="btn btn-success">'.tra('Download').'</a>
                    </p>
                <li> <p>'
                .tra('Run the installer.').'
                </p><li> '.tra("Choose %1 from the list, or enter %2", "<strong>".PROJECT."</strong>", "<strong>$master_url</strong>").'
                </ol>
            ';
            /*End of the edit by Joshua*/
            echo '<u><b>Windows users</b></u>
                <ol>
                <li> <p>'
                .tra('Read our %1 Rules and Policies %2.', '<a href="info.php">', '</a>')
                .'</p></li><li>Go to the <a href="https://boinc.tacc.utexas.edu/create_account_form.php">Sign Up</a> page, create account.</li><li><p>Either: </li>
        <p>    (a) Download <a href="https://boinc.berkeley.edu/download.php">BOINC+VirtualBox</a> software from the URL shown after you have created the account. <p>
                      
                       or

                <p>    (b) If you already have <a href="https://www.virtualbox.org/wiki/Downloads">VirtualBox</a> installed, download the <a href="https://boinc.berkeley.edu/download.php">BOINC software</a> only.
                </li><li>Run the installer.</li><li>
Choose BOINC@TACC from the drop-down list in the client or enter the following URL: https://boinc.tacc.utexas.edu/ </li>
                </ol>
            ';

        }
    );
}

function show_old() {
    global $master_url;
    panel(null,
        function() use($master_url) {
            echo '
                <ul>
                <li> '
                .tra('Install BOINC on this device if not already present.')
                .'<p>
                <li> '
                .tra('Select Tools / Add Project. Choose %1 from the list, or enter %2', "<strong>".PROJECT."</strong>", "<strong>$master_url</strong>")
                .' <p>
                <li> '
                .tra('If you\'re running a command-line version of BOINC on this computer, %1 create an account %2, then use %3 boinccmd --project_attach %4 to add the project.',
                    '<a href="create_account_form.php">',
                    '</a>',
                    '<strong><a href="http://boinc.berkeley.edu/wiki/Boinccmd_tool">',
                    '</a></strong>'
                )
                .'
                </ul>
            ';
        }
    );
}

$old = get_int('old', true);

page_head(tra("Join %1", PROJECT));
show_choose($old);
if ($old) {
    show_old();
} else {
    show_new();
}
page_tail();
