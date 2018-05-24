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


// Different command depending on the image


switch ($image) {

  case "ADV":
     echo "AutoDock-Vina<br>Command submitted to server";
     $secfil = fopen("./token_data/issued.txt", "a");
     // Writes the instructions specific for the server
     fwrite($secfil, "carlosred/autodock-vina:latest /bin/bash -c \" " .  $orders . "; python /Mov_Res.py\"\n");
     fclose($secfil);
     break;

  case "OPS":
     echo "Open-SEES<br>Command submitted to server";
     $secfil = fopen("./token_data/issued.txt", "a");
     // Writes the instructions specific for the server
     fwrite($secfil, "carlosred/opensees:latest /bin/bash -c \"" .  $orders . ";  python /Mov_Res.py\"\n");
     fclose($secfil);
     break;


  default:
     echo "Image not valid, use the general submit for known jobs";

}


?>
