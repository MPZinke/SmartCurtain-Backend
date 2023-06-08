
export default async function IDPage({params})
{
	const id = params.id;

	const response = await fetch(`http://localhost:8080/curtains/${id}`);
	const curtain = await response.json();

	async function click_click_click()
	{
		'use server';

		console.log("click_click_click")
		const response = await fetch(`http://localhost:8080/curtains/${id}`,
			{
				body: "This is a test",
				method: "POST"
			}
		);
	}

	return (
		<div>
			<h1>
				{curtain.name}
			</h1>
			<h2>
				{curtain.percentage}
			</h2>
			<button
			  onClick={click_click_click}
			>
				{curtain.percentage == 0 ? "OPEN" : "CLOSE"}
			</button>
		</div>
	);
}
