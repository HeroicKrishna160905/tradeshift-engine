import { Play, Pause } from 'lucide-react';
import { useGame } from '../../context/GameContext';

const PlaybackControls = () => {
  const { isPlaying, togglePlay, theme } = useGame();
  
  return (
    <div className={`absolute bottom-6 left-190 translate-x-1/2 px-6 py-2 rounded-full shadow-2xl flex items-center gap-4 border z-50 transition-all duration-300 hover:shadow-blue-500/20 hover:-translate-y-1 backdrop-blur-md
      ${theme === 'dark' 
        ? 'bg-gray-900/80 border-gray-700' 
        : 'bg-white/80 border-gray-200 shadow-blue-200/50'
      }`}>
      
      <button 
        onClick={togglePlay}
        className={`flex items-center gap-3 transition-all duration-200 group
          ${isPlaying ? 'text-red-500' : 'text-blue-500'}
        `}
      >
        <div className={`p-2 rounded-full transition-all duration-300 group-hover:scale-110 group-active:scale-90
          ${isPlaying 
            ? 'bg-red-500 text-white shadow-lg shadow-red-500/30' 
            : 'bg-blue-500 text-white shadow-lg shadow-blue-500/30'
          }`}>
          {isPlaying ? <Pause size={20} fill="currentColor" /> : <Play size={20} fill="currentColor" className="ml-0.5" />}
        </div>
        
        <span className={`font-bold text-sm tracking-wide transition-colors
           ${theme === 'dark' ? 'text-gray-200' : 'text-gray-700'}
        `}>
          {isPlaying ? 'PAUSE' : 'START'} REPLAY
        </span>
      </button>
    </div>
  );
};

export default PlaybackControls;