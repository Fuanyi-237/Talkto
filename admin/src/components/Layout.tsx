import { Outlet, Link } from 'react-router-dom'
import { Layout as LayoutIcon, Users, UserCheck, Calendar, Settings } from 'lucide-react'

export default function Layout() {
  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-lg">
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold text-blue-600">Talkto Admin</h1>
        </div>
        <nav className="p-4">
          <ul className="space-y-2">
            <li>
              <Link to="/" className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-100 transition-colors">
                <LayoutIcon className="w-5 h-5" />
                <span>Dashboard</span>
              </Link>
            </li>
            <li>
              <Link to="/users" className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-100 transition-colors">
                <Users className="w-5 h-5" />
                <span>Users</span>
              </Link>
            </li>
            <li>
              <Link to="/counselors" className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-100 transition-colors">
                <UserCheck className="w-5 h-5" />
                <span>Counselors</span>
              </Link>
            </li>
            <li>
              <Link to="/appointments" className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-100 transition-colors">
                <Calendar className="w-5 h-5" />
                <span>Appointments</span>
              </Link>
            </li>
            <li>
              <Link to="/settings" className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-100 transition-colors">
                <Settings className="w-5 h-5" />
                <span>Settings</span>
              </Link>
            </li>
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8">
        <Outlet />
      </main>
    </div>
  )
}
