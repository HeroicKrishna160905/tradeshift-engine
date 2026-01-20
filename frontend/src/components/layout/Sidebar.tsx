import { LayoutDashboard, History, Settings, TrendingUp } from 'lucide-react';
import { useGame } from '../../context/GameContext';

export type Page = 'terminal' | 'history' | 'settings';

interface SidebarProps {
  page: Page;
  setPage: (p: Page) => void;
}

const Sidebar = ({ page, setPage }: SidebarProps) => {
  const { theme } = useGame();

  const NavItem = ({ p, icon: Icon, label }: { p: Page, icon: any, label: string }) => (
    <button 
      onClick={() => setPage(p)}
      className={`w-full p-4 flex flex-col items-center gap-2 transition-all duration-300 group relative
        ${page === p 
          ? 'text-blue-500' 
          : `${theme === 'dark' ? 'text-gray-500 hover:text-gray-300' : 'text-gray-400 hover:text-gray-600'}`
        }
      `}
    >
      {/* Active Indicator Line (Animated) */}
      <div className={`absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 rounded-r-full bg-blue-500 transition-all duration-300 
        ${page === p ? 'opacity-100 scale-100' : 'opacity-0 scale-0'}
      `} />

      {/* Icon with Hover Animation */}
      <div className={`transition-transform duration-300 group-hover:scale-110 group-active:scale-95`}>
        <Icon size={24} />
      </div>
      
      {/* Label */}
      <span className="text-[10px] font-bold tracking-wide opacity-80">{label}</span>
    </button>
  );

  return (
    <div className={`w-20 border-r flex flex-col h-full z-20 transition-colors duration-300
      ${theme === 'dark' 
        ? 'bg-gray-900/50 border-gray-800 backdrop-blur-sm' 
        : 'bg-white/50 border-gray-200 backdrop-blur-sm'
      }`}>
      
      {/* Logo Area */}
      <div className={`h-16 flex items-center justify-center border-b mb-4 ${theme === 'dark' ? 'border-gray-800' : 'border-gray-200'}`}>
        <div className="bg-blue-500/10 p-2 rounded-xl transition-transform hover:rotate-12">
           <TrendingUp className="text-blue-500" size={24} />
        </div>
      </div>
      
      <NavItem p="terminal" icon={LayoutDashboard} label="Trade" />
      <NavItem p="history" icon={History} label="History" />
      <NavItem p="settings" icon={Settings} label="Config" />
    </div>
  );
};

export default Sidebar;