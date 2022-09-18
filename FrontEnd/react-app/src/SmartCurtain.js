import React from 'react';

import './App.css';

import Header from './Header';




class SmartCurtain extends React.Component
{
	constructor(props)
	{
		super(props);
		this.curtains = null;
		this.state = {
			curtains: null,
			is_loaded: false,
			selected_curtain: null,
		};
	}


	select_curtain(id)
	{
		const curtain = this.state.curtains.find(curtain => {return curtain.id == id;});
		this.setState({selected_curtain: curtain});
		console.log("Set curtain", curtain)
	}


	// FROM: https://reactjs.org/docs/faq-ajax.html
	componentDidMount()
	{
		fetch("http://localhost:8080/api/v1.0/curtains/all", {"Access-Control-Allow-Origin": "*"})
		  .then(response => response.json())
		  .then(
			(result) => {
				this.setState(
					{
						curtains: result,
						select_curtain: result.find(curtain => {return true;}),
					}
				);
				console.log("State", this.state.curtains);
			},
			(error) =>
			{
				this.setState(
					{
						error
					}
				);
			}
		);
	}


	render()
	{
		if(this.state.error)
		{
			return this.state.error;
		}
		else if(this.state.curtains)
		{
			return (
				<Header
					smart_curtain={this}
				/>

			);
		}
		else
		{
			return <p>Loading...</p>
		}
	}
}


export default SmartCurtain;
