import React from 'react';


import MoveSection from "./MoveSection/MoveSection"


class Body extends React.Component
{
	constructor(props)
	{
		super(props);
		this.state = {
			smart_curtain: props.smart_curtain
		};
	}


	smart_curtain()
	{
		return this.state.smart_curtain;
	}


	render()
	{
		return (
			<MoveSection
				key="move_section"
				smart_curtain={this.smart_curtain()}
			/>
		);
	}
}


export default Body;
