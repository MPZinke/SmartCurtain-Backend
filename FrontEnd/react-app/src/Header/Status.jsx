

function StatusTD(props)
{
	const background_color = props.is_activated ? "#11FF11": "#FFFFAA";

	if(props.percentage == 0)
	{
		return (
			<td
				style={{width: "100%"}}
			/>
		);

	}
	else if(props.percentage == 100)
	{
		return (
			<td
				style={{width: "100%", backgroundColor: background_color}}
			/>
		);
	}
	else
	{
		console.log("Percentage", props.percentage)
		return [
			<td
				key={1}
				style={{width: `${(100-props.percentage)/2}%`}}
			/>,
			<td
				key={2}
				style={{width: `${props.percentage}%`, backgroundColor: background_color}}
			/>,
			<td
				key={3}
				style={{width: `${(100-props.percentage)/2}%`}}
			/>
			]
		;
	}
}


function Status(props)
{
	return (
		<table
			style={{width: "100%"}}
		>
			<tbody>
				<tr>
					<StatusTD
						is_activated={props.is_activated}
						percentage={props.percentage}
					/>
				</tr>
			</tbody>
		</table>
	);
}


export default Status;
