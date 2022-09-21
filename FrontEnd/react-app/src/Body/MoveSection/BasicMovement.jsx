

function BasicMoveButton(props)
{
	const button_text = props.percentage == 0 ? "Open" : "Close";
	return (
		<div
			key="basic_div"
			className={"d-flex justify-content-center"}
			style={{width: "100%"}}
		>
			<button
				className={"btn btn-info"}
				key={"basic-button"}
				onClick={props.onClick}
			>
				{button_text}
			</button>
		</div>
	);
}


export default BasicMoveButton;
