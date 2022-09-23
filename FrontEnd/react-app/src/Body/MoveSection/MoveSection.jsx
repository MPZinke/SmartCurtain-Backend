

import React from 'react';


import BasicMoveButton from "./BasicMovement";


class MoveSection extends React.Component
{
	constructor(props)
	{
		super(props);
		this.state = {
			smart_curtain: props.smart_curtain,
		};
	}

	on_basic_click()
	{
		const percentage = 100 * +(this.smart_curtain().selected_curtain().percentage == 0);
		const request_options = {
			method: "POST",
			headers: {
	  			"Authorization": `Bearer ${process.env.REACT_APP_BACKEND_API_KEY}`,
				'Content-Type': 'application/json',
			}, 
			body: JSON.stringify({percentage: percentage})
		};

		const curtain_id = this.smart_curtain().selected_curtain().id;
		fetch(`http://localhost:8080/api/v1.0/curtains/${curtain_id}/events/new`, request_options)
		  .then(response => response.json())
		  .then((result) =>
			{
				this.smart_curtain().selected_curtain().is_activated = true;
				this.smart_curtain().selected_curtain()
				this.smart_curtain().setState({selected_curtain: this.smart_curtain().selected_curtain()});
			},
			(error) =>
			{
				console.log("error")
				console.log(error)
				this.setState(
					{
						error
					}
				);
			}
		  );
	}


	on_discrete_click()
	{
		console.log("TODO");
	}


	smart_curtain()
	{
		return this.state.smart_curtain;
	}


	render()
	{
		if(this.smart_curtain().selected_curtain().moves_discretely)
		{
			return (<p>TODO</p>);
		}
		else
		{
			return [
				<div
					key="move_section-div"
					className={"d-flex justify-content-center"}
					style={{width: "100%"}}
				>
					<p
						key="move_section-p"
						style={{color: "#DDDDCC"}}
					>
						{this.smart_curtain().selected_curtain().percentage}
					</p>
				</div>,
				<BasicMoveButton
					key="basicmovebutton"
					onClick={this.on_basic_click.bind(this)}
					percentage={this.smart_curtain().selected_curtain().percentage}
				/>
			];
		}
	}
}


export default MoveSection;
