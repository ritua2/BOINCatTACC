<!DOCTYPE html>

 <html>
  <head>
    <title>Submit BOINC jobs</title>
  </head>

  <body>


    <style>
     div {
         background-color: DodgerBlue;
         width: 350px;
         padding: 25px;
         margin: 25px;
      }
      </style>

      <div>
      <h3>Interactive BOINC web interface</h3>
    </div>

    <p>
      </h4>Submit jobs via boinc2docker.</h4>
    </p>
          

    <p><br><br>
    WARNING: Do not press ENTER until all fields have been completed.
           

         <!-- Token input -->
   <form name="form" action="proc_submit.php" method="post">
   <p>Enter token: </p>
   <input type="text" name="TOK" id="TOK" value="">
   </form>

   <!-- Command input -->
   <form name="form" action="proc_submit.php" method="post">
   <p>Enter the command without bin/boinc2docker_create_work.py: </p>
   <input type="text" name="DERS" id="DERS" value="">
   </form>
   
   <p><br><br>
   <p>

   Program is not designed for high API usage, for more information batch submission using RCP APIs, check the official BOINC documentation.
   </p>


  </body>
</html> 
