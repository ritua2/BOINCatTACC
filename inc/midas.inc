<?php

/*
/ BASICS
/
/ Information about the MIDAS backend to be called from web interface API
*/


// Returns the correct name of an OS
function accepted_OS($some_OS){

    $allowed_OS = array("ubuntu 16.04" => "Ubuntu_16.04");

    if (array_key_exists(strtolower($some_OS), $allowed_OS)){
        return $allowed_OS[strtolower($some_OS)];
    }

    return false;
}


// Finds if a language is accepted
function accepted_lang($some_lang){

    // Allowed languages
    $langs = array('python', 'r', 'c', 'c++', 'fortran', 'bash');

    if (array_key_exists($some_lang, $langs)){
        return true;
    }
    return false;
}


// Finds if a language accepts libraries
function lang_accepts_libs($some_lang){

    // Languages with libraries allowed
    $langLibs = array("python", "c++");

    if (array_key_exists($some_lang, $langLibs)){
        return true;
    }
    return false;
}


?>
