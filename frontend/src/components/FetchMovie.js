import React from "react";

export default class FetchMovie extends React.Component {
  state = {
    loading: true,
    person: null
  };

  async componentDidMount() {
    const url = "http://127.0.0.1:5000/json";
    const response = await fetch(url);
    const data = await response.json();
    this.setState({ person: data.results[0], loading: false });
  }

  render() {

    if(this.state.loading) {
      return <div> loading...</div>
    }

    if(!this.state.person) {
      return <div>didnt get a person</div>
    }
    

    return (
          <div>
            <div>{this.state.person.name.title}</div>
            <div>{this.state.person.name.first}</div>
            <div>{this.state.person.name.last}</div>
            <img src={this.state.person.picture.large} />
          </div>
    );
  }
}
