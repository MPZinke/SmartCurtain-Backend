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


include_once($_SERVER['DOCUMENT_ROOT']."/SmartCurtain/Connections/DBConnect.php");
include_once($_SERVER['DOCUMENT_ROOT']."/SmartCurtain/Connections/DBFunctions.php");


// ————————————————— SLAVES ———————————————————
// ————————————————————————————————————————

// ———— GET ————

if($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["auto_calibration_option"]))
{
	$curtain = $_POST["auto_calibration_option"];
	$details = auto_calibration_option($curtain);
	echo json_encode(array("auto_calibration" => $details));
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["auto_correct_option"]))
{
	$curtain = $_POST["auto_correct_option"];
	$details = auto_correct_option($curtain);
	echo json_encode(array("auto_correct" => $details));
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["get_min_curtain_details"]))
{
	$curtain = $_POST["get_min_curtain_details"];
	$details = curtain_details($curtain);
	if(set_curtain_as_checked($curtain) && $details)
		echo json_encode(array(
		"curtain_direction" => intval($details["curtain_direction"]),
		"curtain_length" => intval($details["curtain_length"]),
		"curtain_position" => intval($details["curtain_position"])));
	else echo json_encode(array(
		"curtain_direction" => 0,
		"curtain_length" => 0,
		"curtain_position" => 0));
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["get_most_recent_event"]))
{
	$curtain = $_POST["get_most_recent_event"];
	$details = get_most_recent_event($curtain);
	if(set_curtain_as_checked($curtain) && $details)
		echo json_encode(array(
		"event_id" => intval($details["event_id"]),
		"event_position" => intval($details["event_position"])));
	else echo json_encode(array(
		"event_id" => 0,
		"event_position" => 0));
}


// ———— SET ————
elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["reset_curtain_length"]))
{
	$curtain = $_POST["reset_curtain_length"];
	$new_length = $_POST["new_length"];
	if(reset_curtain_length($curtain, $new_length)) echo_success("reset_curtain_length");
	else echo_failed("reset_curtain_length");
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["set_curtain_as_closed"]))
{
	$curtain = $_POST["set_curtain_as_closed"];
	if(set_curtain_as_closed($curtain)) echo_success("set_curtain_as_closed");
	else echo_failed("set_curtain_as_closed");
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["set_curtain_activated_state"]))
{
	$curtain = $_POST["set_curtain_activated_state"];
	$activation_state = $_POST["activation_state"];
	if(set_curtain_activated_state($curtain, $activation_state)) echo_success("set_curtain_activated_state");
	else echo_failed("set_curtain_activated_state");
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["set_curtain_as_open"]))
{
	$curtain = $_POST["set_curtain_as_open"];
	if(set_curtain_as_open($curtain)) echo_success("set_curtain_as_open");
	else echo_failed("set_curtain_as_open");
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["set_curtain_as_partially_open"]))
{
	$curtain = $_POST["set_curtain_as_partially_open"];
	if(set_curtain_as_partially_open($curtain)) echo_success("set_curtain_as_partially_open");
	else echo_failed("set_curtain_as_partially_open");
}


elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["set_event_as_activated"]))
{
	$event_id = $_POST["set_event_as_activated"];
	if(!set_event_as_activated($event_id))
		echo_failed("set_event_as_activated");
	if(!set_all_events_for_curtain_as_activated(curtain_for_event($event_id)))
		echo_failed("set_all_events_for_curtain_as_activated");
	if(!set_curtain_position_from_event($event_id))
		echo_failed("set_curtain_position_from_event");
	else echo_success();
}

// —————————————————— APP ————————————————————
// ————————————————————————————————————————

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["get_all_curtain_details"]))
{
	$curtain = $_POST["get_all_curtain_details"];
	$details = curtain_details($curtain);
	if(!$details) echo_failed();
	else echo json_encode(array(	"curtain_activated" => intval($details["curtain_activated"]),
									"curtain_direction" => intval($details["curtain_direction"]),
									"curtain_last_connection" => $details["curtain_last_connection"],
									"curtain_length" => intval($details["curtain_length"]),
									"curtain_name" => $details["curtain_name"],
									"curtain_position" => intval($details["curtain_position"])));
}


// —————————————————— WEB ————————————————————
// ————————————————————————————————————————

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["get_activation_and_percentage_position"]))
{
	$curtain = $_POST["get_activation_and_percentage_position"];
	$details = get_activation_and_percentage_position($curtain);
	if(!$details) echo_failed();
	else echo json_encode($details);
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["get_curtain_activated"]))
{
	$curtain = $_POST["get_curtain_activated"];
	$results = get_curtain_activated($curtain);
	if(!$results) echo_failed();
	else echo json_encode(array("curtain_activated" => intval($results->fetch_assoc()["curtain_activated"])));
}

elseif($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["get_curtain_position"]))
{
	$curtain = $_POST["get_curtain_position"];
	$results = get_curtain_position($curtain);
	if(!$results) echo_failed();
	else echo json_encode(array("curtain_position" => intval($results->fetch_assoc()["curtain_position"])));
}




function echo_success($function_call=null)
{
	if($function_call) echo json_encode(array("success" => 1, "function" => $function_call));
	else echo json_encode(array("success" => 1));
	exit();
}


function echo_failed($function_call=null)
{
	if($function_call) echo json_encode(array("success" => 0, "function" => $function_call));
	else echo json_encode(array("success" => 0));
	exit();
}