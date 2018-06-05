### Notes before use

----
* Designed for large job batch submission
* Requires a token
* Test token before submitting tasks
* Server will not notify if the tasks have failed immediately
* For a file submission, use the following curl method:  
	*curl -F file=@Example_multi_submit.txt http://SERVER_IP:5075/boincserver/v2/submit_known/token=TOKEN*  


### Coral2 Storage

----

* Designed to save files for future BOINC jobs, so that they may be called through wget or curl  
* Each individual user will receive a unique, personal sandbox assigned to their token  
* Users must create a directory before using it, use the following syntax:  
	*curl -d token=TOKEN  http://SERVER_IP/boincserver/v2/create_sandbox*  
* Users may not have more than one directory
