<?php

/***********************************************************************************************************
*
*	created by: MPZinke
*	on ..
*
*	DESCRIPTION: TEMPLATE
*	BUGS:
*	FUTURE:
*
***********************************************************************************************************/


// —————————————— ADD CURTAIN CHANGE ———————————————

function close_immediately($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$mysqli->query(	"INSERT INTO `events` (`curtain_id`, `event_position`, `event_activated`)
						VALUES ('$curtain_id', '0', FALSE);");
	return $mysqli->commit();
}


function immediate_event($curtain_id, $position_percentage)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	// get open position
	$query = "SELECT `curtain_length` FROM `curtains` 
				WHERE `curtain_id` = $curtain_id;";

	$results = $mysqli->query(	"SELECT `curtain_length` FROM `curtains` 
									WHERE `curtain_id` = $curtain_id;");
	if(!$results) return false;
	$max = $results->fetch_assoc()["curtain_length"];
	if(!$max) return false;

	// add event for now to DB
	$position = intval($position_percentage * $max / 100);
	$mysqli->query(	"INSERT INTO `events` (`curtain_id`, `event_position`, `event_activated`)
						VALUES ('$curtain_id', '$position', FALSE);");
	return $mysqli->commit();
}


function new_future_event($curtain, $position_percentage, $time)
{
	if(!is_object($curtain) || !$curtain->curtain_id) return false;

	global $mysqli;
	// get open position
	$results = $mysqli->query(	"SELECT `curtain_length` FROM `curtains` 
									WHERE `curtain_id` = $curtain->curtain_id;");
	if(!$results) return false;
	$max = $results->fetch_assoc()["curtain_length"];

	// add event for now to DB
	$position = intval($position_percentage * $max / 100);
	$mysqli->query(	"INSERT INTO `events` (`curtain_id`, `event_position`, `event_activated`, `event_time`)
						VALUES ($curtain->curtain_id, $position, FALSE, '$time');");
	return $mysqli->commit();
}


function open_immediately($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;

	// get open position
	$results = $mysqli->query(	"SELECT `curtain_length` FROM `curtains` 
									WHERE `curtain_id` = $curtain_id;");
	if(!$results) return false;
	$max = $results->fetch_assoc()["curtain_length"];

	$mysqli->query(	"INSERT INTO `events` (`curtain_id`, `event_position`, `event_activated`)
						VALUES ($curtain_id, $max, FALSE);");
	return $mysqli->commit();
}


// ————————————————— GETTERS ——————————————————

function all_curtains()
{
	global $mysqli;

	$results = $mysqli->query(	"SELECT `curtain_id`, `curtain_name` FROM `curtains`;");
	if(!$results) return array();

	$curtains = array();
	while($row = $results->fetch_assoc()) $curtains[] = new Curtain($row["curtain_id"]);
	return $curtains;
}


function all_mobile_data()
{
	global $mysqli;

	$details = curtain_details();
	$new_events = upcoming_events();
	$past_events = past_events();

	return array("details" => $details, "events" => $new_events, "past" => $past_events);
}


function auto_calibration_option($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$results = $mysqli->query(	"SELECT `auto_calibration`
									FROM `options`
									WHERE `curtain_id` = $curtain_id;");
	if(!$results) return false;

	return intval($results->fetch_assoc()["auto_calibration"]);
}


function auto_correct_option($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$results = $mysqli->query(	"SELECT `auto_correct`
									FROM `options`
									WHERE `curtain_id` = $curtain_id;");
	if(!$results) return false;

	return intval($results->fetch_assoc()["auto_correct"]);
}


function curtain_details($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$results = $mysqli->query(	"SELECT *
									FROM `curtains`
									WHERE `curtain_id` = $curtain_id;");
	if(!$results) return false;

	return $results->fetch_assoc();
}


function get_activation_and_percentage_position($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$results = $mysqli->query(	"SELECT `curtain_activated`, `curtain_length`, `curtain_position`
									FROM `curtains`
									WHERE `curtain_id` = $curtain_id;");
	if(!$results) return false;

	$results = $results->fetch_assoc();
	return array(	"curtain_activated" => $results["curtain_activated"],
					"curtain_percent_position" => intval($results["curtain_position"] / $results["curtain_length"] * 100));
}


function get_curtain_activated($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	return $mysqli->query(	"SELECT `curtain_activated` FROM `curtains`
								WHERE `curtain_id` = $curtain_id;");
}


function get_curtain_position($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	return $mysqli->query(	"SELECT `curtain_position` FROM `curtains`
								WHERE `curtain_id` = $curtain_id;");
}


function get_most_recent_event($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$results = $mysqli->query(	"SELECT *
									FROM `events`
									WHERE `event_activated` = FALSE
									AND `curtain_id` = $curtain_id
									ORDER BY `event_time` DESC;");
	if(!$results) return false;

	return $results->fetch_assoc();
}


function past_events($count=25, $begin=null)
{
	global $mysqli;
	if($begin)
		$results = $mysqli->query(	"SELECT *
										FROM `events`
										WHERE `event_time` < CURRENT_TIMESTAMP
										ORDER BY `event_time` DESC
										LIMIT $count;");
	else
		$results = $mysqli->query(	"SELECT *
										FROM `events`
										WHERE `event_time` < CURRENT_TIMESTAMP
										AND '$begin' < `event_time`
										ORDER BY `event_time` DESC
										LIMIT $count;");

	if(!$results) return false;
	$past_events = array();
	while($row = $results->fetch_assoc()) $past_events[] = $row;

	return $past_events;
}


function pending_events()
{
	global $mysqli;
	$two_minutes_ago = strtotime("-2 minutes");
	$results = $mysqli->query(	"SELECT * FROM `events`
									WHERE `event_activated` = FALSE
									AND `event_time` < '$two_minutes_ago'
									ORDER BY `event_time` DESC;");
	if(!$results) return true;  // error in query or $mysqli; assume worst case of pending events
	return $results->num_rows;
}


function upcoming_events()
{
	global $mysqli;
	$results = $mysqli->query(	"SELECT * FROM `events`
									WHERE `event_activated` = FALSE
									ORDER BY `event_time` DESC;");
	if(!$results) return false;

	$events = array();
	while($row = $results->fetch_assoc()) $events[] = $row;

	return $events;
}


// ————————————————— SETTERS ———————————————————
// —————————————————————————————————————————

// ————————————————— EVENTS ———————————————————

function curtain_for_event($event_id)
{
	if(!$event_id || !is_numeric($event_id)) return 0;

	global $mysqli;
	$results = $mysqli->query(	"SELECT `curtain_id` FROM `events`
									WHERE `event_id` = $event_id;");

	if(!$results || !$results->num_rows) return 0;
	return $results->fetch_assoc()["curtain_id"];
}


function delete_event($event_id)
{
	if(!$event_id || !is_numeric($event_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `events` SET `event_activated` = TRUE
						WHERE `event_id` = $event_id;");
	return $mysqli->commit();
}


function edit_event_position($event_id, $position)
{
	if(!$event_id || !is_numeric($event_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `events` SET `event_position` = $position
						WHERE `event_id` = $event_id;");
	return $mysqli->commit();
}


function edit_event_time($event_id, $time)
{
	if(!$event_id || !is_numeric($event_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `events` SET `` = ''
						WHERE `event_id` = $event_id;");
	return $mysqli->commit();
}


function set_all_events_for_curtain_as_activated($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `events` SET `event_activated` = TRUE
						WHERE `curtain_id` = $curtain_id;");
	return $mysqli->commit();
}


function set_event_as_activated($event_id)
{
	if(!$event_id || !is_numeric($event_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `events` SET `event_activated` = TRUE
						WHERE `event_id` = $event_id;");
	return boolval($mysqli->affected_rows);
}


// ————————————————— CURTAIN ———————————————————


function reset_curtain_length($curtain_id, $curtain_length)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `curtains` SET `curtain_length` = '$curtain_length'
						WHERE `curtain_id` = $curtain_id;");
	return $mysqli->commit();
}


function set_curtain_activated_state($curtain_id, $curtain_activated)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `curtains` SET `curtain_activated` = '$curtain_activated'
						WHERE `curtain_id` = $curtain_id;");
	return $mysqli->commit();
}


function set_curtain_as_checked($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `curtains` SET `curtain_last_connection` = CURRENT_TIMESTAMP
						WHERE `curtain_id` = $curtain_id;");
	return $mysqli->commit();
}


function set_curtain_as_closed($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `curtains` SET `curtain_position` = '0'
						WHERE `curtain_id` = $curtain_id;");
	return $mysqli->commit();
}


function set_curtain_as_partially_open($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	// check if position is set as open/close
	$results = $mysqli->query(	"SELECT `curtain_position` = `curtain_length` AS `open`,
									`curtain_position` = '0' AS `closed`
									FROM `curtains`
									WHERE `curtain_id` = $curtain_id;");
	if(!$results) return false;

	$results = $results->fetch_assoc();
	if($results["open"] || $results["closed"])
	{
		// default to half way open
		$mysqli->query(	"UPDATE `curtains` SET `curtain_position` = `curtain_length` / 2
							WHERE `curtain_id` = $curtain_id;");
		return $mysqli->commit();
	}
	return true;
}


function set_curtain_as_open($curtain_id)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `curtains` SET `curtain_position` = `curtain_length`
						WHERE `curtain_id` = $curtain_id;");
	return $mysqli->commit();
}


function set_curtain_position($curtain_id, $position)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `curtains` SET `curtain_position` = '$position'
						WHERE `curtain_id` = $curtain_id;");
	return $mysqli->commit();
}




function set_curtain_position_from_event($event_id)
{
	if(!$event_id || !is_numeric($event_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `curtains`
						INNER JOIN `events` 
						ON `events`.`curtain_id` = `curtains`.`curtain_id`
						SET `curtains`.`curtain_position` = `events`.`event_position` 
						WHERE `events`.`event_id` = $event_id;");
	return $mysqli->commit();
}


function set_DB_direction($curtain_id, $direction)
{
	if(!$curtain_id || !is_numeric($curtain_id)) return false;

	global $mysqli;
	$mysqli->query(	"UPDATE `curtains` SET `curtain_direction` = '$direction'
						WHERE `curtain_id` = $curtain_id;");
	return $mysqli->commit();
}

?>