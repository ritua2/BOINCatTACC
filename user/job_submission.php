<?php
// This file is part of BOINC.
// http://boinc.berkeley.edu
// Copyright (C) 2016 University of California
//
// BOINC is free software; you can redistribute it and/or modify it
// under the terms of the GNU Lesser General Public License
// as published by the Free Software Foundation,
// either version 3 of the License, or (at your option) any later version.
//
// BOINC is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
// See the GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with BOINC.  If not, see <http://www.gnu.org/licenses/>.

//Added by Gerald Joshua

require_once("../inc/util.inc");

check_get_args(array());

//Any website visitors who have not signed in yet will be
//redirected to the sign in page
$user = get_logged_in_user();
BoincForumPrefs::lookup($user);

page_head(null, null, null, null, null, "Job Submission");

//Page Title
echo '<center><h1>Job Submission</h1></center><br />';
//End of Gerald Joshua's edit

//Added by Gerald Joshua
echo '
	<form action = "http://129.114.16.64/boincserver/job_submission_result.php" method = "post" enctype="multipart/form-data">
	<span style="margin-left: 17.3%; float:left; font-weight:bold;"><a data-toggle="tooltip" style ="border-bottom: 1px dotted #000; text-decoration: none;" title="The location of docker image that will be used can be from docker hub or from the list of available tacc-2-boinc docker images">'.tra("Location of docker image").'</a></span>
	<div style="float:left; margin-left: 3.5%;"><label style="margin-left: 3px;"><input type="radio" id="dockerOpt1" checked="checked"><span style="margin-left: 5px;">List of TACC-2-BOINC docker images</span></label></div>
	<div style="float:left; margin-left: 4%;"><label><input type="radio" id="dockerOpt2"><span style="margin-left: 5px;">Docker hub</span></label></div>
	<div id="taccDockerSection">
	<br /><br />
	<div class="dropdown" style="margin-left: 34.5%;" >
  		<button class="btn btn-primary dropdown-toggle" id="dockerListBtn" value="none"  style="background-color: #174b63; font-weight: bold;" type="button" data-toggle="dropdown"><span id="buttonText">List of TACC-2-BOINC docker images</span>
  		<span class="caret"></span></button>
		<input type="hidden" id="dockerListParam" name="dockerList" value="none">
  		<ul class="dropdown-menu">
    			<li value="carlosred/autodock-vina"><a href="javascript:;">AutoDock Vina</a></li>
    			<li value="carlosred/opensees"><a href="javascript:;">OpenSees</a></li>
    			<li value="carlosred/blast"><a href="javascript:;">BLAST</a></li>
			<li value="carlosred/bedtools"><a href="javascript:;">Bedtools</a></li>
 			<li value="carlosred/htseq"><a href="javascript:;">HTSeq</a></li>
			<li value="carlosred/gromacs"><a href="javascript:;">Gromacs</a></li>
			<li value="carlosred/mpi-lammps"><a href="javascript:;">LAMMPS</a></li>
			<li value="carlosred/namd-cpu"><a href="javascript:;">NAMD</a></li>
			<li value="carlosred/bowtie"><a href="javascript:;">Bowtie</a></li> 		
		</ul>
	</div><br />
	</div>
	<div id="dockerHubSection"><br /><br />';
//End of Gerald Joshua's edit
//Beginning of Thomas Johnson's edit

form_input_text(/*Commented out by Gerald Joshua
        sprintf('<!-- style of span was added by Gerald Joshua --><span style="%s" title="%s">%s</span>', "margin-left: 65%;",
            tra("Name of the Dockerhub Image that will be utilized."),
            '<!-- attribute href of html tag a was removed by Gerald Joshua --><a data-toggle="tooltip" style="border-bottom: 1px dotted #000;text-decoration: none;" 
            title="The name of the Dockerhub Image that will be utilized for this job submission. Provide the name, not the URL.">'.tra("Docker Hub Image").'</a>'
        ) End of Gerald Joshua's edit*/ "" ,
        "Image", "", "",/*Added by Gerald Joshua */"style='margin-bottom: 15px;' name='dockerFileName' id='dockerHubFile' placeholder='e.g., tacc/docker2singularity or nginx:1.14.0 (provide the name, not the URL)' value='none'"
/*End of Gerald Joshua's edit*/);

//Added by Gerald Joshua
echo "
	<button type='button' class='btn btn-success' id='checkBtn' style='font-weight: bold; margin-left: 34.5%;' onclick='checkIfExists();'>Check if it exists on docker hub</button>
	<div id='transparentGreyArea' style='background-color: grey; opacity: 0.5; filter: alpha(opacity=50); height: 100vh; width: 100%; z-index:9998;position: fixed; top: 0; left: 0;;'><i class='fa fa-spinner fa-spin' style='position: fixed; left: 50%; top: 50%; z-index:9999; font-size:60px'></i></div><span id='dockerNotification' style='margin-left: 10px; font-weight: bold;'></span>
	<br /><br /></div>";
//End of Gerald Joshua's edit

