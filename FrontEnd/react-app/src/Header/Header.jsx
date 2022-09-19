import React from 'react';
import CurtainSelect from '../Blocks/Selects';
import Status from './Status';


class Header extends React.Component
{
	constructor(props)
	{
		super(props);
		this.state = {
			smart_curtain: props.smart_curtain
		}
	}


	on_curtain_select(event)
	{
		this.state.smart_curtain.select_curtain(event.target.value);
	}


	smart_curtain()
	{
		return this.state.smart_curtain;
	}


	render()
	{
		return (
			<div>
				<CurtainSelect
					curtains={this.smart_curtain().state.curtains}
					onChange={this.on_curtain_select.bind(this)}
					style={{width:"100%", height: "64px", fontSize: "32px"}
					}
				/>
				<Status
					is_activated={this.smart_curtain().selected_curtain().is_activated}
					percentage={this.smart_curtain().selected_curtain().percentage}
				/>
			</div>
		);
	}
}


export default Header;
