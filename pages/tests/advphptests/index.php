<?php
	print("Hello World");
	$path = "http://127.0.0.1/tests/advphptests/";
	$files = scandir($path);
	foreach ($files as &$value) {
		print "<a href='http://localhost/".$value."' target='_black' >".$value."</a><br/>";
	}
?>