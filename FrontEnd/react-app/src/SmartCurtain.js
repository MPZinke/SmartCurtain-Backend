import React from 'react';

import './App.css';

import Header from './Header';




class SmartCurtain extends React.Component
{
	constructor(props)
	{
		super(props);
		this.curtains = {1: "Livingroom-Curtain", 2: "Bedroom-Curtain"};
		this.state = {
			curtain_id: 0,
		};
	}


	select_curtain(id)
	{
		this.setState({ curtain_id: id });
		console.log(id)
	}


	render()
	{
		return (
				<Header
					smart_curtain={this}
				/>
			// <div className="App">
			// 	<header className="App-header">
			// 		<img src={logo} className="App-logo" alt="logo" />
			// 		<p>
			// 			Edit <code>src/App.js</code> and save to reload.
			// 		</p>
			// 		<a
			// 			className="App-link"
			// 			href="https://reactjs.org"
			// 			target="_blank"
			// 			rel="noopener noreferrer"
			// 		>
			// 			Learn React
			// 		</a>
			// 	</header>
			// </div>
		);
	}
}


export default SmartCurtain;
