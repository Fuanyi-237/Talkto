export default function Counselors() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Counselors Management</h1>
      
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b">
          <div className="flex justify-between items-center">
            <input
              type="text"
              placeholder="Search counselors..."
              className="px-4 py-2 border rounded-lg w-64"
            />
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              Add Counselor
            </button>
          </div>
        </div>
        
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Specialty
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Rating
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Verification
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            <tr>
              <td className="px-6 py-4 whitespace-nowrap">Dr. Sarah Johnson</td>
              <td className="px-6 py-4 whitespace-nowrap">Anxiety & Depression</td>
              <td className="px-6 py-4 whitespace-nowrap">⭐ 4.8</td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                  Verified
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button className="text-blue-600 hover:text-blue-900 mr-3">View</button>
                <button className="text-red-600 hover:text-red-900">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}
