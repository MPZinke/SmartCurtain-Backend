'use client'


/***********************************************************************************************************************
*                                                                                                                      *
*   created by: MPZinke                                                                                                *
*   on 2023.06.08                                                                                                      *
*                                                                                                                      *
*   DESCRIPTION: TEMPLATE                                                                                              *
*   BUGS:                                                                                                              *
*   FROM:        https://swizec.com/blog/async-react-with-nextjs-13/                                                   *
*                                                                                                                      *
***********************************************************************************************************************/


interface TOption
{
	id: number;
	description: string;
	is_deleted: boolean;
	name: string;
};


interface TCurtainOption
{
	id: number;
	Option: TOption;
	data: object | null;
	is_on: boolean;
	notes: string; 
};


function CurtainEvent(props: Any)
{

}


function CurtainOption(props: TCurtainOption)
{
	const {curtain_option} = props;
	return (
		<table>
			<tbody>
				<tr>
					<td>
						Name
					</td>
					<td>
						{curtain_option.Option.name}
					</td>
				</tr>
				<tr>
					<td>
						Is On
					</td>
					<td>
						{curtain_option.is_on}
					</td>
				</tr>
				<tr>
					<td>
						Data
					</td>
					<td>
						{curtain_option.data === null ? "NULL" : JSON.stringify(curtain_option.data)}
					</td>
				</tr>
				<tr>
					<td>
						Notes
					</td>
					<td>
						{curtain_option.notes}
					</td>
				</tr>
				<tr>
					<td>
						Description
					</td>
					<td>
						{curtain_option.Option.description}
					</td>
				</tr>
				<tr>
					<td>
						Is Deleted
					</td>
					<td>
						{curtain_option.is_deleted}
					</td>
				</tr>
			</tbody>
		</table>
	);
}


export default async function IDPage({params})
{
	const id = params.id;

	const response = await fetch(`http://localhost:8080/curtains/${id}`);
	const curtain = await response.json();

	// const curtain_events = curtain.map((curtain))
	const curtain_options = curtain.CurtainOptions.map(curtain_option => 
		<CurtainOption
		  curtain_option={curtain_option}
		/>
	);

	return (
		<div>
			<h1>
				{curtain.name}
			</h1>
			<table>
				<tbody>
					<tr>
						<td>Is Connected</td>
						<td>
							{curtain.is_deleted === true ? "True" : "False"}
						</td>
					</tr>
					<tr>
						<td>Percentage</td>
						<td>
							{curtain.percentage}
						</td>
					</tr>
					<tr>
						<td>Is Moving</td>
						<td>
							{curtain.is_deleted === true ? "True" : "False"}
						</td>
					</tr>
					<tr>
						<td>Length</td>
						<td>
							{curtain.length === null ? "NULL" : curtain.length}
						</td>
					</tr>
					<tr>
						<td>Is Deleted</td>
						<td>
							{curtain.is_deleted === true ? "True" : "False"}
						</td>
					</tr>
					<tr>
						<td>Curtain Events</td>
						<td>
							{JSON.stringify(curtain.CurtainEvents)}
						</td>
					</tr>
					<tr>
						<td>Curtain Options</td>
						<td>
							{curtain_options}
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	);
}
