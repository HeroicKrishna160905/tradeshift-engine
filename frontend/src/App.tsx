import { GameProvider } from './context/GameContext';
import MainLayout from './components/layout/MainLayout';

/**
 * The Root Component
 * This is where the React application starts.
 */
export default function App() {
  return (
    // GameProvider wraps the entire app.
    // This ensures that ANY component inside MainLayout can access the game state.
    <GameProvider>
      <MainLayout />
    </GameProvider>
  );
}