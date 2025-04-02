<?php
// this is added in the www to prevent acess to it plus it's recommended to use the enviromental variables instead of hardcoding the creds
// Alternative secure connection using environment variables
$host = getenv('DB_HOST') ?: 'Database end point';
$dbname = getenv('DB_NAME') ?: 'Name';
$user = getenv('DB_USER') ?: 'User';
$pass = getenv('DB_PASS') ?: 'yourpassword';  // Replace or use env vars
$conn = pg_connect("host=$host dbname=$dbname user=$user password=$pass");
if (!$conn) {
    die("Oops! Couldn’t connect to the database.");
}
?>