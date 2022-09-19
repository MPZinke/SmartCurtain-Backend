import React from 'react';


import Header from './Header/Header';
import Body from './Body/Body';


class SmartCurtain extends React.Component
{
	constructor(props)
	{
		super(props);
		this.state = {
			curtains: null,
			selected_curtain: null,
		};
	}


	select_curtain(id)
	{
		const curtain = this.state.curtains.find(curtain => {return curtain.id == id;});
		this.setState({selected_curtain: curtain});
	}


	selected_curtain()
	{
		return this.state.selected_curtain;
	}


	// FROM: https://reactjs.org/docs/faq-ajax.html
	componentDidMount()
	{
		this.iterval = setInterval(() =>
		  {
			fetch("http://localhost:8080/api/v1.0/curtains/all")
			  .then(response => response.json())
			  .then(
				(result) => {
					this.setState({curtains: result});
					const selected_curtain = this.selected_curtain();
					// If curtain is not selected
					if(!selected_curtain)
					{
						this.setState({selected_curtain: result.find(curtain => {return true;})});
					}
					// If the selected curtain has changed
					else if(selected_curtain != result.find(curtain => {return curtain.id == selected_curtain.id;}))
					{
						const updated_curtain = result.find(curtain => {return curtain.id == selected_curtain.id;});
						this.setState({selected_curtain: updated_curtain});
					}
				},
				(error) =>
				{
					console.log("error")
					console.log(error)
					this.setState(
						{
							error
						}
					);
				}
			)
		  },
		  1000
		);
	}


	componentWillUnmount()
	{
		clearInterval(this.interval);
	}


	render()
	{
		if(this.state.error)
		{
			return this.state.error;
		}
		else if(this.state.curtains)
		{
			return [
				<Header
					smart_curtain={this}
				/>,
				<Body
					smart_curtain={this}
				/>
			];
		}
		else
		{
			return <p>Loading...</p>
		}
	}
}


export default SmartCurtain;
