import './App.css';
import { useState } from 'react';
import playerData from '../../data/player_data.json';

import Leaderboard from './components/leaderboard.jsx';
import Filter from './components/filter.jsx';

const App =() => {
const [filter,setFilter] = useState({track: '', car: ''});

  const handleFilterChange = (newFilter) => {
    console.log('Filter changed:', newFilter);

    setFilter(prevFilter => ({
      ...prevFilter,
      ...newFilter
    }));
  }

  
 const filteredPlayers = playerData.player_data.filter(player => {
    console.log('Filtering player:', player, 'with filter:', filter);
    
        return (
            (filter.track ? player.track === filter.track : true) &&
            (filter.car ? player.car === filter.car : true)
        );
    });
  const sortedPlayers = [...filteredPlayers].sort((a, b) => {

    const timeToMs = (time) => {
      const [minutes, seconds, miliseconds] = time.split(':').map(Number);
      return (minutes * 60 + seconds) * 1000 + miliseconds;
    }
    return timeToMs(a.avg_five) - timeToMs(b.avg_five);
  });


  return (
    <div className="App">
      <div>
        <h1>LMU Leaderboard</h1>
        <p>This was made for Yoji CREW!</p>
      </div>
      <Filter filter={filter} onFilterChange={handleFilterChange} />
      <Leaderboard filteredPlayers={sortedPlayers} />
    </div>

  );
}

export default App;