/*Commented out by Gerald Joshua
//It's better to use textarea tag than input tag for commands since there is a 
//big possibility that the number of lines of the commands is more than one 
form_input_text(sprintf('<!-- style of span was added by Gerald Joshua--><span style="%s" title="%s">%s</span>', "margin-left: 65%;", 
	tra("The list of commands to be processed."),
	'<!-- attribute href of html tag a was removed by Gerald Joshua --><a data-toggle="tooltip" style ="border-bottom: 1px dotted #000; text-decoration: none;"
	title="The list of commands that will be used in processing the data. Must provide all necessary commands.">'.tra("List of Commands").'</a>'
	),
	"Commands",""
);
*/

//Added by Gerald Joshua
//Most codes below were taken from the codes above

//Section for commands
echo '<span style="margin-left: 21.3%; font-weight:bold;"><a data-toggle="tooltip" style ="border-bottom: 1px dotted #000; text-decoration: none;" title="The list of commands that will be used in processing the data. Must provide all necessary commands.">'.tra("List of commands").'</a></span>';

echo '<textarea id="commandLines" name="theCommandLine" style="margin-top: -20px;margin-left: 34.5%;width: 64.5%;padding: 10px; border-radius: 5px;" rows="7" placeholder="e.g., gcc -o hello.exe hello.c (hit enter at each of the end the command line including the last command line)"></textarea><br /><br />';
tra("Please upload your relevant tar (.tgz or .tar.gz extensions only) or zip (.zip extenstion only) for the current submission.");
//End of commands section

/*Added by Gerald Joshua
Zip/Tar file upload section*/
echo '<span style="margin-left: 26%; float:left; font-weight:bold;"><a data-toggle="tooltip" style ="border-bottom: 1px dotted #000; text-decoration: none;" title="The list of input files or data that will be processed. Please zip the input files into one zip or one tar folder where the acceptable file extensions for the moment are .zip, .tgz, or .tar.gz ">'.tra("Input files").'</a></span>';
//End of Gerald Joshua's edit

//File Upload Code to be placed below
 echo /*Started by Thomas, edited by Gerald Joshua*/' 
<label style="margin-left:3%;"><input type="radio" id="tarUpload" checked="checked">
<span style="margin-left:5px;">Tar Upload</span></label>

<label style="margin-left: 30px;"><input type="radio" id="zipUpload"><span style="margin-left: 5px;">Zip Upload</span></label><br />

  <div style="margin-left:34.3%;">
<!-- Added by Gerald Joshua, sample code for form tag from Thomas -->
    <label class="btn btn-success" style="font-weight: bold; margin-bottom: 5px;">
    Browse <input type="file" name="file" id="uploadBtn" onchange="fileExtensionChecking(this);"> 
    </label>
    <span class="label label-info" id="fileLocation" style="font-size: 14px;">No file chosen</span> 
    <br /><span id="warningMsg" style="color: red; font-weight: bold;"><br /></span><br />
    <input type="hidden" id="theParameters" value="" />
    <input class="btn btn-success" type="submit" id="submitBtn" value="Submit the job" style="font-weight: bold;">
  </div>
</form>';

echo '<span id="testBtn"></span>';


//End of Thomas Johnson's edit

