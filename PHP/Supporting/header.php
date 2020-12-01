<?php
	/***************************************************
	*
	*	-Included with every web-portal doc as redundant
	*	 import of dependencies & menu
	*
	***************************************************/

	session_start();
	date_default_timezone_set("America/Chicago");

	// ———— load page info ————
	include_once("$_SERVER[DOCUMENT_ROOT]/SmartCurtain/Connections/DBConnect.php");
	include_once("$_SERVER[DOCUMENT_ROOT]/SmartCurtain/Connections/DBFunctions.php");
	include_once("$_SERVER[DOCUMENT_ROOT]/SmartCurtain/Supporting/Curtain.php");
	include_once("$_SERVER[DOCUMENT_ROOT]/SmartCurtain/Supporting/Event.php");

	if(isset($_SESSION["message"]))
	{
		echo "<script> window.onload = function() 
					{ alert('$_SESSION[message]'); };</script>";
		unset($_SESSION["message"]);
	}

	// ———— load curtain info ————
	$curtains = all_curtains();

	if(filter_input(INPUT_GET, 'curtain')) $selected_curtain = new Curtain($_GET["curtain"]);
	elseif(count($curtains)) $selected_curtain = $curtains[0];
	else $selected_curtain = new Curtain(0);

	// curtain display info
	if($selected_curtain->curtain_id)
	{
		// decimal light of day hex
		$time_of_day_colors = array(	'0000', '1515', '2a2a', '3f3f', '5555', '6a6a', '7f7f', '9494',
										'aaaa', 'bfbf', 'd4d4', 'e9e9', 'ffff', 'e9e9', 'd4d4', 'bfbf',
										'aaaa', '9494', '7f7f', '6a6a', '5555', '3f3f', '2a2a', '0000');
		$time_of_day_color = $time_of_day_colors[date("G")];

		$open_percentage = $selected_curtain->current_state_percentage();
		$open_color = dechex(intval($selected_curtain->current_state_percentage() * 255 / 100));
		$combined_color = $time_of_day_color.$open_color;
	}
	else
	{
		$open_percentage = 100;
		$time_of_day_color = "FF00";
		$open_color = "00";
		$combined_color = $time_of_day_color.$open_color;
	}

?>
	<html>
		<head>
			<link rel="icon" href="<?php echo "http://$_SERVER[HTTP_HOST]/SmartCurtain/Media/icon.png"; ?>">
			<meta name="viewport" content="width=device-width,initial-scale=1">
			<meta name="theme-color" content="#555556"/>
			<link rel="stylesheet" type="text/css" href="<?php echo "http://$_SERVER[HTTP_HOST]/SmartCurtain/Supporting/style.css"; ?>"/>
			<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
		</head>
		<header class='header'>
			<table style='width:100%;'>
				<tr style='width:100%;'>
					<td style='width:20%'>
						<span style="font-size:30px;cursor:pointer;" onclick="openNav()" class="header">&nbsp; &#9776;</span>
					</td>
					<td style='width:60%;margin:auto'>
						<select id='curtain_select' name='curtain_select' class='select dark' onchange='redirect_to_curtain(this);'>
							<?php
								foreach($curtains as $curtain)
								{
									if($selected_curtain() == $curtain->curtain_id)
										echo "<option selected value='$curtain->curtain_id'>$curtain->curtain_name</option>";
									else
										echo "<option value='$curtain->curtain_id'>$curtain->curtain_name</option>";
								}
							?>
						</select>
					</td>
					<td style='width:20%';>
					</td>
				</tr>
				<tr>
					<td colspan='3' align='middle'>
						<div id='current_light' style='background-image: linear-gradient(90deg, 
									#<?php echo $combined_color; ?>, 
									#<?php echo "$time_of_day_color"; ?>00, 
									#<?php echo $combined_color; ?>);
									height:8px;
									width:<?php echo $open_percentage; ?>%;'>
						</div>
					</td>
				</tr>
			</table>
		</header>
		<body class='body'>
			<div id="sideMenu">
				<?php $curtain_get_method = $_GET["curtain"] ? "?curtain=$_GET[curtain]" : "" ?>
				<a href="javascript:void(0)" class="closebtn" onclick="closeNav()" style="position:relative;left:75%;">&times;</a>
				<a href="./index.php<?php echo $curtain_get_method; ?>" onclick="closeNav()">Set Curtain</a>
				<a href="./events.php<?php echo $curtain_get_method; ?>" onclick="closeNav()">Create Event</a>
				<a href="./edit.php<?php echo $curtain_get_method; ?>" onclick="closeNav()">Edit Curtain Details</a>
			</div>
