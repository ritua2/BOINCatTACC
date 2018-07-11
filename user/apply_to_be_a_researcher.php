<?php

/*
Apply to be a Researcher webpage
6/27/2018
Thomas Hilton Johnson III
BOINC Project
*/

require_once("../inc/db.inc");
require_once("../inc/util.inc");
require_once("../inc/news.inc");
require_once("../inc/cache.inc");
require_once("../inc/uotd.inc");
require_once("../inc/sanitize_html.inc");
require_once("../inc/text_transform.inc");
require_once("../project/project.inc");
require_once("../inc/bootstrap.inc");


page_head(null, null, true);

//grid('top', 'left', 'right');

page_tail(false, "", true);
?>