//Beginning of Gerald Joshua's edit
echo'
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script>
	//Checking variables
	var isDockerChosen = false;
	var isCommandInputed = false;
	var isFileUploaded = false;
	var lastDockerImgInputed = "";		

	//Submit button will be available if all fields are filled out
	function activateSubmitBtn(taccDocker, command, file){
		if (taccDocker && command && file){
			$("#submitBtn").prop("disabled",false);
		}
	}

	//Check if docker image inserted by the user exists in docker hub
	function checkIfExists(){
		$(".fa-spinner").show();
		$("#transparentGreyArea").show();
		var dockerImgName = $("#dockerHubFile").val();		
		var dockerImgFound = false;				
		lastDockerImgInputed = dockerImgName;		

		//Find if docker image has a tag or not
		if(dockerImgName.indexOf(":") > -1){//Colon exists
			$.ajax({
  				type: "POST",
  				url: "http://129.114.16.64/checkIfExists.php",
  				data: { 
					tagExists: "1",
					tag: String(dockerImgName.split(":")[1])					,dockerName: String(dockerImgName.split(":")[0])
				},
  				success: function(result){
					console.log(result);
					dockerImgFound = result;
					isDockerChosen = dockerImgFound;
					if(isDockerChosen){
						activateSubmitBtn(isDockerChosen, isCommandInputed, isFileUploaded);
					$("#dockerNotification").text("The docker image exists on docker hub");
					}
					else{
						$("#submitBtn").prop("disabled",true);
						$("#dockerNotification").text("The docker image DOES NOT exist on docker hub");
					}
					$(".fa-spinner").hide();
					$("#transparentGreyArea").hide();
				}			
			});
		} else {//No tag exists
			$.ajax({
  				type: "POST",
  				url: "http://129.114.16.64/checkIfExists.php",
  				data: { 
					tagExists: "0",
					dockerName: dockerImgName
				},
  				success: function(result){
						console.log(result);
						dockerImgFound = result;
						isDockerChosen = dockerImgFound;
						if(isDockerChosen){
						activateSubmitBtn(isDockerChosen, isCommandInputed, isFileUploaded);
					$("#dockerNotification").text("The docker image exists on docker hub");
					}
					else{
						$("#submitBtn").prop("disabled",true);
						$("#dockerNotification").text("The docker image DOES NOT exist on docker hub");
					}
					$(".fa-spinner").hide();
					$("#transparentGreyArea").hide();
				}			
			});
		}			
	}

	//Function that handles file extension checking process
	function fileExtensionChecking(fileName) {
		fileName = String(fileName.value);
    		fileExtension = fileName.substring((fileName.indexOf(".")+1));
		if($("#tarUpload").is(":checked")){
			if(fileExtension != "tgz" && fileExtension != "tar.gz"){
				$("#warningMsg").text("Warning message: The file extension must be either .tgz or .tar.gz");
				$("#warningMsg").show();
				isFileUploaded = false;
				$("#submitBtn").prop("disabled",true);	
			}
			else {
				isFileUploaded = true;
				activateSubmitBtn(isDockerChosen, isCommandInputed, isFileUploaded);
			}
		}	
		if($("#zipUpload").is(":checked")){
			if(fileExtension != "zip"){
				$("#warningMsg").text("Warning message: The file extension must be .zip");
				$("#warningMsg").show();
				isFileUploaded = false;
				$("#submitBtn").prop("disabled",true);
			}
			else {
				isFileUploaded = true;
				activateSubmitBtn(isDockerChosen, isCommandInputed, isFileUploaded);
			}
		}				
	}

	$(function(){
		//Initial condition
		$("#dockerHubSection").hide();
		$("#uploadBtn").hide();
		$("#warningMsg").hide();		
		$("#submitBtn").prop("disabled",true);
		$(".fa-spinner").hide();
		$("#transparentGreyArea").hide();

		//Check whether the command lines have been inputed or not
		$("#commandLines").bind("input propertychange", function() {
  			if(this.value.length > 0){
				isCommandInputed = true;
				activateSubmitBtn(isDockerChosen, isCommandInputed, isFileUploaded);					
			}
			else{
				$("#submitBtn").prop("disabled", true);
				isCommandInputed = false;
			}
		});

		//Put a semicolon at end of each command line if it does not hav e one
		$("#commandLines").keypress(function(theEnter){
			if (theEnter.keyCode == 13 && $(this).val().substring($(this).val().length - 1) != ";") {
        			$(this).val($(this).val() + "; ");
			}
		});
		
		$("#dockerHubFile").bind("input propertychange", function() {
			if(this.value != lastDockerImgInputed){
				isDockerChosen = false;
				$("#dockerNotification").text("");
				$("#submitBtn").prop("disabled", true);	
			}
			else if(this.value == lastDockerImgInputed){
				isDockerChosen = true;
				activateSubmitBtn(isDockerChosen, isCommandInputed, isFileUploaded);
			}
		});

		//For docker images dropdown list 
		$(".dropdown-menu li").click(function(){
			$("#buttonText").text($(this).text());
      			$("#dockerListBtn").val($(this).attr("value"));
   			$("#dockerListParam").val($(this).attr("value"));
			isDockerChosen = true;
			activateSubmitBtn(isDockerChosen, isCommandInputed, isFileUploaded);
		});
		$("#dockerOpt1").click(function(){
			$(this).prop("checked", true);
			$("#dockerOpt2").prop("checked", false);
			$("#dockerHubSection").hide();
			$("#taccDockerSection").show();
			$("#buttonText").text("List of TACC-2-BOINC docker images");
      			$("#dockerListBtn").val("none");
			$("#dockerListParam").val("none");
			isDockerChosen = false;
			$("#submitBtn").prop("disabled",true);
		});
		$("#dockerOpt2").click(function(){
			$(this).prop("checked", true);
			$("#dockerOpt1").prop("checked", false);
			$("#dockerHubSection").show();
			$("#taccDockerSection").hide();
			isDockerChosen = false;
			$("#submitBtn").prop("disabled",true);
			$("#dockerNotification").text("");
			$("#dockerHubFile").val("");
		});

		//For files upload
		$("#zipUpload").click(function(){
			$(this).prop("checked", true);
			$("#tarUpload").prop("checked", false);
			$("#warningMsg").hide();
			$("#fileLocation").text("No file chosen");
		});
		$("#tarUpload").click(function(){
			$(this).prop("checked", true);
			$("#zipUpload").prop("checked", false);
			$("#warningMsg").hide();
			$("#fileLocation").text("No file chosen");
		});
		$("#uploadBtn").on("change", function() {
			theFileLocation = $(this).val();
  			$("#fileLocation").text(theFileLocation);
		});	
	});
</script>
';
page_tail();
//End of Gerald Joshua's edit
?>
