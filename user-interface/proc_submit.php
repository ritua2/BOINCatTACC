<?php

include './token_data/validation.inc';
$user_token = $_POST['TOK'];
$orders = $_POST['DERS'];

if (valid_token($user_token) == false){
   exit("Invalid token");
}

// Skips empty orders
if (trim($orders) == ''){
   exit('Invalid, empty command');
}

echo "Command submitted to the server <br>";
// Prints the result to a file
$secfil = fopen("./token_data/issued.txt", "a");
fwrite($secfil, $orders . "\n");
fclose($secfil);


?>
