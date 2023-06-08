import Image from 'next/image'
import styles from './page.module.css'


interface CType
{
	id: number;
	name: string;
};


interface BType
{
	id: number;
	name: string;
	c_s: CType[];
}


function B(props: BType)
{
	console.log(props.id)
	const c_s = props.c_s.map(c => 
		<tr>
			<td>
				<C
				  id={c.id}
				  name={c.name}
				/>
			</td>
		</tr>
	);

	return (
		<a
		  href={`/b/${props.id}`}
		>
			<div>
				{props.name}
				<table>
					<tbody>
						{c_s}
					</tbody>
				</table>
			</div>
		</a>
	);
}


function C(props: {id: int, name: string})
{
	console.log(props.id)
	return (
		<a
		  href={`/c/${props.id}`}
		>
			<button>
				{props.name}
			</button>
		</a>
	);
}



export default async function Main() {
	const response = await fetch("http://localhost:8080/homes/1/structure");
	const values = await response.json();

	const b_s = values.rooms.map(b =>
		// {
			<B
			  id={b.id}
			  name={b.name}
			  c_s={b.curtains}
			/>
		// }
	);

	return (
		<main>
			{b_s}
			{/*{
				values.map(value =>
					{
						value.name
					}
				)
			}*/}
		</main>
	)
}
