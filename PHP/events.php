<?php

include_once($_SERVER['DOCUMENT_ROOT'].'/SmartCurtain/Supporting/header.php');

if($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["position_percentage_input"]))
{
	$time = str_replace("T", " ", $_POST["time_input"]);
	$position = $_POST["position_percentage_input"];

	if(new_future_event($selected_curtain, $position, $time))
	{
		$_SESSION["message"] = "Successfully created event";
		header("Location:events.php?curtain=$selected_curtain->curtain_id");
	}
	else
	{
		$_SESSION["message"] = "Failed to create event";
		header("Location:events.php?curtain=$selected_curtain->curtain_id");
	}
}

?>
<title>Events <?php if($selected_curtain()) echo "Curtain ".$selected_curtain(); ?></title>

<h1>Events</h1>

<?php if(!isset($_GET["event"])) { ?>
	<button onclick='collapse_expand_div(this, "#create_event_div", "Create Event", null);' class='button'>Create Event</button>
	<form id='set_future_event' name='set_future_event' method='post'>
		<div id='create_event_div' hidden>
			<!-- <h3>Time</h3> -->
			<input name='time_input' type='datetime-local' value='<?php echo date("Y-m-d\TH:i");?>'
			class='input' style='margin:8px;'>
			<!-- <h3>Position</h3> -->
			<input id='position_percentage_input' name='position_percentage_input' type='number' 
			max='100' min='0' class='input' value='<?php echo intval($open_percentage); ?>' style='margin:8px;'
			onchange='change_slider(this.value);' onkeyup='change_slider(this.value);'>

			<table style='padding-top:20px;width:100%;' width='100%'>
				<tr width='100%'>
					<td width='20%' align='right'>
						<button name='close_button' class='button' type='button' 
						style='background-color:inherit;' onclick='set_slider_and_input(0);'>Closed</button>
					</td>
					<td width='60%' align='middle'>
						<input id='slider_input' value='<?php echo intval($open_percentage); ?>' type='range' 
						style='width:100%' min='0' max='100'/>
					</td>
					<td width='20%' align='left'>
						<button name='open_button' class='button' type='button'
						style='background-color:inherit;' onclick='set_slider_and_input(100);'>Open</button>
					</td>
				</tr>
			</table>

			<!-- DISPLAY -->
			<?php 
			$gradient_left_side = intval((100 - $open_percentage) / 2);
			$gradient_right_side = $gradient_left_side + $open_percentage;
			$gradient = "to right, #222222, #222222 $gradient_left_side%, 
							#$combined_color $gradient_left_side%, #$combined_color $gradient_right_side%, 
							#222222 $gradient_right_side%";
			?>
			<div id='slider_light' style='width:60%; height: 50%; margin:auto; border-radius: 5px;
			background-image:linear-gradient(<?php echo $gradient; ?>)'
			onclick='post_value("set_future_event")'> </div>
		</div>
	</form>
<?php } ?>

<table class='table alternate'>
	<thead>
		<th width='25%' style='align:left;'> Event Time </th>
		<th width='50%' style='align:left;'> Event Position </th>
		<th width='25%' style='align:left;'>  </th>
	</thead>
<?php
	foreach($selected_curtain->events as $event)
	{
		$gradient_left_side = intval((100 - $event->event_percentage) / 2);
		$gradient_right_side = $gradient_left_side + $event->event_percentage;
		$gradient = "to right, #0000FF, #0000FF $gradient_left_side%, 
						#FFFFAA $gradient_left_side%, #FFFFAA $gradient_right_side%, 
						#0000FF $gradient_right_side%";
		if($_GET["event"] == $event->event_id)
		{
			$background_color = "#000000";
			$disabled = "";
			$position_td = "<div id='gradient-$event->event_id' style='height:100%; width: 100%; 
							border-radius: 5px; background-image:linear-gradient($gradient);'>
								<input id='slider_input' name='position-$event->event_id' type='range'
								style='background-color:#AAAA00; margin:auto; width:100%; vertical-align:middle;'
								value='$event->event_percentage'>
							</div>";
			$tr_color = "style='background-color: rgb(100,255,100,.5);'";
		}
		else
		{
			$disabled = "disabled";
			$background_color = "var(--background_color)";
			$position_td = "<div id='gradient-$event->event_id' style='height:100%; width:100%; 
					border-radius: 5px; background-image:linear-gradient($gradient);'></div>";
			$tr_color = "";
		}
		echo 	"<tr $tr_color>
					<td>
						<input name='time-$event->event_id' type='datetime-local' class='input dark' 
						value='".str_replace(' ', 'T', substr($event->event_time, 0, 16))."'
						style='background-color: $background_color; color: #FFFFFF;' $disabled> 
					</td>
					<td> $position_td </td>
					<td onclick='edit($event->event_id)'> Edit </td>
				</tr>";
	}
?>
</table>

<?php
include_once("$_SERVER[DOCUMENT_ROOT]/Supporting/footer.php");
?>

<script>
	function post_value(form) {
		document.getElementById(form).submit();
	}



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


	function set_slider_and_input(value) {
		document.getElementById("position_percentage_input").value = value;
		document.getElementById("slider_input").value = value;
		set_slider_light(Math.max(value, 7));
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