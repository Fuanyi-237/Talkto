import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Users from './pages/Users'
import Counselors from './pages/Counselors'
import Layout from './components/Layout'

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/users" element={<Users />} />
          <Route path="/counselors" element={<Counselors />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
