// This is a Functional Component with TypeScript
const MainLayout = () => {
  return (
    <div className="flex h-screen w-screen bg-gray-950 text-white">
      {/* Sidebar */}
      <aside className="w-16 border-r border-gray-800 flex flex-col items-center py-4">
        <div className="p-2 bg-blue-600 rounded">Logo</div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Topbar */}
        <header className="h-12 border-b border-gray-800 flex items-center px-4 justify-between">
            <span>NIFTY 50 Simulation</span>
            <div className="text-green-400">Connected</div>
        </header>

        {/* Chart Area */}
        <main className="flex-1 bg-black relative">
            {/* The Chart will go here later */}
            <h1 className="text-gray-500 m-10">Chart Placeholder</h1>
        </main>
      </div>
    </div>
  );
};

export default MainLayout;