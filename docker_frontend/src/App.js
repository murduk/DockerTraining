import logo from './logo.svg';
import { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: process.env.REACT_APP_BACKEND,
})

function App() {
  console.log(process.env.REACT_APP_BACKEND)
  const [posts, setPosts] = useState([])
  const [newPost, setNewPost] = useState("")

  useEffect(() => {
    axiosInstance.get('/').then(response => {
      console.log(response.data)
      setPosts(response.data)
    })
  }, [])

  const refresh = () => {
    axiosInstance.get('/').then(response => {
      console.log(response.data)
      setPosts(response.data)
    })
  }

  const onPostChange = (e) => {
    setNewPost(e.target.value)
  }

  const submitNewPost = () => {
    axiosInstance.post('/newpost', { newpost: newPost }).then(response => {
      refresh()
    })
  }

  const listItems = posts.map((post, index) =>
    <li key={index}>
      {post}
    </li>
  );

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h2>Previous Posts</h2>
        <ul>{listItems}</ul>
        <textarea value={newPost} onChange={onPostChange}></textarea>
        <h3>Post Something</h3>
        <button onClick={submitNewPost}>Post</button>
      </header>
    </div>
  );
}

export default App;
