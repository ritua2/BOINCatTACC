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

// Provides a list of commonly asked questions and answers for volunteers

require_once("../inc/util.inc");
//Beginning of Thomas Johnson's edit
page_head(null, null, null, null, null, tra('Frequently Asked Questions (FAQ)'));
//End of Thomas Johnson's edit


//Page Title
echo '<center><h1>Frequently Asked Questions (FAQ)</h1></center><br>';



echo '<pre style="word-break:normal;white-space:normal;margin-left:20%;margin-right: 20%;"><style="text-align:left;"><p style="font-size:14px;font-weight: normal;"><span style="font-weight:bold;">'.tra('Issues with VirtualBox').'</span><br>'.tra('Certain versions of Virtual Box (e.g., 6.1.4 and 6.1.2) are having compatibility issues with the BOINC client used for processing BOINC@TACC jobs on certain operating systems. We do not have a solution for this right now but will update the users as soon as we have further information. Right now, Virtual Box version 5 is guaranteed to work.').' </p>';

echo '</style></pre><br>';


//End of the edit by Joshua
page_tail();
//End of Gerald Joshua's Edit

?>