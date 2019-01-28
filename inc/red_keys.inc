<?php

// Finds the organization key for any organization within the Redis database
require '/home/boincadm/project/html/user/token_data/autoload.php';
Predis\Autoloader::register();


// Gets the organization key for an organization name
// ONAM (str): Organization name
function get_ok($ONAM){

	// Adds the redis setup
	try{
	   $redis =  new Predis\Client(array(
	             "scheme"=>"tcp",
	             "host"=>"0.0.0.0",
	             "port"=>6389,
	         	 "database"=> 3));
	}
	catch (Exception $exce) {
	   echo "<p>Could not connect to Redis</p>";
	   echo $exce->getMessage();
	   exit;
	}


	try {
		 return $redis->hget("$ONAM", "Organization Token");
	}
	catch (Exception $e){
		return "Organization $ONAM is not registered";
	}


}


?>
