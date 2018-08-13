<?php
/* Started by Carlos
/ BASICS
/
/ Information about the MIDAS backend to be called from web interface API
*/
// Lists the OS available
function allowed_OS(){
    return array("ubuntu 16.04" => "Ubuntu_16.04");
}

//Edited by Joshua
// Languages available
function langs_list(){
    return array('python', 'r', 'c', 'cPlusPlus', 'fortran', 'bash');
}
//End of Joshua's Edit

// Languages with libraries allowed
// Return the programming languages allowed along with its 'name' attribute in the input type as key value pair array
function langLibs(){
    return array("python"=>"python3Lib", "cPlusPlus"=>"cPlusPlusLib");
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

    $allOS = allowed_OS();

    if (in_array(strtolower($some_OS), $allOS)){
        $allOS = allowed_OS();
        return $allOS[strtolower($some_OS)];
    }

    return false;
}


// Finds if a language is accepted
function accepted_lang($some_lang){

    $lans = langs();

    return in_array(strtolower($some_lang), $lans);
}


// Finds if a language accepts libraries
function lang_accepts_libs($some_lang){

    $lalibs = langLibs();

    return in_array($some_lang, $lalibs);
}


// Returns if a tag is optional or not
function accepted_tags($some_tag){

    $TT = Tags();

    if (in_array(strtoupper($some_tag), $TT)){
        $aTags = manTags();
        return $aTags[strtoupper($some_tag)];

    }

    throw new Exception("Tag is not accepted");
}


// Adds a tag and data
function properly_tagged($ttag, $ddata){

    $TT = Tags();

    if (! in_array($ttag, $TT)){
        return false;
    }

    return "[$ttag] $ddata";
}

//Updated by Joshua: Semicolon inserted at the end of return line
// Returns command instructions for all languages, except C and C++
function command_instructions($lang, $everything_else){
    
    return properly_tagged("COMMAND", "$lang: $everything_else");
}
//End of Joshua's edit

//End of Carlos' Edit
//Remove the last line by Joshua as php files cannot have blank line at the end
?>