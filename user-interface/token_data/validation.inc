<?php

function valid_token($toktok){


        $fh = fopen('/root/project/html/user/token_data/Tokens.txt', 'r');
        while ($line= fgets($fh)){

                if (trim($line) == $toktok){
                        return true;
                }
        }

        return false;
}


?>
