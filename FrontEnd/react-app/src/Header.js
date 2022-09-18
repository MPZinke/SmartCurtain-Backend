import React from 'react';
import CurtainSelect from './Blocks/Selects';


class Header extends React.Component
{
	constructor(props)
	{
		super(props);
		this.smart_curtain = props.smart_curtain;
	}


	on_curtain_select(event)
	{
		this.smart_curtain.select_curtain(event.target.value);
	}


	render()
	{
		return (
			<div>
				<CurtainSelect
					curtains={this.smart_curtain.state.curtains}
					onChange={this.on_curtain_select.bind(this)}
					style={{width:"100%"}}
				/>
			</div>
		);
	}
}


export default Header;
