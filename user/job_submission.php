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

page_head(null, null, null, null, null, "Job Submission");

if (!isset($_SESSION))
{
    session_start(); 
}

if(!isset($_SESSION['user'])){
	echo "<script>window.location.replace('./login_as_a_researcher_form.php');</script>";
}

//Page Title
echo '<center><h1>Job Submission</h1></center><br />';
//End of Gerald Joshua's edit

//Added by Gerald Joshua
//CSS
echo '
	<style>
	.tooltip-inner {
	  background-color: #00acd6 !important;
	  color: #fff;
	}

	.tooltip.top .tooltip-arrow {
	  border-top-color: #00acd6;
	}

	.tooltip.right .tooltip-arrow {
	  border-right-color: #00acd6;
	}

	.tooltip.bottom .tooltip-arrow {
	  border-bottom-color: #00acd6;
	}

	.tooltip.left .tooltip-arrow {
	  border-left-color: #00acd6;
	}
	</style>'
;

echo '
		<span style="margin-left: 17.3%; float:left; font-weight:bold;"><a href="javascript:;" data-toggle="tooltip" data-placement="bottom" title="The location of docker image that will be used can be from docker hub or from the list of available tacc-2-boinc docker images. Besides that, our system could also create a docker image for your job submission.">'.tra("Location of docker image ").'</a><span style="color: red">*</span></span>
		<div style="float:left; margin-left: 3.5%;"><label style="margin-left: 3px;"><input type="radio" id="dockerOpt1" checked="checked"><span style="margin-left: 5px;">List of Docker images maintained by BOINC@TACC</span></label></div>
		<div style="float:left; margin-left: 4%;"><label><input type="radio" id="dockerOpt2"><span style="margin-left: 5px;">Docker hub</span></label></div>
		<div style="float:left; margin-left: 4.5%;"><label><input type="radio" id="dockerOpt3"><span style="margin-left: 5px;">Automated docker build</span></label></div>

		<form action="./midas_job_submission_result.php" autocomplete="off" method="post" enctype="multipart/form-data">

		<!-- Section for option 3 -->
		<div id="automatedDockerSection">
			<!-- Section for list of OS -->
			<span style="font-weight:bold;">
				<br /><br />
				<!-- OS text -->
				<a href="javascript:;" data-toggle="tooltip" style ="margin:0 0 0 21.3%; data-placement="bottom" title="The operating system that will be used for running the job. We are only supporting ubuntu 16.04 as for now">'.
					tra("Operating System").'
				</a><span style="color: red">*</span>
			</span>

			<!-- List of OS TACC-2-BOINC is currently supporting -->
			<div class="dropdown" style="margin: -1.5% 0 0 35%;" >
		  		<button class="btn btn-primary dropdown-toggle" style="background-color: #174b63; font-weight: bold;" data-toggle="dropdown">
			  		<span id="btnText">List of operating system supported by TACC-2-BOINC</span>
			  		<span class="caret"></span>
			  	</button>
				<input type="hidden" id="osListParam" name="operating_system">
		  		<ul id="osDropDown" class="dropdown-menu">
		    			<li value="Ubuntu_16.04"><a href="javascript:;">Ubuntu-16.04</a></li> 		
				</ul>
			</div>

			<br />

			<!-- Section for programming languages list -->
			<span style="font-weight:bold;">
				<!-- Programming Language text -->
				<a href="javascript:;" data-toggle="tooltip" style ="margin:0 0 0 10.5%; data-placement="bottom" title="List all programming languages and libraries needed for running your job.">'.
					tra("Programming languages and libraries ").'</a><span style="color: red">*</span>
			</span>

			<!-- List of programming languages TACC-2-BOINC is currently supporting -->
			<div style="margin: -2.5% 0 2% 35%;">
				<!-- Python3 -->
				<div class="checkbox">
	  				<label style="font-weight:bold;">
	  					<input type="checkbox" id="p3" name="python">Python3 (We are not currently supporting Python 2)
	  				</label>
				</div>
				<div class="radio" id="radioP3">
					<label class="radio-inline" style="font-weight:bold;">
						<input type="radio" id="p31" name="p3Opt" checked>Python3 libraries needed
					</label>
					<label class="radio-inline" style="margin-left:3.5%;font-weight:bold;">
						<input type="radio" id="p32" name="p3Opt">No Python3 libraries needed
					</label>
				</div>
				<input type="text" id="p3Lib" class="form-control" placeholder="e.g., python-openstackclient, numpy (Provide only the module name. Separate each module name with a comma)" name="python3Lib"/>

				<!-- R -->
				<div class="checkbox">
				  	<label style="font-weight:bold;"><input id="r" type="checkbox" name="r">R</label>
				</div>

				<!-- C -->
				<div class="checkbox">
				  	<label style="font-weight:bold;"><input id="c" type="checkbox" name="c">C</label>
				</div>

				<!-- C++ -->
				<div class="checkbox">
				  	<label style="font-weight:bold;">
				  		<input type="checkbox" id="cPlusPlus" name="cPlusPlus">C++ (Please refer to this <a href="https://github.com/pfultz2/cget-recipes/tree/master/recipes" target="_blank">cget</a> package manager for the libraries)</label>
				</div>
				<div class="radio" id="radioC">
					<label style="font-weight:bold;">
						<input type="radio" id="c1" name="c++Lib" checked>C++ libraries needed
					</label>
					<label style="font-weight:bold;margin-left:3.5%;" class="radio-inline" id="c2">
						<input type="radio" name="c++Lib">No C++ libraries needed
					</label>
				</div>
				<input type="text" id="cLib" class="form-control" placeholder="e.g., boost, gnome (Provide only the package name. Separate each package name with a comma)" name="cPlusPlusLib"/>

				<!-- Fortran -->
				<div class="checkbox">
				  	<label style="font-weight:bold;">
				  		<input type="checkbox" id="fortran" name="fortran">Fortran
				  	</label>
				</div>

				<!-- Bash -->
				<div class="checkbox">
				  	<label style="font-weight:bold;">
				  		<input type="checkbox" id="bash" name="bash">Bash
				  	</label>
				</div>
			</div>

			<!-- Section for user setup -->
			<span style="font-weight:bold;">
				<!-- User setup text -->
				<a href="javascript:;" data-toggle="tooltip" style ="margin:0 0 0 26%; data-placement="top" title="User setup is used to cover package installation, compiling and linking so that the command lines will be mainly running the executable program. This part is very useful for C and C++. The set up file has to be a bash script file (.sh).">'.
					tra("Setup File ").'
				</a><span style="color: red">*</span>
			</span>

			<!-- User setup file -->
			<div style="margin: -2.5% 0 0 35%;">
				<div class="radio">
					<label style="font-weight:bold;">
						<input type="radio" id="setupFile1" name="setup_file_option" checked>Setup file needed
					</label>
					<label class="radio-inline" style="margin-left:3.5%; font-weight:bold;">
						<input type="radio" id="setupFile2" name="setup_file_option">No setup file needed
					</label>
					</span>
				</div>
				<div id="setup_options">
					<label class="btn btn-success btn-file" style="font-weight:bold; font-weight:bold;">
		    			Browse <input type="file" name="setup_file" id="setup_file_btn" style="display: none;" onchange="checkFileExtension(this);">
					</label>
					<span class="label label-info" id="setupFileLocation" style="font-size: 14px;">No file chosen</span>
					<br />
					<span id="setupFileMsg" style="color: red; font-weight: bold;">
				</div> 
			</div>

			<!--Section for midas job topics or subtopics-->
			<div id="midasTopics">
				<span style="margin-left: 13%; float:left; font-weight:bold;">
					<a href="javascript:;" data-toggle="tooltip" data-placement="bottom" title="Each job will be associated with one or more tags which are essentially the topics of the job submitted. Each topic can have a list of sub topic. Please follow the format specified in the input field.">'.tra("The Job Topic and/or Sub Topics").'
					</a>
				</span>';

			//The input field
			form_input_text("" , "Midas Topic", "", "","style='margin-left: 3%; margin-bottom: 18px;' name='midasTopic' id='midasTopicInput' placeholder='Format: T1;T2, e.g., biology;computer science. Capital letters will be transformed to lower case.' value=''");
			
			echo'
			</div>
			<!--End of midas job topics section or subtopics-->
			
			<br/>

			<!-- Section for commands -->
			<span style="font-weight:bold;">
				<!-- Commands text -->
				<a href="javascript:;" data-toggle="tooltip" style ="margin:0 0 0 25.5%;  data-placement="bottom" title="List all command lines needed to run the job.">'.
					tra("Commands").'
				</a><span style="color: red">*</span>
			</span>

			<!-- List of commands -->
			<div style="margin: -1.5% 0 0 34.5%;">
				<br/>
				<textarea id="command_line" name="commandLine" value="none" style="margin: -3% 0 0 0; width: 64.5%;padding: 10px; border-radius: 5px;" rows="7" placeholder="e.g., gcc -o hello.exe hello.c (hit enter at each of the end the command line including the last command line)"></textarea>
				<br/>
			</div>

			<br/>

			<!-- Section for output Files -->
			<span style="font-weight:bold;">
				<!-- Output text -->
				<a href="javascript:;" data-toggle="tooltip" style ="margin:0 0 0 25.5%;  data-placement="bottom" title="The result of the job has to be sent to the output files. List all of those output file names here.">'.
					tra("Output Files ").'</a><span style="color: red">*</span>
			</span>

			<!-- List of output files -->
			<div style="margin: -2.5% 0 0 34.5%;">
				<div class="radio">
					<label style="font-weight:bold;">
						<input type="radio" id="all_output_files" name="output_file_option" checked>Get all output files
					</label>
					<label class="radio-inline" style="margin-left:3.5%; font-weight:bold;">
						<input type="radio" id="some_output_files" name="output_file_option">Get only some output files
					</label>
					<input type="text" id="output_file_list" style="margin: 1.5% 0 0 0;" class="form-control" placeholder="e.g., output_file.txt, result.txt (List all the ouput files with its file extension. Separate each output file with a comma)" name="outputFileList" />
				</div>
			</div>
			
			<br />

			<!-- Section for input files -->
			<span style="font-weight:bold;">
				<!-- Input Files text -->
				<a href="javascript:;" data-toggle="tooltip" style ="margin:0 0 0 27%;  data-placement="bottom" title="The list of input files or data that will be processed. Please zip the input files into one zip or one tar file where the acceptable file extensions as for now are .zip, .tgz, or .tar.gz and the file size must be less than or equal to 100 MB">'.
					tra("Input files").'</a><span style="color: red">*</span>
			</span>

			<!-- Input Files -->
			<div style="margin: -1.5% 0 0 34.5%;">
				<label style="margin-left:">
					<input type="radio" id="midasTarUpload" name="inputFileOpt" checked="checked">
					<span style="margin-left:5px;">Upload compressed TAR file</span>
				</label>

				<label style="margin-left: 3%;">
					<input type="radio" id="midasZipUpload" name="inputFileOpt">
					<span style="margin-left: 5px;">Zip Upload</span>
				</label>

				<label style="margin-left:3%;">
					<input type="radio" id="midasNoUpload" name="inputFileOpt">
					<span style="margin-left:5px;">No Input Files</span>
				</label><br />

				<div id="midasSubmitPart">
					<label class="btn btn-success btn-file" style="font-weight:bold;">
		    			Browse <input type="file" id="midas_upload_btn" name="midas_input_file" onchange="midasFileExtensionChecking(this)" style="display: none;">
					</label>
					<span class="label label-info" id="midasFileLocation" style="font-size: 14px;">No file chosen</span>
					<br />
					<span id="midasWarningMsg" style="color: red; font-weight: bold;">
					<br />
					</span>
					<br />
				</div>
				<input type="hidden" id="" value="" />
				<input class="btn btn-success" type="submit" id="midasSubmitBtn" style="font-weight: bold;">
				<br/>
				<span style="color: black; font-weight:bold;">(<span style="color: red">*</span>) required</span>
			</div>			
		</div>
		</form>

		<form action="./job_submission_result.php" autocomplete="off" id="jobSubmissionForm" method="post" enctype="multipart/form-data">
		<div id="nonAutomatedDockerSection">
			<div id="taccDockerSection">
			<br /><br />
			<div class="dropdown" style="margin-left: 34.5%;" >
		  		<button class="btn btn-primary dropdown-toggle" id="dockerListBtn" value="none"  style="background-color: #174b63; font-weight: bold;" type="button" data-toggle="dropdown"><span id="buttonText">List of Docker images maintained by BOINC@TACC</span>
		  		<span class="caret"></span></button>
				<input type="hidden" id="dockerListParam" name="dockerList" value="none">
		  		<ul id="imgDropDown" class="dropdown-menu">
		    			<li value="carlosred/autodock-vina:latest"><a href="javascript:;">AutoDock Vina</a></li>
		    			<li value="saumyashah/opensees:latest"><a href="javascript:;">OpenSees</a></li>
		    			<li value="carlosred/blast:latest"><a href="javascript:;">BLAST</a></li>
						<li value="carlosred/bedtools:latest"><a href="javascript:;">Bedtools</a></li>
			 			<li value="carlosred/htseq:latest"><a href="javascript:;">HTSeq</a></li>
						<li value="carlosred/gromacs:latest"><a href="javascript:;">Gromacs</a></li>
						<li value="carlosred/mpi-lammps:latest"><a href="javascript:;">LAMMPS</a></li>
						<li value="carlosred/namd-cpu:latest"><a href="javascript:;">NAMD</a></li>
						<li value="carlosred/bowtie:built"><a href="javascript:;">Bowtie</a></li>
						<li value="carlosred/gpu:cuda"><a href="javascript:;">Cuda</a></li> 
						<li value="carlosred/openfoam6:latest"><a href="javascript:;">OpenFOAM6</a></li>

				</ul>
			</div><br />
			</div>
			<div id="dockerHubSection"><br /><br />';
		//End of Gerald Joshua's edit
		//Beginning of Thomas Johnson's edit

		form_input_text("" ,
		        "Image", "", "",/*Added by Gerald Joshua */"style='margin-bottom: 15px;' name='dockerFileName' id='dockerHubFile' placeholder='e.g., tacc/docker2singularity or nginx:1.14.0 (provide the name, not the URL)' value='none'"
		/*End of Gerald Joshua's edit*/);

		//Added by Gerald Joshua
		echo "
			<button type='button' class='btn btn-success' id='checkBtn' style='font-weight: bold; margin-left: 34.5%;' onclick='checkIfExists();'>Check if it exists on docker hub</button>
			<div id='transparentGreyArea' style='background-color: grey; opacity: 0.5; filter: alpha(opacity=50); height: 100vh; width: 100%; z-index:9998;position: fixed; top: 0; left: 0;;'><i class='fa fa-spinner fa-spin' style='position: fixed; left: 50%; top: 50%; z-index:9999; font-size:60px'></i></div><span id='dockerNotification' style='margin-left: 10px; font-weight: bold;'></span>
			</div>";
		//End of Gerald Joshua's edit

		/*Section for non-midas job topics or subtopics*/
		echo '<div id="nonMidasTopics">';
		echo '<span style="margin-left: 15%; float:left; font-weight:bold;"><a href="javascript:;" data-toggle="tooltip" data-placement="bottom" title="Each job will be associated with one or more tags which are essentially the topics of the job submitted. Each topic can have a list of sub topic. Please follow the format specified in the input field.">'.tra("The Job Topic and/or Sub Topics").'</a></span>';
		form_input_text("" , "Non Midas Topic", "", "","style='margin-bottom: 18px;' name='nonMidasTopic' id='nonMidasTopicInput' placeholder='Format: T1;T2, e.g., biology;computer science. Capital letters will be transformed to lower case.' value=''");
		echo '<br/><br/>';
		echo'</div>';
		/*End of non-midas job topics section or subtopics*/

		//Section for commands
		echo '<span style="margin-left: 21.3%; font-weight:bold;"><a href="javascript:;" data-toggle="tooltip" data-placement="bottom" title="The list of commands that will be used in processing the data. Must provide all the necessary commands. Hit enter for each command line to make sure that a semicolon is inserted.">'.tra("List of commands ").'</a><span style="color: red">*</span></span>';

		echo '<textarea id="commandLines" name="theCommandLine" style="margin-top: -20px;margin-left: 34.5%;width: 64.5%;padding: 10px; border-radius: 5px;" rows="7" placeholder="e.g., gcc -o hello.exe hello.c (hit enter at each of the end the command line including the last command line)"></textarea><br /><br />';
		tra("Please upload your relevant tar (.tgz or .tar.gz extensions only) or zip (.zip extenstion only) for the current submission.");
		//End of commands section
		//End of Gerald Joshua's edit

		/*Added by Gerald Joshua
		Zip/Tar file upload section*/
		echo '<span style="margin-left: 26%; float:left; font-weight:bold;"><a href="javascript:;" data-toggle="tooltip" data-placement="top" title="The list of input files or data that will be processed. Please zip the input files into one zip or one tar file where the acceptable file extensions as for now are .zip, .tgz, or .tar.gz and the file size must be less than or equal to 100 MB">'.tra("Input files ").'</a><span style="color: red">*</span></span>';
		//End of Gerald Joshua's edit

		//File Upload Code to be placed below
		 echo /*Started by Thomas, edited by Gerald Joshua*/' 
		<label style="margin-left:3%;"><input type="radio" id="tarUpload" checked="checked">
		<span style="margin-left:5px;">Compressed TAR file Upload</span></label>

		<label style="margin-left: 3.5%;"><input type="radio" id="zipUpload"><span style="margin-left: 5px;">Zip Upload</span></label>

		<label style="margin-left:4%;"><input type="radio" id="noUpload">
		<span style="margin-left:5px;">No Input Files</span></label><br />

		  	<div id="submitPart" style="margin-left:34.3%;">
				<!-- Added by Gerald Joshua, sample code for tag form from Thomas -->
			    <label id="theLabel" class="btn btn-success" style="font-weight: bold; margin-bottom: 5px;">
			    Browse <input type="file" name="file" id="uploadBtn" onchange="fileExtensionChecking(this);"> 
			    </label>
  			    <span class="label label-info" id="fileLocation" style="font-size: 14px;">No file chosen</span> 
			    <br /><span id="warningMsg" style="color: red; font-weight: bold;"><br /></span><br />
			    <input type="hidden" id="theParameters" value="" />
			</div>
			<input class="btn btn-success" type="submit" id="submitBtn" value="Submit the job" style="font-weight: bold;margin-left:34.3%;">
			<br/>
			<span style="color: black; font-weight:bold; margin-left:34.3%;">(<span style="color: red">*</span>) required</span>
		</div>
	</form>';
	//End of Joshua's edit
