import React from 'react';


import Curtain from "./Curtain";
import Header from './Header/Header';
import Body from './Body/Body';


function curtain_by_id(curtain_id, curtains)
{
	return curtains.find(curtain => {return curtain.id == curtain_id;});
}


class SmartCurtain extends React.Component
{
	constructor(props)
	{
		super(props);
		this.state = {
			curtains: null,
			selected_curtain: null
		};
	}


	componentDidMount()
	{
		this.interval = setInterval(this.update.bind(this), 1000);
	}


	componentWillUnmount()
	{
		clearInterval(this.interval);
	}


	any_curtain_has_changed(curtains)
	{
		if(!this.state.curtains || curtains.length != this.state.curtains.length)
		{
			return true;
		}

		return this.state.curtains.some((curtain) => {return !curtain.equals(curtain_by_id(curtain.id, curtains));});
	}


	select_curtain(id)
	{
		this.setState({selected_curtain: curtain_by_id(id, this.state.curtains)});
	}


	selected_curtain()
	{
		return this.state.selected_curtain;
	}


	update()
	{
		console.log("Update")
		const header = {
  			method: "GET",
	  		headers: new Headers({
	  			"Authorization": `Bearer ${process.env.REACT_APP_BACKEND_API_KEY}`
	  		})
		};

		fetch("http://localhost:8080/api/v1.0/curtains/all", header)
		  .then(response => response.json())
		  .then(
			(result) => {
				const curtains = result.map((curtain) => {return new Curtain(curtain)});
				if(this.any_curtain_has_changed(curtains))
				{
					const selected_curtain = this.selected_curtain();
					// If no curtain is selected or the curtain no longer exists, default to first one
					if(!selected_curtain || !curtains.some(curtain => {return curtain.is_same(selected_curtain)}))
					{
						this.setState({curtains: curtains, selected_curtain: result.find(curtain => {return true;})});
					}
					// If the selected curtain has changed, update the curtain
					else
					{
						const updated_selected_curtain = curtain_by_id(selected_curtain.id, curtains);
						this.setState({curtains: curtains, selected_curtain: updated_selected_curtain});
					}
				}
			},
			(error) =>
			{
				this.setState({error});
			}
		  );
	}


	render()
	{
		if(this.state.curtains)
		{
			return (
				<div>
					<Header
						smart_curtain={this}
					/>
					<Body
						smart_curtain={this}
					/>
				</div>
			);
		}
		else
		{
			return (
				<p
					style={{color: "white"}}
				>
					Loading...
				</p>
			);
		}
	}
}


export default SmartCurtain;
