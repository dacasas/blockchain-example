import React, { Component } from 'react';
import './App.css';

const url = path => `http://localhost:5000${path}`

class Transactions extends Component {
  state = {
    from: "",
    to: "",
    amount: "",
    generated: [],
    version: 0,
  }
  static getDerivedStateFromProps(nextProps, prevState) {
    if (nextProps.version !== prevState.version) {
      return {
        generated: [],
        version: nextProps.version,
      }
    }
  }
  handleWrite = (key, text) => {
    this.setState({
      [key]: text,
    })
  }
  handleSubmit = async e => {
    e.preventDefault()
    const { from, to, amount, generated } = this.state
    const fetched = await fetch(url('/transaction'), {
      method: "post",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        from, to, amount,
      })
    })
    const fetchedText = await fetched.text()
    if (fetchedText.trim() === "Transaction submission successful") {
      this.setState({
        from: "",
        to: "",
        amount: "",
        generated: [{ from, to, amount }, ...generated]
      })
    }
  }

  createRandom = () => {
    this.setState({
      from: Math.random().toString(36).substring(2),
      to: Math.random().toString(36).substring(2),
      amount: Math.trunc(Math.random() * 1000)
    })
  }
  render() {
    const { generated } = this.state
    return (
      <div>
        <h1>Transactions</h1>
        <form onSubmit={this.handleSubmit}>
          <div>
            <label htmlFor="from">From: </label>
            <input id="from" value={this.state.from} onChange={e => this.handleWrite("from", e.target.value)} />
          </div>
          <div>
            <label htmlFor="to">To: </label>
            <input id="to" value={this.state.to} onChange={e => this.handleWrite("to", e.target.value)} />
          </div>
          <div>
            <label htmlFor="amount">Amount: </label>
            <input id="amount" value={this.state.amount} onChange={e => this.handleWrite("amount", e.target.valueAsNumber)} type="number"/>
          </div>
          <button>Create</button>
          <button onClick={this.createRandom}>Create Random</button>
        </form>
        <h2>Generated Transactions</h2>
        <pre>
          {JSON.stringify(generated, null, 2)}
        </pre>
      </div>
    )
  }
}

class Miner extends Component {
  state = {
    mining: false,
    mineDuration: 0,
    durations: [],
  }
  mine = async () => {
    const start = new Date().getTime()
    this.setState({ mining: true, mineDuration: 0 })
    const interval = setInterval(() => {
      this.setState({ mineDuration: new Date().getTime() - start })
    }, 1)
    await fetch(url('/mine'))
    const { durations } = this.state
    this.setState({
      mining: false,
      durations: [...durations, new Date().getTime() - start],
      mineDuration: new Date().getTime() - start
    })
    clearInterval(interval)
    this.props.onFinishMine()
  }
  infiniteMine = async () => {
    await this.mine()
    this.infiniteMine()
  }
  render() {
    const { mineDuration, durations } = this.state
    return (
      <div>
        <h1>Miner</h1>
        <button onClick={this.mine} disabled={this.state.mining}>Mine</button>
        <button onClick={this.infiniteMine} disabled={this.state.mining}>Infinite Mine</button>
        <p>Mine duration: {mineDuration} ms</p>
        <h2>Durations</h2>
        <ol>
          {durations.map((duration, i) => <li key={i}><strong>{duration}</strong> ms</li>)}
        </ol>
      </div>
    )
  }
}

class Blockchain extends Component {
  render() {
    const { blocks } = this.props
    return (
      <div>
        <h1>Blockchain</h1>
        <pre>
          {JSON.stringify(blocks, null, 2)}
        </pre>
      </div>
    )
  }
}

class App extends Component {
  state = {
    version: 0,
    blocks: [],
  }
  fetchBlocks = async () => {
    const response = await fetch(url('/blocks'))
    const blocks = await response.json()
    this.setState({
      blocks: blocks
        .reverse()
        .map(block => ({ ...block, data: JSON.parse(this.stringBeautify(block.data)) }))
    })
  }
  stringBeautify(string) {
    return string.split("'").join("\"").replace("None", "null")
  }

  handleFinishMine = () => {
    this.setState(({ version }) => ({ version: version + 1 }) )
    this.fetchBlocks()
  }
  render() {
    const { version, blocks } = this.state
    return (
      <div style={{ display: "flex", flexFlow: "row nowrap", justifyContent: "space-around"}}>
        <Transactions version={version} />
        <Miner onFinishMine={this.handleFinishMine} />
        <Blockchain blocks={blocks} />
      </div>
    );
  }
}

export default App;
