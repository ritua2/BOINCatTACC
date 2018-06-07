### Notes before use

----
* Designed for large job batch submission
* Requires a token
* Test token before submitting tasks
* Server will not notify if the tasks have failed immediately
* For a job file submission, use the following curl method:  
	*curl -F file=@Example_multi_submit.txt http://SERVER_IP:5075/boincserver/v2/submit_known/token=TOKEN*  


### Reef Storage

----

* Designed to save files for future BOINC jobs, so that they may be called through wget or curl  
* Each individual user will receive a unique, personal sandbox assigned to their token  
* Users must create a directory before using it, use the following syntax:  
	*curl -d token=TOKEN  http://SERVER_IP:5060/boincserver/v2/create_sandbox*  
* Users may not have more than one directory
* Check all user files using the following syntax (files will be comma-separated):  
	*curl http://SERVER_IP:5060/boincserver/v2/all_files/token=TOKEN*
* Upload a file using the syntax:  
	*curl -F file=@FILE.txt http://SERVER_IP:5060/boincserver/v2/upload_reef/token=TOKEN*
* Delete a file using the syntax:
	*curl -d del=FILE_NAME  http://SERVER_IP:5060/boincserver/v2/delete_file/token=TOKEN*
* Download a file using curl/wget with the syntax:  
	*curl http://SERVER_IP:5060/boincserver/v2/reef/TOKEN/FILE_NAME*



**Summary**  
Using Reef, it is now possible to:  
	- Upload files to the cloud, favoring integration with local file systems  
	- Delete files when they are no longer useful
	- Maintain a sandbox of data for future BOINC projects
