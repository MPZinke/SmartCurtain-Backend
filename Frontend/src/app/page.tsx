import Image from 'next/image'
import styles from './page.module.css'

export default async function Main() {
	const response = await fetch("http://localhost:8080/homes");
	const curtains = await response.json();

	return (
		<main>
			{JSON.stringify(curtains)}
			{/*{
				curtains.map(curtain =>
					{
						curtain.name
					}
				)
			}*/}
		</main>
	)
}
