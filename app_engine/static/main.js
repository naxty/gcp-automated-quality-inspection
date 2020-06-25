'use strict';

const e = React.createElement;


class Image extends React.Component {
  render() {
    return (
      e('img', { src: this.props.url })
    )
  }
}

class Decision extends React.Component {

  makeDecision() {
    let formData = {
      id: this.props.id,
      decision: this.props.decision
    }
    fetch('./make_decision', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify(formData)
    })
      .then(response => response.json())
      .then(result => {
        console.log('Success:', result);
        this.props.reload()
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
  render() {
    //return e('button', { on })
    return React.createElement("button", {
      onClick: () => this.makeDecision()
    }, this.props.text);
  }
}

class MainApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasImage: false, url: null, id: null };
  }

  loadImage() {
    console.log("loading image")
    fetch('./need_decision')
      .then(response => {
        return response.json()
      })
      .then(data => {
        if ("id" in data) {
          this.setState(
            {
              url: data.url,
              id: data.id,
              hasImage: true
            })
        } else {
          this.setState(
            {
              url: null,
              id: null,
              hasImage: false
            })
        }
      });
  }

  componentDidMount() {
    this.loadImage()
  }

  render() {
    console.log(this.state)

    if (this.state.hasImage === false) {
      return 'There are no images for a decision right now.';
    }

    return React.createElement("div", null,
      React.createElement(Image, {
        url: this.state.url
      }),
      React.createElement("div", null,
        React.createElement(Decision, {
          decision: "ok",
          text: "Ok",
          id: this.state.id,
          reload: () => this.loadImage()
        }),
        React.createElement(Decision, {
          decision: "defect",
          text: "Defect",
          id: this.state.id,
          reload: () => this.loadImage()
        })));
  }
}
const domContainer = document.querySelector('#container');
ReactDOM.render(e(MainApp), domContainer);