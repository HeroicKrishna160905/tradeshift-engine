import { useState } from 'react';
import { useGame } from '../../context/GameContext';

const OrderPanel = () => {
  const { currentPrice, placeOrder, isPlaying, theme, trades, closePosition } = useGame();
  const [qty, setQty] = useState(50);

  return (
    <div className={`w-80 border-l flex flex-col transition-colors duration-300
      ${theme === 'dark' 
        ? 'bg-gray-900/50 border-gray-800 backdrop-blur-sm' 
        : 'bg-white/50 border-gray-200 backdrop-blur-sm'
      }`}>
      
      {/* Header & Inputs */}
      <div className={`p-4 border-b ${theme === 'dark' ? 'border-gray-800' : 'border-gray-200'}`}>
        <h2 className={`font-bold mb-4 flex items-center gap-2 ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>
          <span className="w-1.5 h-6 bg-blue-500 rounded-full"></span>
          Place Order
        </h2>
        
        <div className="space-y-4">
          {/* Quantity Selector */}
          <div>
            <label className={`text-xs mb-1 block font-medium ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>Quantity (Lots)</label>
            <div className="flex items-center gap-2">
              <button 
                onClick={() => setQty(Math.max(50, qty - 50))} 
                className={`w-10 h-10 rounded-lg flex items-center justify-center font-bold transition-all hover:scale-105 active:scale-95
                  ${theme === 'dark' ? 'bg-gray-800 hover:bg-gray-700 text-white' : 'bg-gray-200 hover:bg-gray-300 text-gray-800'}
                `}>-</button>
              
              <input 
                type="number" 
                value={qty} 
                readOnly
                className={`flex-1 h-10 border rounded-lg text-center font-mono font-bold bg-transparent
                  ${theme === 'dark' ? 'border-gray-700 text-white' : 'border-gray-300 text-gray-900'}
                `}
              />
              
              <button 
                onClick={() => setQty(qty + 50)} 
                className={`w-10 h-10 rounded-lg flex items-center justify-center font-bold transition-all hover:scale-105 active:scale-95
                  ${theme === 'dark' ? 'bg-gray-800 hover:bg-gray-700 text-white' : 'bg-gray-200 hover:bg-gray-300 text-gray-800'}
                `}>+</button>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="grid grid-cols-2 gap-3">
            <button 
              disabled={!isPlaying}
              onClick={() => placeOrder('BUY', qty)}
              className="group relative bg-green-600 hover:bg-green-500 disabled:opacity-50 disabled:cursor-not-allowed text-white py-4 rounded-xl font-bold transition-all duration-200 hover:shadow-lg hover:shadow-green-500/25 active:scale-95 active:translate-y-0.5 overflow-hidden"
            >
              <div className="flex flex-col items-center relative z-10">
                <span className="text-[10px] opacity-75 tracking-wider">LONG</span>
                <span className="text-lg">BUY</span>
              </div>
            </button>
            
            <button 
              disabled={!isPlaying}
              onClick={() => placeOrder('SELL', qty)}
              className="group relative bg-red-600 hover:bg-red-500 disabled:opacity-50 disabled:cursor-not-allowed text-white py-4 rounded-xl font-bold transition-all duration-200 hover:shadow-lg hover:shadow-red-500/25 active:scale-95 active:translate-y-0.5 overflow-hidden"
            >
              <div className="flex flex-col items-center relative z-10">
                <span className="text-[10px] opacity-75 tracking-wider">SHORT</span>
                <span className="text-lg">SELL</span>
              </div>
            </button>
          </div>
          
          {/* Margin Info */}
          <div className={`p-3 rounded-lg text-xs text-center border
            ${theme === 'dark' 
              ? 'bg-gray-800/50 border-gray-700 text-gray-400' 
              : 'bg-blue-50 border-blue-100 text-blue-600'
            }`}>
            Margin Req: <span className="font-mono font-bold">₹{((currentPrice * qty) / 5).toFixed(0)}</span>
          </div>
        </div>
      </div>
      
      {/* Positions List */}
      <div className="flex-1 overflow-auto p-4 scrollbar-thin">
        <h3 className={`text-xs font-bold uppercase mb-3 ${theme === 'dark' ? 'text-gray-500' : 'text-gray-400'}`}>Active Positions</h3>
        <div className="space-y-3">
          {trades.filter(t => t.status === 'OPEN').map(trade => {
             const multiplier = trade.type === 'BUY' ? 1 : -1;
             const pnl = (currentPrice - trade.entryPrice) * trade.quantity * multiplier;
             const isProfit = pnl >= 0;
             return (
               <div key={trade.id} className={`rounded-xl p-3 border transition-all hover:shadow-md ${theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'}`}>
                 <div className="flex justify-between items-start mb-2">
                   <span className={`text-xs font-bold px-2 py-0.5 rounded shadow-sm ${trade.type === 'BUY' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>{trade.type}</span>
                   <span className={`font-mono font-bold text-sm ${isProfit ? 'text-green-500' : 'text-red-500'}`}>{pnl > 0 ? '+' : ''}{pnl.toFixed(2)}</span>
                 </div>
                 <div className={`flex justify-between text-xs mb-3 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                   <span>{trade.quantity} Qty</span>
                   <span>@ {trade.entryPrice.toFixed(2)}</span>
                 </div>
                 <button onClick={() => closePosition(trade.id)} className={`w-full py-1.5 text-xs font-bold rounded-lg transition-colors ${theme === 'dark' ? 'bg-gray-700 hover:bg-gray-600 text-white' : 'bg-gray-100 hover:bg-gray-200 text-gray-600'}`}>Close Position</button>
               </div>
             )
          })}
          {trades.filter(t => t.status === 'OPEN').length === 0 && <div className="text-center text-xs opacity-50 mt-10">No active positions</div>}
        </div>
      </div>
    </div>
  );
};

export default OrderPanel;


