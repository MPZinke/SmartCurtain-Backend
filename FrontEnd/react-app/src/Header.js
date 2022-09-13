import React from 'react';



function CurtainSelect(props)
{
	return (
		<select
			onChange={props.onChange}
		>
			<option value="0" selected disabled hidden></option>
			{
				Object.keys(props.curtains).map(
					(id, index) =>
					{
						return (
							<option
								key={id}
								value={id}
							>
								{props.curtains[id]}
							</option>
						);
					}
				)
			}
		</select>
	);
}


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
					onChange={this.on_curtain_select.bind(this)}
					curtains={this.smart_curtain.curtains}
				/>
			</div>
		);
	}
}


export default Header;
