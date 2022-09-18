
/***********************************************************************************************************************
*                                                                                                                      *
*   created by: MPZinke                                                                                                *
*   on 2022.09.13                                                                                                      *
*                                                                                                                      *
*   DESCRIPTION: TEMPLATE                                                                                              *
*   BUGS:                                                                                                              *
*   FUTURE:                                                                                                            *
*                                                                                                                      *
***********************************************************************************************************************/


function CurtainSelect(props)
{
	const curtains = props.curtains;

	return (
		<select
			onChange={props.onChange}
			style={props.style}
		>
			{props.default_option}
			{
				curtains.map(
					(curtain, index) =>
					{
						return (
							<option
								key={curtain.id}
								value={curtain.id}
							>
								{curtain.name}
							</option>
						);
					}
				)
			}
		</select>
	);
}


export default CurtainSelect;
