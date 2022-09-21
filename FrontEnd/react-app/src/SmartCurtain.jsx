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


	any_curtain_has_changed(curtains)
	{
		if(!this.state.curtains || curtains.length != this.state.curtains.length)
		{
			return true;
		}

		return !curtains.every(
			(curtain) =>
			{
				let state_curtain = this.state.curtains.find(state_curtain => {return state_curtain.id == curtain.id;});
				return curtain == state_curtain;
			}
		);
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
		this.iterval = setInterval(() =>  // FROM: https://stackoverflow.com/a/66044632
		  {
		  	const header = {
		  		headers: new Headers({
		  			'method': "GET",
		  			'Authorization': `Bearer ${process.env.REACT_APP_BACKEND_API_KEY}`
		  		})
			};

			fetch("http://localhost:8080/api/v1.0/curtains/all", header)
			  .then(response => response.json())
			  .then(
				(result) => {
					if(this.any_curtain_has_changed(result))
					{
						this.setState({curtains: result});
					}

					let selected_curtain = this.selected_curtain();
					// If curtain is not selected
					if(!selected_curtain)
					{
						this.setState({selected_curtain: result.find(curtain => {return true;})});
					}
					// If the selected curtain has changed
					else if(selected_curtain != result.find(curtain => {return curtain.id == selected_curtain.id;}))
					{
						selected_curtain = result.find(curtain => {return curtain.id == selected_curtain.id;});
						this.setState({selected_curtain: selected_curtain});
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
					key="header"
				/>,
				<Body
					smart_curtain={this}
					key="body"
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