//End of Thomas Johnson's edit

//Beginning of Gerald Joshua's edit
?>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script>
	//Global variable
	var inputFile = $("#uploadBtn");
	var inputFileRemoved = false;
	var pLCount = 0;

	//Checking variables for non midas job
	var isDockerChosen = false;
	var isCommandInputed = false;
	var isFileUploaded = false;
	var lastDockerImgInputed = "";

	//Checking variables for midas job
	var checkingForMidas = {
	  	operating_system: false, 
	  	programming_language: false,
	  	setup_file: false, 
	  	library_list: true,
	  	output_files: true,
	  	input_file: false,
	  	command_lines: false
	};
	var isNoPython3LibChecked = false;
	var isNoCPlusPlusLibChecked = false;
	var isNoSetupFileChecked = false;
	var isAllOutputFilesChecked = true;
	var isNoInputFilesChecked = false;

	//Non-midas job submit button will be available if all fields are filled out
	function activateSubmitBtn(theDocker, command, file){
		if (theDocker && command && file){
			$("#submitBtn").prop("disabled",false);
		}
	}

	//Midas job submit button will be available if all fields are filled out
	function activateMidasSubmitBtn(checkingObj){
		var returnVal = true;
		for(var checkingVar in checkingObj){
			console.log("Key: "+checkingVar+", value: "+checkingObj[checkingVar]+"\n");
			returnVal &= checkingObj[checkingVar];
		}
		console.log("returnVal: "+returnVal);
		if(returnVal)
			$("#midasSubmitBtn").prop("disabled",false);
		else
			$("#midasSubmitBtn").prop("disabled",true);
	}

	//Check if docker image inserted by the user exists in docker hub
	function checkIfExists(){
		$(".fa-spinner").show();
		$("#transparentGreyArea").show();
		var dockerImgName = $("#dockerHubFile").val();		
		var dockerImgFound = false;				
		lastDockerImgInputed = dockerImgName;		

		//Find if docker image has a tag or not
		if(dockerImgName.indexOf(':') > -1){//Colon exists
			$.ajax({
  				type: "POST",
  				url: "./checkIfExists.php",
  				data: { 
					tagExists: "1",
					tag: String(dockerImgName.split(":")[1]),
					dockerName: String(dockerImgName.split(":")[0])
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
  				url: "./checkIfExists.php",
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

	//Function that handles the process of file extension for setup file
	function checkFileExtension(fileName){
		$("#setupFileMsg").html("");
		fileName = String(fileName.value);
		warningMessage = "";
    	fileExtension = fileName.substring((fileName.indexOf(".")+1));
		if(fileExtension != "sh"){
			warningMessage += "Warning: The file extension must be .sh";
			$("#setupFileMsg").html(warningMessage);
			$("#setupFileMsg").show();
			checkingForMidas.setup_file = false;
			activateMidasSubmitBtn(checkingForMidas);	
		}
		else {
			checkingForMidas.setup_file = true;
			activateMidasSubmitBtn(checkingForMidas);
		}
	}

	//Function that handles the process of file extension and file size checking for non midas
	function fileExtensionChecking(fileName) {
		$("#warningMsg").html("");
		fileSize = fileName.files[0].size;
		fileName = String(fileName.value);
		inputFileRemoved = false;	
  		$("#fileLocation").text(fileName);
		isFileSizeAllowed = true;
		warningMessage = "";
		if(fileSize > 104857600){
			warningMessage += "Warning: The file size must be less than 100 MB";
			isFileSizeAllowed = false;
		}
    	fileExtension = fileName.substring((fileName.indexOf(".")+1));
		if($("#tarUpload").is(":checked")){
			if(fileExtension != "tgz" && fileExtension != "tar.gz"){
				if(warningMessage != "")
					warningMessage += "<br />";
				warningMessage += "Warning: The file extension must be either .tgz or .tar.gz";
				$("#warningMsg").html(warningMessage);
				$("#warningMsg").show();
				isFileUploaded = false;
				$("#submitBtn").prop("disabled",true);	
			}
			else {
				isFileUploaded = true;
				if(!isFileSizeAllowed){
					$("#warningMsg").html(warningMessage);
					$("#warningMsg").show();
					$("#submitBtn").prop("disabled",true);
					isFileUploaded = false;
				}				
				activateSubmitBtn(isDockerChosen, isCommandInputed, isFileUploaded);
			}
		}	
		if($("#zipUpload").is(":checked")){
			if(fileExtension != "zip"){
				if(warningMessage != "")
					warningMessage += "<br />";
				warningMessage += "Warning: The file extension must be .zip";
				$("#warningMsg").html(warningMessage);
				$("#warningMsg").show();
				isFileUploaded = false;
				$("#submitBtn").prop("disabled",true);
			}
			else {
				isFileUploaded = true;
				if(!isFileSizeAllowed){
					$("#warningMsg").html(warningMessage);
					$("#warningMsg").show();
					$("#submitBtn").prop("disabled",true);
					isFileUploaded = false;
				}				
				activateSubmitBtn(isDockerChosen, isCommandInputed, isFileUploaded);
			}
		}				
	}

	//Function that handles the process of file extension and file size checking
	function midasFileExtensionChecking(fileName) {
		$("#midasWarningMsg").html("");
		fileSize = fileName.files[0].size;
		fileName = String(fileName.value);
		$("#midasFileLocation").text(fileName);
		isFileSizeAllowed = true;
		warningMessage = "";
		if(fileSize > 104857600){
			warningMessage += "Warning: The file size must be less than 100 MB";
			isFileSizeAllowed = false;
		}
    	fileExtension = fileName.substring((fileName.indexOf(".")+1));
		if($("#midasTarUpload").is(":checked")){
			if(fileExtension != "tgz" && fileExtension != "tar.gz"){
				if(warningMessage != "")
					warningMessage += "<br />";
				warningMessage += "Warning: The file extension must be either .tgz or .tar.gz";
				$("#midasWarningMsg").html(warningMessage);
				$("#midasWarningMsg").show();
				checkingForMidas.input_file = false;
				activateMidasSubmitBtn(checkingForMidas);	
			}
			else {
				isFileUploaded = true;
				checkingForMidas.input_file = true;
				if(!isFileSizeAllowed){
					$("#midasWarningMsg").html(warningMessage);
					$("#midasWarningMsg").show();
					checkingForMidas.input_file = false;
				}				
				activateMidasSubmitBtn(checkingForMidas);
			}
		}	
		if($("#midasZipUpload").is(":checked")){
			if(fileExtension != "zip"){
				if(warningMessage != "")
					warningMessage += "<br />";
				warningMessage += "Warning: The file extension must be .zip";
				$("#midasWarningMsg").html(warningMessage);
				$("#midasWarningMsg").show();
				checkingForMidas.input_file = false;
				activateMidasSubmitBtn(checkingForMidas);
			}
			else {
				isFileUploaded = true;
				checkingForMidas.input_file = true;
				if(!isFileSizeAllowed){
					$("#midasWarningMsg").html(warningMessage);
					$("#midasWarningMsg").show();
					checkingForMidas.input_file = false;
				}				
				activateMidasSubmitBtn(checkingForMidas);
			}
		}				
	}

	$(function(){
		//Initial condition
		$("#dockerHubSection").hide();
		$("#nonMidasTopics").hide();
		$("#midasTopics").hide();
		$("#uploadBtn").hide();
		$("#warningMsg").hide();		
		$("#submitBtn").prop("disabled",true);
		$(".fa-spinner").hide();
		$("#transparentGreyArea").hide();
		$("#automatedDockerSection").hide();
		$("#radioC").hide();
		$("#radioP3").hide();
		$("#cLib").hide();
		$("#p3Lib").hide();
		$("#output_file_list").hide();
		$("#midasSubmitBtn").prop("disabled",true);
		$("#midasSubmitBtn").prop("value", "Submit the job");

		//libraries and programming languages
		//R
		$("#r").click(function(){
			if($(this).is(':checked')){
				$(this).val("r");
				pLCount++;
				checkingForMidas.programming_language = true;
				activateMidasSubmitBtn(checkingForMidas);	
			}
			else{
				$(this).val("");
				if(pLCount > 0)
					pLCount--;
				if(pLCount == 0){
					checkingForMidas.programming_language = false;
					activateMidasSubmitBtn(checkingForMidas);
				}
			}
		});

		//C
		$("#c").click(function(){
			if($(this).is(':checked')){
				$(this).val("c");
				pLCount++;
				checkingForMidas.programming_language = true;
				activateMidasSubmitBtn(checkingForMidas);		
			}
			else{
				$(this).val("");
				if(pLCount > 0)
					pLCount--;
				if(pLCount == 0){
					checkingForMidas.programming_language = false;
					activateMidasSubmitBtn(checkingForMidas);
				}	
			}
		});


		//Bash
		$("#bash").click(function(){
			if($(this).is(':checked')){
				$(this).val("bash");	
				pLCount++;
				checkingForMidas.programming_language = true;
				activateMidasSubmitBtn(checkingForMidas);			
			}
			else{
				$(this).val("");
				if(pLCount > 0)
					pLCount--;
				if(pLCount == 0){
					checkingForMidas.programming_language = false;
					activateMidasSubmitBtn(checkingForMidas);
				}	
			}
		});

		//C++
		$("#cPlusPlus").click(function(){
			if($(this).is(':checked')){
				$(this).val("cPlusPlus");
				$("#radioC").show();
				$("#cLib").show();
				if(checkingForMidas.library_list){
					checkingForMidas.library_list = false;
					activateMidasSubmitBtn(checkingForMidas);
				}	
			}
			else{
				$(this).val("");
				$("#radioC").hide();
				$("#cLib").hide();
				if(pLCount > 0)
					pLCount--;
				if(pLCount == 0){
					checkingForMidas.programming_language = false;
				}
				$("#cLib").val("");
				checkingForMidas.library_list = true;
				if($("#p31").is(':checked') && $("#p3").is(':checked') && $("#p3Lib").value == ""){
					checkingForMidas.library_list = false;
				}
				activateMidasSubmitBtn(checkingForMidas);	
			}
		});
		$("#c1").click(function(){
			$("#cLib").show();
			checkingForMidas.programming_language = false;
			if(pLCount > 0)
				pLCount--;
			checkingForMidas.library_list = false;
			activateMidasSubmitBtn(checkingForMidas);
			isNoCPlusPlusLibChecked = false;
		});
		$("#c2").click(function(){
			$("#cLib").hide();
			pLCount++;
			$("#cLib").val("");
			checkingForMidas.library_list = true;
			if($("#p31").is(':checked') && $("#p3").is(':checked') && $("#p3Lib").value == ""){
				checkingForMidas.library_list = false;
			}
			checkingForMidas.programming_language = true;
			activateMidasSubmitBtn(checkingForMidas);
			isNoCPlusPlusLibChecked = true;
		});

		//Python
		$("#p3").click(function(){
			if($(this).is(':checked')){
				$(this).val("python");
				$("#radioP3").show();
				$("#p3Lib").show();
				if(checkingForMidas.library_list){
					checkingForMidas.library_list = false;
					activateMidasSubmitBtn(checkingForMidas);
				}		
			}
			else{
				$(this).val("");
				$("#radioP3").hide();
				$("#p3Lib").hide();	
				if(pLCount > 0)
					pLCount--;
				if(pLCount == 0){
					checkingForMidas.programming_language = false;
				}
				$("#p3Lib").val("");
				checkingForMidas.library_list = true;
				if($("#c1").is(':checked') && $("#cPlusPlus").is(':checked') && $("#cLib").value == ""){
					checkingForMidas.library_list = false;
				}
				activateMidasSubmitBtn(checkingForMidas);			
			}
		});
		$("#p31").click(function(){
			$("#p3Lib").show();
			checkingForMidas.programming_language = false;
			if(pLCount > 0)
				pLCount--;
			checkingForMidas.library_list = false;
			activateMidasSubmitBtn(checkingForMidas);
			isNoPython3LibChecked = true;
		});
		$("#p32").click(function(){
			$("#p3Lib").hide();
			checkingForMidas.programming_language = true;
			pLCount++;
			$("#p3Lib").val("");
			checkingForMidas.library_list = true;
			if($("#c1").is(':checked') && $("#cPlusPlus").is(':checked') && $("#cLib").value == ""){
				checkingForMidas.library_list = false;
			}
			activateMidasSubmitBtn(checkingForMidas);
			isNoPython3LibChecked = true;
		});
		
		//Fortran
		$("#fortran").click(function(){
			if($(this).is(':checked')){
				$(this).val("fortran");
				pLCount++;
				checkingForMidas.programming_language = true;
				activateMidasSubmitBtn(checkingForMidas);		
			}
			else{
				$(this).val("");
				if(pLCount > 0)
					pLCount--;
				if(pLCount == 0){
					checkingForMidas.programming_language = false;
					activateMidasSubmitBtn(checkingForMidas);
				}	
			}
		});

		//Setup Files
		$("#setupFile1").click(function(){
			if($(this).is(':checked')){
				$("#setup_options").show();
				$("#setupFileLocation").text("No file chosen");
				checkingForMidas.setup_file = false;
				activateMidasSubmitBtn(checkingForMidas);
				isNoSetupFileChecked = false;
			}
		});
		$("#setupFile2").click(function(){
			if($(this).is(':checked')){
				$("#setup_options").hide();
				$("#setup_file_btn").val("");
				checkingForMidas.setup_file = true;
				activateMidasSubmitBtn(checkingForMidas);
				isNoSetupFileChecked = true;
			}
		});
		$("#setup_file_btn").on("change", function() {
			theFileLocation = $(this).val();
  			$("#setupFileLocation").text(theFileLocation);
		});

		//Output Files
		$("#all_output_files").click(function(){
			$("#output_file_list").hide();
			$("#output_file_list").val("");
			checkingForMidas.output_files = true;
			activateMidasSubmitBtn(checkingForMidas);
			isAllOutputFilesChecked = true;
		});
		$("#some_output_files").click(function(){
			$("#output_file_list").val("");
			$("#output_file_list").show();
			checkingForMidas.output_files = false;
			activateMidasSubmitBtn(checkingForMidas);
			isAllOutputFilesChecked = false;
		});

		//Check whether the command lines have been inputed or not for non midas
		$("#commandLines").bind("input propertychange", function() {
  			if(this.value.indexOf(';') > -1){
				isCommandInputed = true;
				activateSubmitBtn(isDockerChosen, isCommandInputed, isFileUploaded);					
			}
			else{
				$("#submitBtn").prop("disabled", true);
				isCommandInputed = false;
			}
		});

		//Check whether the command lines have been inputed or not for midas
		$("#command_line").bind("input propertychange", function() {
			var midasCommandLines = this.value.split('\n');
			var commandLinesCorrect = true;
			for(var i = 0; i < midasCommandLines.length;i++){
				if(!midasCommandLines[i]){
				    if(midasCommandLines[i].indexOf(";") > -1)
				    	commandLinesCorrect &= true;
				    else
				    	commandLinesCorrect &= false;
				}
			}
  			if(commandLinesCorrect) {
				checkingForMidas.command_lines = true;
				activateMidasSubmitBtn(checkingForMidas);					
			}
			else{
				checkingForMidas.command_lines = false;
				activateMidasSubmitBtn(checkingForMidas);	
			}
		});

		//Check whether the library have been inputed or not for midas job
		$("#p3Lib, #cLib").bind("input propertychange", function() {
  			if(this.value.length > 0) {
  				checkingForMidas.library_list = true;
				if($("#p31").is(':checked') && $("#p3").is(':checked') && $("#p3Lib").value == ""){
					checkingForMidas.library_list = false;
				}
				if($("#c1").is(':checked') && $("#cPlusPlus").is(':checked') && $("#cLib").value == ""){
					checkingForMidas.library_list = false;
				}
				pLCount++;
				checkingForMidas.programming_language = true;					
			}
			else{
				checkingForMidas.library_list = false;
				checkingForMidas.programming_language = false;
			}
			activateMidasSubmitBtn(checkingForMidas);
		});

		//Check whether the outputList have been inputed or not for midas job
		$("#output_file_list").bind("input propertychange", function() {
  			if(this.value.length > 0) {
				checkingForMidas.output_files = true;					
			}
			else{
				checkingForMidas.output_files = false;
			}
			activateMidasSubmitBtn(checkingForMidas);
		});

		//Put a semicolon at end of each command line if it does not have one
		$("#commandLines, #command_line").keypress(function(theEnter){
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

		//For os dropdown list 
		$("#osDropDown li").click(function(){
			$("#btnText").text($(this).text());
   			$("#osListParam").val($(this).attr("value"));
			checkingForMidas.operating_system = true;
			activateMidasSubmitBtn(checkingForMidas);
		});

		//For docker images dropdown list
		$("#imgDropDown li").click(function(){
			$("#buttonText").text($(this).text());
      		$("#dockerListBtn").val($(this).attr("value"));
   			$("#dockerListParam").val($(this).attr("value"));
   			isDockerChosen = true;
			activateSubmitBtn(isDockerChosen, isCommandInputed, isFileUploaded);
		});

		$("#dockerOpt1").click(function(){
			$(this).prop("checked", true);
			$("#dockerOpt2").prop("checked", false);
			$("#dockerOpt3").prop("checked", false);
			$("#dockerHubSection").hide();
			$("#taccDockerSection").show();
			$("#nonAutomatedDockerSection").show();
			$("#automatedDockerSection").hide();
			$("#buttonText").text("List of Docker images maintained by BOINC@TACC");
      		$("#dockerListBtn").val("none");
			$("#dockerListParam").val("none");
			isDockerChosen = false;
			$("#submitBtn").prop("disabled",true);
			$("#nonMidasTopics").hide();
			$("#midasTopics").hide();
			$("#nonMidasTopicInput").val("");
			$("#midasTopicInput").val("");
		});
		$("#dockerOpt2").click(function(){
			$(this).prop("checked", true);
			$("#dockerOpt1").prop("checked", false);
			$("#dockerOpt3").prop("checked", false);
			$("#dockerHubSection").show();
			$("#taccDockerSection").hide();
			$("#nonAutomatedDockerSection").show();
			$("#automatedDockerSection").hide();
			isDockerChosen = false;
			$("#submitBtn").prop("disabled",true);
			$("#dockerNotification").text("");
			$("#dockerHubFile").val("");
			$("#nonMidasTopics").show();
			$("#midasTopics").hide();
			$("#nonMidasTopicInput").val("");
			$("#midasTopicInput").val("");
		});
		$("#dockerOpt3").click(function(){
			$(this).prop("checked", true);
			$("#dockerOpt1").prop("checked", false);
			$("#dockerOpt2").prop("checked", false);
			$("#dockerHubSection").hide();
			$("#taccDockerSection").hide();
			$("#nonAutomatedDockerSection").hide();
			$("#automatedDockerSection").show();
			$("#btnText").text("List of operating system supported by TACC-2-BOINC");
			$("#osListParam").val("none");
			$("#nonMidasTopics").hide();
			$("#midasTopics").show();
			$("#nonMidasTopicInput").val("");
			$("#midasTopicInput").val("");
			isThirdOption = true;
		});

		//For non-Midas files upload
		$("#zipUpload").click(function(){
			inputFileRemoved = false;
			$("#submitPart").show();
			$(this).prop("checked", true);
			$("#tarUpload").prop("checked", false);
			$("#noUpload").prop("checked", false);
			$("#warningMsg").hide();
			$("#fileLocation").text("No file chosen");
			$("#submitBtn").prop("disabled",true);
		});
		$("#tarUpload").click(function(){
			inputFileRemoved = false;
			$("#submitPart").show();
			$(this).prop("checked", true);
			$("#zipUpload").prop("checked", false);
			$("#noUpload").prop("checked", false);
			$("#warningMsg").hide();
			$("#fileLocation").text("No file chosen");
			$("#submitBtn").prop("disabled",true);
		});
		$("#noUpload").click(function(){
  			//$("#uploadingPart").wrap("<form>").closest("form").get(0).reset();
			//$("#uploadingPart").unwrap();
			$("#uploadBtn").hide();
			inputFileRemoved = true;
			//inputFile.replaceWith(inputFile.val("").clone(true));
			$(this).prop("checked", true);
			$("#zipUpload").prop("checked", false);
			$("#tarUpload").prop("checked", false);
			$("#submitPart").hide();
			isFileUploaded = true;
			activateSubmitBtn(isDockerChosen, isCommandInputed, isFileUploaded);
		});
		$("#submitBtn").click(function(){
			if(inputFileRemoved)
				$("#uploadBtn").remove();
		});

		//Events when midas submit button is clicked
		$("#midasSubmitBtn").click(function(){
			if(isNoPython3LibChecked)
				$("#p3Lib").remove();
			if(isNoCPlusPlusLibChecked)
				$("#cLib").remove();
			if(isNoSetupFileChecked)
				$("#setup_file_btn").remove();
			if(isAllOutputFilesChecked)
				$("#output_file_list").remove();
			if(isNoInputFilesChecked)
				$("#midas_upload_btn").remove();
		});

		//For Midas files upload
		$("#midasZipUpload").click(function(){
			$("#midasSubmitPart").show();
			$("#midasWarningMsg").hide();
			$("#midasFileLocation").text("No file chosen");
			checkingForMidas.input_file = false;
			activateMidasSubmitBtn(checkingForMidas);
			isNoInputFilesChecked = false;
		});
		$("#midasTarUpload").click(function(){
			$("#midasSubmitPart").show();
			$("#midasWarningMsg").hide();
			$("#midasFileLocation").text("No file chosen");
			checkingForMidas.input_file = false;
			activateMidasSubmitBtn(checkingForMidas);
			isNoInputFilesChecked = false;
		});
		$("#midasNoUpload").click(function(){
			$("#midasSubmitPart").hide();
			checkingForMidas.input_file = true;
			activateMidasSubmitBtn(checkingForMidas);
			isNoInputFilesChecked = true;
		});

		//For tooltip
		$('[data-toggle="tooltip"]').tooltip();
	});
</script>
<?php
page_tail();
//End of Gerald Joshua's edit
?>
