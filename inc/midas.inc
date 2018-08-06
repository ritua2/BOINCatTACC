<?php

/*
/ BASICS
/
/ Information about the MIDAS backend to be called from web interface API
*/



// Lists the OS available
function allowed_OS(){
    return array("ubuntu 16.04" => "Ubuntu_16.04");
}


// Languages available
function langs(){
    return array('python', 'r', 'c', 'c++', 'fortran', 'bash');
}


// Languages with libraries allowed
function langLibs(){
    return array("python", "c++");
}


// MIDAS tags
function Tags(){

    return array("OS", "LANGUAGE", "LIBRARY", "USER_SETUP", "COMMAND", "OUTPUT");
}

// Optional and mandatory  tags
function manTags(){

    return array(   "OS" => true,
                    "LANGUAGE"=> true,
                    "LIBRARY" => false,
                    "USER_SETUP" => false,
                    "COMMAND" => true,
                    "OUTPUT" => true
                );
}


// Returns the correct name of an OS
function accepted_OS($some_OS){

    if (array_key_exists(strtolower($some_OS), allowed_OS())){
        $allOS = allowed_OS();
        return $allOS[strtolower($some_OS)];
    }

    return false;
}


// Finds if a language is accepted
function accepted_lang($some_lang){

    return array_key_exists(strtolower($some_lang), langs());
}


// Finds if a language accepts libraries
function lang_accepts_libs($some_lang){

    return array_key_exists($some_lang, langLibs());
}


// Returns the list of tags, and if they are optional or not
function accepted_tags($some_tag){

    if (array_key_exists(strtoupper($some_tag), Tags())){
        $aTags = manTags();
        return $aTags[strtoupper($some_tag)];

    }

    return false;
}


// 

?>
