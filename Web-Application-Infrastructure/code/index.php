<?php
// Start session and check for password access first
session_start();

// If not authorized, show password prompt
if (!isset($_SESSION['authorized']) || !$_SESSION['authorized']) {
    // Check if the password was submitted
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['access_password'])) {
        $inputPassword = trim($_POST['access_password']);
        if ($inputPassword === "hehe you looked at the code snippit") {
            $_SESSION['authorized'] = true;
            // Redirect to avoid resubmission
            header("Location: index.php");
            exit();
        } else {
            $error = "Incorrect password!";
        }
    }
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
         <meta charset="UTF-8">
         <meta name="viewport" content="width=device-width, initial-scale=1.0">
         <title>Restricted Access</title>
         <style>
             body {
                 background: #1e3c72;
                 color: #fff;
                 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                 display: flex;
                 align-items: center;
                 justify-content: center;
                 height: 100vh;
                 margin: 0;
             }
             .password-container {
                 background: rgba(0,0,0,0.5);
                 padding: 20px;
                 border-radius: 10px;
                 text-align: center;
             }
             input[type="password"] {
                 padding: 10px;
                 width: 100%;
                 margin-top: 10px;
                 margin-bottom: 10px;
                 border: none;
                 border-radius: 5px;
             }
             button {
                 padding: 10px 20px;
                 border: none;
                 border-radius: 5px;
                 background: #00ddeb;
                 color: #fff;
                 cursor: pointer;
             }
         </style>
    </head>
    <body>
         <div class="password-container">
              <h1>Enter Password</h1>
              <?php if(isset($error)) { echo "<p style='color: red;'>$error</p>"; } ?>
              <form method="post">
                   <input type="password" name="access_password" placeholder="Enter password" required>
                   <button type="submit">Submit</button>
              </form>
         </div>
    </body>
    </html>
    <?php
    exit();
}

// ----- End password prompt -----

// Disable error display in production but log errors
ini_set('display_errors', 0);
ini_set('display_startup_errors', 0);
error_reporting(E_ALL);

// Include database configuration
require_once '/var/www/dbconfig.php';

// Create a function to connect to the database
function getDbConnection() {
    $conn = pg_connect("host=" . DB_HOST . " dbname=" . DB_NAME . " user=" . DB_USER . " password=" . DB_PASS);
    if (!$conn) {
        error_log("Failed to connect to database: " . pg_last_error());
        die("Failed to connect to database. Check logs for details.");
    }
    return $conn;
}

$conn = getDbConnection();

// Function to handle session logging
function logSession($conn) {
    $session_id = session_id();
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'];
    $query = "SELECT 1 FROM sessions WHERE session_id = $1";
    $result = pg_query_params($conn, $query, array($session_id));
    if ($result === false) {
        error_log("Session check failed: " . pg_last_error($conn));
        return;
    }
    if (pg_num_rows($result) == 0) {
        $query = "INSERT INTO sessions (session_id, ip, last_activity) VALUES ($1, $2, NOW())";
        $result = pg_query_params($conn, $query, array($session_id, $ip));
        if ($result === false) {
            error_log("Session insert failed: " . pg_last_error($conn));
        }
    } else {
        $query = "UPDATE sessions SET last_activity = NOW() WHERE session_id = $1";
        $result = pg_query_params($conn, $query, array($session_id));
        if ($result === false) {
            error_log("Session update failed: " . pg_last_error($conn));
        }
    }
}
logSession($conn);

// Process form submission using the PRG pattern
$playVideo = false;
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['name']) && isset($_POST['quota'])) {
    $name = trim(filter_input(INPUT_POST, 'name', FILTER_SANITIZE_STRING));
    $quota = trim(filter_input(INPUT_POST, 'quota', FILTER_SANITIZE_STRING));

    if ($name !== '' && $quota !== '') {
        $query = "INSERT INTO entries (name, quota) VALUES ($1, $2)";
        $result = pg_query_params($conn, $query, array($name, $quota));
        if ($result === false) {
            error_log("Insert query failed: " . pg_last_error($conn));
            echo "Failed to insert data. Check logs for details.";
        } else {
            header("Location: index.php?submitted=1");
            exit();
        }
    } else {
        error_log("Invalid form input");
    }
}

