<?php

// Prevents direct access
if ($_SERVER['HTTP_REFERER'] != "http://$_SERVER[HTTP_HOST]/boincserver/submit_jobs.php"){
    header("Location: http://$_SERVER[HTTP_HOST]/boincserver/submit_jobs.php");
    exit('Cannot access page directly, token required');
}

include './token_data/validation.inc';
$user_token = $_POST['TOK'];
$orders = $_POST['DERS'];

// Skips empty orders
if (trim($orders) == ''){
   exit('Invalid, empty command');
}

if ($user_token == ''){
   exit("Invalid, token not provided");
}

if ((valid_token($user_token) == false)){
   exit("Invalid token");
}


// Redis setup
require './token_data/predis/autoload.php';
Predis\Autoloader::register();

// Adds the redis setup
try{
   $redis =  new Predis\Client(array(
             "scheme"=>"tcp",
             "host"=>"0.0.0.0",
             "port"=>6389));
}
catch (Exception $exce) {
   echo $exce->getMessage();
   exit("Could not connect to Redis<br>");
} 

echo "Database connection established. <br>";   
// Separates the array into image, and command
$new_orders = explode(" ", $orders);
$Image = $new_orders[0];

$AAA = '';

for ($qq = 1; $qq <= count($new_orders); $qq++){

    $AAA = "$AAA ". $new_orders[$qq];
}


date_default_timezone_set('America/Chicago');
$prestime = date("Y-m-d H:i:s");
echo "$Image ; command submitted.<br>";   

// Adds the commands to Redis
$redis->rpush('Token', $user_token);
$redis->rpush('Image', $Image);
$redis->rpush('Command', $AAA);
$redis->rpush('Date (Sub)', $prestime);
$redis->rpush('Date (Run)', '0');
$redis->rpush('Error', 'ABC');
$redis->rpush('Notified', '0');

?>
