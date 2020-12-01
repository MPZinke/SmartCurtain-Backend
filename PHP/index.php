<?php

include_once("$_SERVER[DOCUMENT_ROOT]/SmartCurtain/Supporting/header.php");

$fail_message = "Failed to set event";

if($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["set_curtain"]))
{
	$new_percentage_position = $_POST["position_percentage_input"];
	if(immediate_event($selected_curtain->curtain_id, $new_percentage_position))
	{
		$_SESSION["message"] = "Successfully set event";
		header("Location:index.php?curtain=$selected_curtain->curtain_id");
	}
	else
	{
		$_SESSION["message"] = "$fail_message";
		header("Location:index.php?curtain=$selected_curtain->curtain_id");
	}
}
elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["close_button"]))
{
	if(close_immediately($selected_curtain->curtain_id))
	{
		$_SESSION["message"] = "Close event set successfully";
		header("Location:index.php?curtain=$selected_curtain->curtain_id");
	}
	else
	{
		$_SESSION["message"] = "$fail_message";
		header("Location:index.php?curtain=$selected_curtain->curtain_id");
	}
}
elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["open_button"]))
{
	if(open_immediately($selected_curtain->curtain_id))
	{
		$_SESSION["message"] = "Open event set successfully";
		header("Location:index.php?curtain=$selected_curtain->curtain_id");
	}
	else
	{
		$_SESSION["message"] = "$fail_message";
		header("Location:index.php?curtain=$selected_curtain->curtain_id");
	}
}


if(!$selected_curtain->curtain_id) echo "<h1>SELECT A CURTAIN</h1>";
else
{
?>
<title>Curtain <?php if($selected_curtain()) echo $selected_curtain(); ?></title>

<h1>Set Curtain</h1>
<form method='post'>
	<input id='position_percentage_input' name='position_percentage_input' value='<?php echo intval($open_percentage); ?>' 
	class='input' type='number' min='0' max='100' style='width:25%;size:24px' 
	onchange='change_slider(this.value);' onkeyup='change_slider(this.value);'/>

	<button class='button' name='set_curtain' style='display:block; margin:auto; margin-top:20px;'>Set Curtain</button>

	<table style='padding-top:20px;width:100%;' width='100%'>
		<tr width='100%'>
			<td width='20%' align='right'>
				<button name='close_button' class='button background_color' style='background-color:inherit;'>Closed</button>
			</td>
			<td width='60%' align='middle'>
				<input id='slider_input' value='<?php echo intval($open_percentage); ?>' type='range' 
				style='width:100%' min='0' max='100'/>
			</td>
			<td width='20%' align='left'>
				<button name='open_button' class='button' style='background-color:inherit;'>Open</button>
			</td>
		</tr>
	</table>
</form>

<!-- DISPLAY -->
<div id='curtain_display' width='60%' height='50%' style='margin:auto;'>
	<?php 
		$gradient_left_side = intval((100 - $open_percentage) / 2);
		$gradient_right_side = $gradient_left_side + $open_percentage;
		$gradient = "to right, #222222, #222222 $gradient_left_side%, 
						#$combined_color $gradient_left_side%, #$combined_color $gradient_right_side%, 
						#222222 $gradient_right_side%";
	?>
	<div id='slider_light' style='width:60%; height: 50%; margin:auto; border-radius: 5px;
	background-image:linear-gradient(<?php echo $gradient; ?>)'> </div>
</div>


<script>
	// ——————————————— CURTAIN DISPLAY ———————————————

	function create_gradient(open_percentage) {
		var color = `#<?php echo $time_of_day_color; ?>${Math.floor(open_percentage * 255 / 100).toString(16)}`;
		var left = Math.floor((100 - open_percentage) / 2);
		var right = open_percentage + left;
		return `linear-gradient(to right, #222222,` + 
				`#222222 ${left}%, ${color} ${left}%, ` + 
				` ${color} ${right}%, #222222 ${right}%)`;
	}

	function set_slider_light(percentage) {
		percentage = Math.min(percentage, 100);  // prevent width from going over 100
		var slider_light = document.getElementById("slider_light");
		document.getElementById("slider_light").style.backgroundImage = create_gradient(percentage);
	}

	function change_slider(value) {
		document.getElementById("slider_input").value = value;
		set_slider_light(value);
	}

	// Update the current slider value (each time you drag the slider handle)
	document.getElementById("slider_input").oninput = function() {
		document.getElementById("position_percentage_input").value = this.value;
		set_slider_light(this.value);
	}


</script>

<?php 
}


include_once("$_SERVER[DOCUMENT_ROOT]/SmartCurtain/Supporting/footer.php");
?>
