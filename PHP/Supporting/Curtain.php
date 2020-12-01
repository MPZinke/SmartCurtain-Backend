<?php

class Curtain
{
	public $curtain_id;
	public $curtain_activated;
	public $curtain_direction;
	public $curtain_last_connection;
	public $curtain_length;
	public $curtain_name;
	public $curtain_position;
	// options — BOOL
	public $adafruit_feed;
	public $auto_calibration;
	public $event_predictor;
	public $sunrise_open;
	public $sunset_close;
	// objects
	public $events = array();  // future events
	public $passed_events = array();
	// other
	public $errors = array();

	function __construct($curtain_id)
	{
		if(!$curtain_id || !is_numeric($curtain_id))
			return $this->null_all_values();

		$this->curtain_id = $curtain_id;
		if(!$this->set_curtain_attributes()) return;
		$this->set_curtain_events();
		$this->set_curtain_errors();
		$this->set_curtain_options();
	}


	public function __invoke()
	{
		return $this->curtain_id;
	}


	function all_curtains()
	{
		global $mysqli;

		$results = $mysqli->query(	"SELECT `curtain_id`FROM `curtains`;");
		if(!$results) return array();

		$curtains = array();
		while($row = $results->fetch_assoc()) $curtains[] = new self($row["curtain_id"]);
		return $curtains;
	}


	public function current_state_percentage()
	{
		if(!$this->curtain_id) return 0;

		return $this->curtain_position *100 / $this->curtain_length;
	}


	private function null_all_values()
	{
		foreach($this as $key => $value) $this->$key = 0;
	}


	private function set_curtain_attributes()
	{
		global $mysqli;
		$results = $mysqli->query(	"SELECT * FROM `curtains` 
										WHERE `curtain_id` = $this->curtain_id");
		if(!$results || !$results->num_rows) return $this->null_all_values();

		$results = $results->fetch_assoc();
		$this->curtain_activated = $results["curtain_activated"];
		$this->curtain_direction = $results["curtain_direction"];
		$this->curtain_last_connection = $results["curtain_last_connection"];
		$this->curtain_length = $results["curtain_length"];
		$this->curtain_name = $results["curtain_name"];
		$this->curtain_position = $results["curtain_position"];

		return true;
	}


	private function set_curtain_errors()
	{
		global $mysqli;
		$results = $mysqli->query(	"SELECT * FROM `error_log` 
										WHERE `curtain_id` = $this->curtain_id
										ORDER BY `time` DESC");

		if($results)
		{
			while($row = $results->fetch_assoc()) $this->errors[] = $row;
		}
	}


	private function set_curtain_events()
	{
		global $mysqli;
		$results = $mysqli->query(	"SELECT `event_id` FROM `events` 
										WHERE `curtain_id` = $this->curtain_id
										AND `event_time` > CURRENT_TIME
										ORDER BY `event_time` DESC");

		if($results)
			while($row = $results->fetch_assoc()) $this->events[] = new Event($row["event_id"]);

		$results = $mysqli->query(	"SELECT `event_id` FROM `events` 
										WHERE `curtain_id` = $this->curtain_id
										AND CURRENT_TIME > `event_time`
										ORDER BY `event_time` DESC
										LIMIT 50");

		if($results)
			while($row = $results->fetch_assoc()) $this->passed_events[] = new Event($row["event_id"]);
	}


	private function set_curtain_options()
	{
		global $mysqli;
		$results = $mysqli->query(	"SELECT * FROM `options`
										WHERE `curtain_id` = $this->curtain_id");
		if(!$results) return $this->null_all_values;

		$results = $results->fetch_assoc();
		$this->adafruit_feed = $results["adafruit_feed"];
		$this->auto_calibration = $results["auto_calibration"];
		$this->event_predictor = $results["event_predictor"];
		$this->sunrise_open = $results["sunrise_open"];
		$this->sunset_close = $results["sunset_close"];
	}
}

?>