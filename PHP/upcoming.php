<?php
	/***************************************************
	*
	*	-Main page of local portal to curtains
	*	-View & remove upcoming scheduled events
	*
	***************************************************/

	include_once ($_SERVER['DOCUMENT_ROOT'].'/dependencies/header.php');

	$events = get_future_events();

	if($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['delete_button'])) {
		// remove_events(.) returns number of while deleting any event
		remove_events(filter_input(INPUT_POST, 'times_to_delete'));
		if($failures > 0) {
			echo '<script>'.
					'alert("Failed to remove '.$failures.' of the selected events");'.
					'window.location.href = "upcoming.php";'.
				'</script>';
		}
		else {
			echo '<script>'.
					'alert("Successfully removed all selected events");'.
					'window.location.href = "upcoming.php";'.
				'</script>';
		}
	}

	{ ?>
	<div id='future_events_title' class='title'> 
		<h1>Upcoming Actions</h1>
	</div>
	<div>
		<table class='table'>
			<thead>
				<td> Action </td>
				<td> Day </td>
				<td> Time </td>
			</thead>
			<?php
			if($events) {
				foreach($events as $event) {
					echo "<tr> <td> <input type='checkbox' onclick='incld_val(\"$event[event_time]\")' class='cb left' hidden/>".get_state_string($event['event_action'])."</td> ".
					"<td>".get_day($event['event_time'])."</td> ".
					"<td>".date('H:i', strtotime($event['event_time']))."</td> </tr>";
				}
			} 
			else {
				echo"<tr> <td>NO DATA AVAILABLE</td> </td>"; 
			} ?>
		</table>
	</div>
	<div id='state_refresh' hidden>
		<form method='POST'>
			<button name='delete_button' class='button button-danger'>DELETE</button>
			<input name='times_to_delete' id='times_to_delete' value='' hidden/>
		</form>
	</div>


	<script>
		// shade table rows
		var rows = document.getElementsByTagName('tr');
		for(var x = 1; x < rows.length; x++) {
			if(rows[x].getElementsByTagName('td')[0].innerHTML.includes('Open')) rows[x].className = 'open';
			else {rows[x].className = 'close';}
		}

		// insert delete button
		var button = " <button id='select_button' class='button right' onclick='show_options(this)'>Select</button>"; 
		var header = document.getElementsByClassName('header')[0];
		header.innerHTML += button;

		function show_options(btn) {
			if(btn.innerHTML == "Select") {
				btn.innerHTML = "Cancel";
				btn.className = 'button button-cancel right';
				$(".cb, #state_refresh").show();
			}
			else {
				btn.innerHTML = "Select";
				btn.className = 'button right';
				$(".cb, #state_refresh").hide();
			}
		}

		function incld_val(time) {
			var times_input = document.getElementById('times_to_delete');
			var input_value = times_input.value;
			if(input_value.includes(time)) {
				var times = input_value.split("|");
				times.splice(times.indexOf(time), 1);
				input_value = times.join('|');
			}
			else { 
				if(input_value.length > 0) input_value += '|';
				input_value += time;
			}
			times_input.value = input_value;
		}
	</script>

<?php }
	include_once ($_SERVER['DOCUMENT_ROOT'].'/dependencies/footer.php');
	/* created by: MPZinke on 01.10.19 */
?>