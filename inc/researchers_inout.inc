<?php

/* BASICS
/  
/  Logins as a researcher
/  Finds if a researcher is already logged in
/  Logs a researcher out
*/

require '/home/boincadm/project/html/user/token_data/autoload.php';
Predis\Autoloader::register();


// Sets the default timezone
date_default_timezone_set('America/Chicago');


// Returns a redis object on which to work on
function redup(){
	try{
	   return new Predis\Client(array(
	             "scheme"=>"tcp",
	             "host"=>"0.0.0.0",
	             "port"=>6389,
	         	 "database"=> 5));
	}
	catch (Exception $exce) {
	   echo "<p>Could not connect to Redis</p><p>Program aborted</>";

	   echo $exce->getMessage();
	   exit;
	}
}


// Checks if a researcher is logged in (key exists)
function logged_in($unam){
	try{
		$redis =redup();
		// Adds an entry with the username and the date of login
		return $redis->exists($unam);
	}
	catch (Exception $e){
		return "Redis error, could not check login information";
	}
}


// Logs in a researcher
// unam (str): Username

function res_login($unam){

	// Checks if the researcher is logged in first
	if (logged_in($unam)){
		return "User already logged in";
	}

	try{
		$redis =redup();
		// Adds an entry with the username and the date of login
		$redis->set("$unam", date("Y-m-d H:i:s"));
		return "Successful user login";
	}
	catch (Exception $e){
		return "Redis error, could not login";
	}

}


// Logs a user out
function logout($unam){
	// Checks if the user is already logged in
	if (! logged_in($unam)){
		return "User not logged in";
	}
	try{
		$redis =redup();
		// Adds an entry with the username and the date of login
		$redis->del(array($unam));
		return "Successfully logged out";
	}
	catch (Exception $e){
		echo "$e";
		return "Redis error, could not log out user";
	}
}


?>
