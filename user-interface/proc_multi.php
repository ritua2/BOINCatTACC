<?php


if ($_SERVER['HTTP_REFERER'] != "http://$_SERVER[HTTP_HOST]/boincserver/submit_multi.html"){
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


// Stores the files in a lower directory, outside user access

$target_dir = "./token_data/process_files";

if ($_FILES["filfil"]["error"] == UPLOAD_ERR_OK){
    
    $temp_name = $_FILES["filfil"]["tmp_name"];
    $curname = trim(explode("/", $temp_name)[2]);
    $curname = $curname . ".txt";
    move_uploaded_file($temp_name, "$target_dir/$curname");
    // Adds the token information at the end of the file
    $tokadd = file_put_contents("$target_dir/$curname", "\n$user_token\n".PHP_EOOL, FILE_APPEND | LOCK_EX);
    exit("File has been succesfully submitted for processing");
}

else{
    exit("No file was submitted");
}

?>
