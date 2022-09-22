

class Curtain
{
	constructor(curtain)
	{
		this.id = curtain.id;
		this.name = curtain.name;
		this.ip_address = curtain.ip_address;
		this.is_activated = curtain.is_activated;
		this.length = curtain.length;
		this.moves_discretely = curtain.moves_discretely;
		this.percentage = curtain.percentage;
	}


	equals(curtain)
	{
		if(!curtain)
		{
			return false;
		}

		return this.id == curtain.id && this.name == curtain.name && this.ip_address == curtain.ip_address
		  && this.is_activated == curtain.is_activated && this.length == curtain.length
		  && this.moves_discretely == curtain.moves_discretely && this.percentage == curtain.percentage;
	}


	is_same(curtain)
	{
		return this.id == curtain.id;
	}
}


export default Curtain;
