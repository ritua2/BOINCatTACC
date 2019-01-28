<?php

function valid_token($toktok){


        $fh = fopen('/home/boincadm/project/html/user/token_data/Tokens.txt', 'r');
        while ($line= fgets($fh)){

               // Each line is separated into 3 parts by ;
               // Name and Last name
               // Token
               // Email
               $splitted = explode(',', trim($line));
               $seltok = trim($splitted[1]);

               if ($seltok == $toktok){
                       return true;
               }

        }

        return false;
}


?>
