// frontend/src/pages/mainapppage.tsx

export default function MainAppPage() {
  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Server List Column */}
      <div className="w-20 bg-gray-800 p-2">
        <p className="text-center font-bold">Servers</p>
      </div>

      {/* Channel List & User Info Column */}
      <div className="w-60 flex flex-col bg-gray-700">
        <div className="p-2 border-b border-gray-600">
          <h1 className="font-bold">Channel List</h1>
        </div>
        <div className="flex-1 p-2">{/* Channel links will go here */}</div>
        <div className="p-2 border-t border-gray-600">
          <p>User Info</p>
        </div>
      </div>

      {/* Main Chat Area Column */}
      <div className="flex-1 flex flex-col bg-gray-600">
        <div className="p-2 border-b border-gray-500">
          <h2 className="font-bold">#general</h2>
        </div>
        <div className="flex-1 p-2">{/* Messages will go here */}</div>
        <div className="p-2">
          <input
            type="text"
            placeholder="Message #general"
            className="w-full bg-gray-500 rounded p-2 focus:outline-none"
          />
        </div>
      </div>
    </div>
  );
}