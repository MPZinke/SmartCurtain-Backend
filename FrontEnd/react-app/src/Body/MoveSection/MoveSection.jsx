

import React from 'react';


import BasicMoveButton from "./BasicMovement";


class MoveSection extends React.Component
{
	constructor(props)
	{
		super(props);
		this.state = {
			smart_curtain: props.smart_curtain,
			moves_discretely: props.moves_discretely,
		};
	}

	on_basic_click()
	{
		const percentage = 100 * +(this.state.smart_curtain.state.selected_curtain.percentage == 0);
		this.state.smart_curtain.state.selected_curtain.percentage = percentage;
		this.state.smart_curtain.setState({selected_curtain: this.state.smart_curtain.state.selected_curtain});
	}


	on_discrete_click()
	{
		console.log("Discrete Click");
	}


	smart_curtain()
	{
		return this.state.smart_curtain;
	}


	render()
	{
		if(this.state.moves_discretely)
		{
			return (<p>TODO</p>);
		}
		else
		{
			return [
				<p
					style={{color: "#DDDDCC"}}
				>
					{this.smart_curtain().selected_curtain().percentage}
				</p>,
				<BasicMoveButton
					onClick={this.on_basic_click.bind(this)}
					percentage={this.state.smart_curtain.state.selected_curtain.percentage}
				/>
			];
		}
	}
}


export default MoveSection;
