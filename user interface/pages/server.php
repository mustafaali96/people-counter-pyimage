<?php
	
	session_start();

	// Connect to database
	$servername = "localhost";
	$username = "root";
	$password = "";
	$dbname = "peoplecounter";

	// Create connection
	$conn = new mysqli($servername, $username, $password, $dbname);
	// Check connection
	if ($conn->connect_error) {
	  die("Connection failed: " . $conn->connect_error);
	}
	
	// If Login button is clicked
	if (isset($_POST['logged'])) {
		echo('Welcome');
		$username = $_POST['username'];
		$pwd = $_POST['password'];

		// $query = "INSERT INTO people (name, country, phone) VALUES ('$name', '$country', '$phone')";
		

		// $rec = mysqli_query($db, "SELECT is_admin FROM login WHERE username = $username AND password = $pwd");
		// $record = mysqli_fetch_array($rec);
		// $name = $record['is_admin'];
		
		$result = $conn->query("SELECT * FROM login WHERE username = '$username' AND password = '$pwd'");

		if ($result) {
			$row = $result->fetch_assoc();
		    $location = 'location: indexUser.html';
		    if ($row["is_admin"] == 1) {
		    	$location = 'location: index.html';
		    }
		    header($location);

		} else {
		  header('location: pages/login.html');
		}


		// header('location: index.html'); // redirect to index page after inserting th data
	}

	// // update records
	// if (isset($_POST['update'])) {
	// 	$name = ($_POST['name']);
	// 	$country = ($_POST['country']);
	// 	$phone = ($_POST['phone']);
	// 	$id = ($_POST['id']);
		 

	// 	mysqli_query($db, "UPDATE people SET name='$name', country='$country', phone='$phone' WHERE id='$id' ");

	// 	$_SESSION['msg'] = "Data updated successfully!";
	// 	header('location: index.php');

	// }

	// // delete records
	// if (isset($_GET['del'])) {
	// 	$id = $_GET['del'];
	// 	mysqli_query($db, "DELETE FROM people WHERE id=$id");
	// 	$_SESSION['msg'] = "Data deleted successfully!";
	// 	header('location: index.php');


	// }

	// retrieve records
	// $results = mysqli_query($db, "SELECT * FROM people");


?>