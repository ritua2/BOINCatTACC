<?php

require_once("../inc/util.inc");
require_once("../inc/researchers_inout.inc");
page_head(null, null, null, null,  null, "Log In Verification");

//Added by Gerald Joshua
if(!isset($_POST['username'])){
	echo "<script>window.location.replace('./login_as_a_researcher_form.php')</script>";
}
else {
	//Commented out by Thomas (allowed anyone to log in as a researcher)
	//End of Joshua's edit
	$username=$_POST["username"];
	$password=$_POST["password"];

	$ch = curl_init();


	//Edited by Gerald Joshua
	$url = "http://0.0.0.0:6032/boincserver/v2/api/ldap_check/".$username."/".$password;
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

	$result = curl_exec($ch);
	curl_close ($ch);

	echo "<br>";

	echo "<br><br>";

	if(substr($result,0,7)=="INVALID")
	{
		//Edited by Gerald Joshua
		echo tra("<center><h3>INVALID LOGIN</h3></center>");
		//End of the edit by Joshua

		//Added by Joshua
		echo '<center><a href="./login_as_a_researcher_form.php" class="btn btn-success" role="button">Go Back to Log In Page</a></center>';
		//End of the edit by Joshua
	}
	//https://stackoverflow.com/questions/503093/how-do-i-redirect-to-another-webpage
	else{
		if (!isset($_SESSION))
		{
	    		session_start();
		}

		$_SESSION['user']=$username;
		echo "<script>window.location.replace(\"./index.php\")</script>";
	}
}

page_tail();
?>