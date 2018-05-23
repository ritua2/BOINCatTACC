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
           </h4> Submit jobs via boinc2docker.</h4>
    </p>

          

    <p><br><br>
           

         <!-- Token input -->
   <form name="form" action="proc_submit.php" method="post">
          
    Token: <input type="text" name="TOK" id="TOK" value="" onkeydown="if (event.keyCode==13) {alert('ENTER key use is not allowed'); return false;}"/><br>
    Command: <input type="text" name="DERS" id="DERS" value="" onkeydown="if (event.keyCode==13) {alert('ENTER key use is not allowed'); return false;}"/>
    <br>
    <input type = "submit" value = "Submit">
   </form>

    <p><br><br>
    <p>

   Program is not designed for high API usage, for more information batch submission using RCP APIs, check the official BOINC documentation.
    </p>

  </body>
</html> 
