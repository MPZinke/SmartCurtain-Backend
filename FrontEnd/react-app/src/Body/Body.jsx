import React from 'react';
// import CurtainSelect from '../Blocks/Selects';
// import Status from './Status';


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
				<button
					className={"btn btn-info"}
				>
					Open
				</button>
				{/*<CurtainSelect
					curtains={this.smart_curtain.state.curtains}
					onChange={this.on_curtain_select.bind(this)}
					style={{width:"100%", height: "64px", fontSize: "32px"}}
				/>
				<Status
					percentage={20}
				/>*/}
			</div>
		);
	}
}


export default Header;
