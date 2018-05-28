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
   echo "Succesful connection to redis";
}
catch (Exception $exce) {
   echo "Could not connect to Redis<br>";
   echo $exce->getMessage();
} 

echo "Redis is set up";   
// Separates the array into image, and command
$new_orders = explode(" ", $orders);

AAA = '';

foreach($new_orders as $part){
       if $part != ''{
          $AAA = $AAA . $part;
       }

echo "<br>$AAA<br>";


   

// Prints the result to a file
$secfil = fopen("./token_data/issued.txt", "a");
fwrite($secfil, "$user_token ___ $orders" . "\n");
fclose($secfil);

?>
