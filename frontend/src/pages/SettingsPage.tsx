import { Activity, AlertCircle } from 'lucide-react';
import { useGame } from '../context/GameContext';

const SettingsPage = () => {
  const { speed, setSpeed, resetSimulation } = useGame();
  
  return (
    <div className="p-8 w-full max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-white mb-6">Settings</h2>
      
      <div className="space-y-6">
        {/* Speed Control Section */}
        <div className="bg-gray-900 p-6 rounded-lg border border-gray-800">
          <div className="flex items-center gap-3 mb-4 text-white">
            <Activity className="text-blue-500" />
            <h3 className="font-semibold">Simulation Speed</h3>
          </div>
          <p className="text-gray-400 text-sm mb-4">Control how fast the historical data is replayed.</p>
          
          <div className="flex items-center gap-4">
            <input 
              type="range" 
              min="1" 
              max="20" 
              value={speed} 
              onChange={(e) => setSpeed(parseInt(e.target.value))}
              className="flex-1 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
            <span className="text-white font-mono w-12 text-right">{speed}x</span>
          </div>
        </div>

        {/* Reset Section */}
        <div className="bg-gray-900 p-6 rounded-lg border border-gray-800">
          <div className="flex items-center gap-3 mb-4 text-white">
            <AlertCircle className="text-red-500" />
            <h3 className="font-semibold">Danger Zone</h3>
          </div>
          <div className="flex items-center justify-between">
            <p className="text-gray-400 text-sm">Reset account balance and clear trade history.</p>
            <button 
              onClick={resetSimulation}
              className="px-4 py-2 bg-red-900/50 text-red-400 hover:bg-red-900 border border-red-900 rounded transition-colors text-sm font-medium"
            >
              Reset Simulation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;