// Determine if video should play based on GET parameter
if (isset($_GET['submitted']) && $_GET['submitted'] == '1') {
    $playVideo = true;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Miku Miku Beam</title>
    <style>
        /* --- CSS remains unchanged --- */
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
        }
        .background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            overflow: hidden;
            z-index: -1;
            background: rgba(0, 0, 0, 0.7);
        }
        .background video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: none; /* Initially hidden */
        }
        .background .video-placeholder {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 24px;
            text-align: center;
            z-index: 1;
        }
        .content {
            position: relative;
            z-index: 1;
            padding: 40px;
            display: flex;
            justify-content: space-between;
            min-height: 100vh;
            align-items: flex-start;
        }
        .content-overlay {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(8px);
            padding: 30px;
            border-radius: 15px;
            width: 45%;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .list-container {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(8px);
            padding: 30px;
            border-radius: 15px;
            width: 40%;
            color: #fff;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .active-users {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(8px);
            padding: 30px;
            border-radius: 15px;
            width: 40%;
            color: #fff;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-top: 20px;
        }
        .active-users p {
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
        }
        h1, h2 {
            color: #fff;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
        }
        label {
            color: #fff;
            font-size: 16px;
            margin-bottom: 5px;
            display: block;
        }
        input, button {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        input {
            background: rgba(255, 255, 255, 0.15);
            color: #fff;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        input:focus {
            outline: none;
            background: rgba(255, 255, 255, 0.25);
            border-color: #00ddeb;
            box-shadow: 0 0 10px rgba(0, 221, 235, 0.5);
        }
        button {
            background: linear-gradient(45deg, #00ddeb, #00b4d8);
            color: #fff;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background: linear-gradient(45deg, #00b4d8, #00ddeb);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 221, 235, 0.4);
        }
        .list-container p {
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
            transition: transform 0.2s ease;
        }
        .list-container p:hover {
            transform: scale(1.02);
            background: rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body>
    <div class="background">
        <div class="video-placeholder" id="videoPlaceholder">
            Submit the form to play the video
        </div>
        <?php
        // Only load and display the video element if the form has been submitted
        if ($playVideo) {
            $videoPath = 'Wolf.mp4';
            if (file_exists($videoPath)) {
                echo '<video id="backgroundVideo" loop playsinline poster="poster.jpg">
                        <source src="' . htmlspecialchars($videoPath) . '" type="video/mp4">
                        <p style="color: red; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
                           Video failed to load. Check file or server logs.
                        </p>
                      </video>';
            } else {
                error_log("Video file not found: " . $videoPath);
                echo '<p style="color: red; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
                         Video not available.
                      </p>';
            }
        }
        ?>
    </div>
    <div class="content">
        <div class="active-users">
            <h2>Active Users</h2>
            <?php
            $timeout_minutes = 30;
            $query_count = "SELECT COUNT(*) FROM sessions WHERE last_activity > NOW() - INTERVAL '$timeout_minutes minutes'";
            $result_count = pg_query($conn, $query_count);
            if ($result_count) {
                $active_count = pg_fetch_result($result_count, 0, 0);
                echo "<p>Number of active sessions: " . htmlspecialchars($active_count) . "</p>";
            } else {
                echo "<p>Failed to count active sessions</p>";
            }
            ?>
        </div>
        <div class="content-overlay">
            <h1>Enter Your Name and Quota</h1>
            <form method="post" action="index.php" id="submissionForm">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
                <label for="quota">Quota:</label>
                <input type="text" id="quota" name="quota" required>
                <button type="submit">Submit</button>
            </form>
        </div>
        <div class="list-container">
            <h2>Entries</h2>
            <?php
            $result = pg_query($conn, "SELECT name, quota FROM entries ORDER BY id DESC");
            if ($result) {
                while ($row = pg_fetch_assoc($result)) {
                    echo "<p>Name: " . htmlspecialchars($row['name']) . ", Quota: " . htmlspecialchars($row['quota']) . "</p>";
                }
            } else {
                echo "No entries found";
            }
            ?>
        </div>
    </div>

    <script>
        // JavaScript to control video playback with better error handling.
        (function() {
            const video = document.getElementById('backgroundVideo');
            const placeholder = document.getElementById('videoPlaceholder');
            const form = document.getElementById('submissionForm');

            // Function to try playing the video if it exists
            function playBackgroundVideo() {
                if (video && video.style.display !== 'block') {
                    video.style.display = 'block';
                    placeholder.style.display = 'none';
                    video.play().catch(error => {
                        console.error("Video playback failed:", error);
                        placeholder.textContent = "Video playback failed.";
                        placeholder.style.display = 'block';
                    });
                }
            }

            // If the video element is already in the DOM (submitted), try playing it
            if (video) {
                playBackgroundVideo();
            }

            // Listen for any video errors
            if(video) {
                video.addEventListener('error', function() {
                    console.error("Error loading the video file.");
                    placeholder.textContent = "Error loading video.";
                    placeholder.style.display = 'block';
                });
            }
        })();
    </script>
</body>
</html>
<?php
// Close the database connection
pg_close($conn);
?>
