import { Users, UserCheck, Calendar, TrendingUp } from 'lucide-react'

export default function Dashboard() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <Users className="w-8 h-8 text-blue-600" />
            <span className="text-sm text-gray-500">Total Users</span>
          </div>
          <p className="text-3xl font-bold">1,234</p>
          <p className="text-sm text-green-600 mt-2">+12% from last month</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <UserCheck className="w-8 h-8 text-green-600" />
            <span className="text-sm text-gray-500">Active Counselors</span>
          </div>
          <p className="text-3xl font-bold">56</p>
          <p className="text-sm text-green-600 mt-2">+3 new this week</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <Calendar className="w-8 h-8 text-purple-600" />
            <span className="text-sm text-gray-500">Appointments</span>
          </div>
          <p className="text-3xl font-bold">892</p>
          <p className="text-sm text-green-600 mt-2">+8% from last month</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <TrendingUp className="w-8 h-8 text-orange-600" />
            <span className="text-sm text-gray-500">Revenue</span>
          </div>
          <p className="text-3xl font-bold">$45,678</p>
          <p className="text-sm text-green-600 mt-2">+15% from last month</p>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
        <p className="text-gray-500">No recent activity to display</p>
      </div>
    </div>
  )
}
