import { useEffect, useRef, useState } from 'react';
import { createChart, ColorType } from 'lightweight-charts';
import type { ISeriesApi,UTCTimestamp } from 'lightweight-charts';
import { useGame } from '../../context/GameContext';

const ChartArea = () => {
  const { currentPrice, currentCandle, isPlaying, theme } = useGame();
  
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const seriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const chartRef = useRef<any | null>(null);
  const lastTimeRef = useRef<number>(0);

  // Initialize Chart
  useEffect(() => {
    if (!chartContainerRef.current) return;

    const isDark = theme === 'dark';
    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: 'transparent' }, 
        textColor: isDark ? '#9ca3af' : '#4b5563',
      },
      grid: {
        vertLines: { color: isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)' },
        horzLines: { color: isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)' },
      },
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
        borderColor: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
      },
    });

    chartRef.current = chart;

    const series = chart.addCandlestickSeries({
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderVisible: false,
      wickUpColor: '#26a69a',
      wickDownColor: '#ef5350',
    });

    seriesRef.current = series;

    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({ 
          width: chartContainerRef.current.clientWidth,
          height: chartContainerRef.current.clientHeight
        });
      }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, []);

  // Update Theme
  useEffect(() => {
    if (!chartRef.current) return;
    const isDark = theme === 'dark';
    chartRef.current.applyOptions({
      layout: { textColor: isDark ? '#9ca3af' : '#4b5563' },
      grid: {
        vertLines: { color: isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)' },
        horzLines: { color: isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)' },
      },
    });
  }, [theme]);

  // UPDATE CHART WITH REAL CANDLES
  useEffect(() => {
    if (!isPlaying || !seriesRef.current || !currentCandle) return;

    try {
      // 1. Check for Reset (Looping from 2024 back to 2015)
      if (currentCandle.time < lastTimeRef.current) {
         console.log("↺ Timeline Reset");
         seriesRef.current.setData([]); // Clear Chart
      }

      // 2. Plot the Candle
      // We explicitly cast to the Lightweight Charts Candle format
      const candle = {
         time: currentCandle.time as UTCTimestamp,
         open: currentCandle.open,
         high: currentCandle.high,
         low: currentCandle.low,
         close: currentCandle.close
      };

      seriesRef.current.update(candle);
      lastTimeRef.current = currentCandle.time;

    } catch (err) { 
        console.error("Chart Error:", err); 
    }
  }, [currentCandle, isPlaying]);

  return (
    <div className={`flex-1 flex flex-col min-h-0 min-w-0 h-full w-full font-sans transition-colors duration-500
      ${theme === 'dark' 
        ? 'bg-gray-900/40 backdrop-blur-sm' 
        : 'bg-white/40 backdrop-blur-sm'
      }`}>
      
      {/* HEADER */}
      <div className={`flex items-center justify-between px-4 py-3 border-b transition-colors
         ${theme === 'dark' ? 'border-gray-800' : 'border-gray-200'}`}>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
             <span className={`font-bold text-lg tracking-wide ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>NIFTY 50</span>
             <span className="bg-green-500/10 text-green-500 text-[10px] font-bold px-1.5 py-0.5 rounded border border-green-500/20">INDEX</span>
          </div>
        </div>
        <div className={`text-xl font-mono font-bold leading-none ${
             currentPrice >= (currentCandle?.open ?? 0) ? 'text-[#26a69a]' : 'text-[#ef5350]'
        }`}>
            {currentPrice.toFixed(2)}
        </div>
      </div>

      <div className="flex-1 relative w-full h-full">
         <div ref={chartContainerRef} className="absolute inset-0" />
      </div>
    </div>
  );
};

export default ChartArea;