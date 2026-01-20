import { Wallet, Sun, Moon } from 'lucide-react';
import { useGame } from '../../context/GameContext';

const Topbar = () => {
  const { balance, isPlaying, theme, toggleTheme } = useGame();
  
  return (
    <header className={`h-16 border-b flex items-center justify-between px-6 transition-colors duration-300
      ${theme === 'dark' 
        ? 'bg-gray-900/40 border-gray-800 backdrop-blur-md' 
        : 'bg-white/40 border-gray-200 backdrop-blur-md'
      }`}>
      
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-bold tracking-wide">
          QUANT<span className="text-blue-500">SIM</span>
        </h1>
        <span className={`px-2 py-0.5 rounded text-xs font-mono border transition-colors duration-300
          ${isPlaying 
            ? 'bg-green-500/10 text-green-500 border-green-500/20' 
            : 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20'
          }`}>
          {isPlaying ? 'LIVE FEED' : 'PAUSED'}
        </span>
      </div>
      
      <div className="flex items-center gap-4">
        {/* THEME TOGGLE BUTTON */}
        <button 
          onClick={toggleTheme}
          className={`p-2 rounded-full transition-all duration-300 hover:scale-110 active:rotate-180
            ${theme === 'dark' 
              ? 'hover:bg-gray-800 text-yellow-400' 
              : 'hover:bg-blue-100 text-slate-700'
            }`}
        >
          {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
        </button>

        <div className="h-6 w-[1px] bg-gray-500/20"></div>

        <div className="flex items-center gap-3">
          <div className="flex flex-col items-end">
            <span className={`text-[10px] uppercase font-bold tracking-wider ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>Account Equity</span>
            <span className="font-mono text-lg font-bold">₹{balance.toLocaleString('en-IN', { maximumFractionDigits: 2 })}</span>
          </div>
          <div className="w-10 h-10 rounded-full flex items-center justify-center bg-blue-500 text-white shadow-lg shadow-blue-500/30">
            <Wallet size={20} />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Topbar;