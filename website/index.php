<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Display</title>

    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #1f1f1f;
            color: #ffffff;
        }

        #taskbar {
            background-color: #333333;
            padding: 10px;
            border-radius: 15px 15px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        #logo {
            width: 40px; /* Adjust the logo width */
            height: auto;
        }

        #goBackButton {
            cursor: pointer;
            background-color: #0073e6; /* Button background color */
            color: #ffffff;
            padding: 8px 12px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
        }

        h2 {
            color: #00bfff;
            margin-top: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            color: #ffffff;
        }

        th, td {
            border: 1px solid #00bfff;
            padding: 8px;
            text-align: left;
        }

        tr:nth-child(even) {
            background-color: #333333;
        }

        tr:nth-child(odd) {
            background-color: #1f1f1f;
        }

        .audioPlayer {
            display: none;
        }
    </style>
</head>
<body>
    <div id="taskbar">
        <img id="logo" src="happy_heads_logo-removebg.png" alt="Logo"> <!-- Replace "your_logo.png" with the actual path to your logo -->
        <a href="C:\Users\braje\language_detection\website\frontend\index_1.html"><button id="goBackButton" onclick="goBack()">Go Back</button></a>
    </div>


    
    <?php
        // Database connection parameters
        $servername = "localhost";
        $username = "root";
        $password = "Anushka@123";
        $database = "foul_db";

        // Create connection
        $conn = new mysqli($servername, $username, $password, $database);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        // Fetch data from the natural join of 'students' and 'Defaulters_list'
        $joinQuery = "SELECT students.id, students.name, Defaulters_list.audio, Defaulters_list.fine 
                      FROM students
                      NATURAL JOIN Defaulters_list";

        $joinResult = $conn->query($joinQuery);

        if ($joinResult->num_rows > 0) {
            echo "<h2>Students Defaulters List</h2>";
            echo "<table border='1'>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Audio</th>
                        <th>Fine</th>
                        <th>Action</th>
                    </tr>";

            while ($row = $joinResult->fetch_assoc()) {
                echo "<tr>
                        <td>{$row['id']}</td>
                        <td>{$row['name']}</td>
                        <td>{$row['audio']}</td>
                        <td>{$row['fine']}</td>
                        <td><button onclick=\"playAudio('{$row['audio']}')\">Play Audio</button></td>
                      </tr>";
            }

            echo "</table>";
        } else {
            echo "No records found ";
        }

        // Close the database connection
        $conn->close();
    ?>

<div class="audioPlayer" id="audioPlayer">
        <audio controls id="audioControl">
            Your browser does not support the audio element.
        </audio>
    </div>

    <script>
        function goBack() {
            // You can implement the logic to go back to the homepage here
            alert("Going back to homepage!");
        }

        function playAudio(audioPath) {
            var audioControl = document.getElementById('audioControl');
            var audioPlayer = document.getElementById('audioPlayer');
            
            // Set the audio source
            audioControl.src = audioPath;

            // Show the audio player
            audioPlayer.style.display = 'block';

            // Pause and reload the audio to ensure it starts from the beginning
            audioControl.pause();
            audioControl.load();

            // Play the audio
            audioControl.play();
        }
    </script>
</body>
</html>