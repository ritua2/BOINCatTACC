<?php


if ($_SERVER['HTTP_REFERER'] != "http://$_SERVER[HTTP_HOST]/boincserver/submit_mm
ulti.html"){
   header("Location: http://$_SERVER[HTTP_HOST]/boincserver/submit_multi.html");
   exit('Cannot access page directly, token required');

}


include './token_data/validation.inc';
$user_token = $_POST['TOK'];


if ($user_token == ''){
   exit("Invalid, token not provided");
}

if (valid_token($user_token) == false){
   exit("Invalid token");
}

?>
