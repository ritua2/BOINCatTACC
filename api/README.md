### Notes before use

----
* Designed for large job batch submission
* Requires a token
* Test token before submitting tasks
* Server will not notify if the tasks have failed immediately
* For a file submission, use the following curl method:  
	curl -F file=@Example_multi_submit.txt http://SERVER_IP/boincserver/v2/submit_known/token=TOKEN
	