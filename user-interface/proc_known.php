<?php

// Prevents direct access

if ($_SERVER['HTTP_REFERER'] != "http://$_SERVER[HTTP_HOST]/boincserver/submit_known.html"){
    header("Location: http://$_SERVER[HTTP_HOST]/boincserver/submit_known.html");
    exit('Cannot access page directly, token required');
}


include './token_data/validation.inc';


$user_token = $_POST['TOK'];
$orders = $_POST['DERS'];
$image = $_POST['known'];


if ($user_token == ''){
   exit("Invalid, token not provided");
}

if (valid_token($user_token) == false){
   exit("Invalid token");
}

// Skips empty orders
if (trim($orders) == ''){
   exit('Invalid, empty command');
}

require './token_data/predis/autoload.php';
Predis\Autoloader::register();

// Adds the redis setup
try{
   $redis =  new Predis\Client(array(
             "scheme"=>"tcp",
             "host"=>"0.0.0.0",
             "port"=>6389));
   echo "Succesful connection to redis";
}
catch (Exception $exce) {
   echo "Could not connect to Redis<br>";
   echo $exce->getMessage();
}


// Different command depending on the image
date_default_timezone_set('America/Chicago');

switch ($image) {

  case "ADV":
     echo "AutoDock-Vina<br>Command submitted to server";

     // Adds data to Redis
     $prestime =date("Y-m-d H:i:s");
     $redis->rpush('Token', $user_token);
     $redis->rpush('Image', "carlosred/autodock-vina:latest");
     $redis->rpush('Command', $orders);
     $redis->rpush('Date (Sub)', $prestime);
     $redis->rpush('Date (Run)', '0');
     $redis->rpush('Error', 'ABC');
     $redis->rpush('Notified', '0');

     break;

  case "OPS":
     echo "Open-SEES<br>Command submitted to server";

     $prestime =date("Y-m-d H:i:s");
     $redis->rpush('Token', $user_token);
     $redis->rpush('Image', "saumyashah/opensees:latest");
     $redis->rpush('Command', $orders);
     $redis->rpush('Date (Sub)', $prestime);
     $redis->rpush('Date (Run)', '0');
     $redis->rpush('Error', 'ABC');
     $redis->rpush('Notified', '0');

     break;

  default:
     echo "Image not valid, use the general submit for known jobs";

}

?>