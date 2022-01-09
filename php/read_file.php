<?php 
$myfile = fopen("{RFILE}", "r") or die("Unable to open file!");
echo fread($myfile, filesize("{RFILE}"));
fclose($myfile);
?>