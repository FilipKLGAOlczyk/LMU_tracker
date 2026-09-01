import Leaderboard from './components/leaderboard.jsx';
import Filter from './components/filter.jsx';

const App =() => {
const [filter,setFilter] = useState({track: '', car: ''});

  handleFilterChange = (filter) => {
    if (filter.track) {
      setFilter((prevFilter) => ({ ...prevFilter, track: filter.track }));
    }
    if (filter.car) {
      setFilter((prevFilter) => ({ ...prevFilter, car: filter.car }));
    }
  }

  return (
    <div>
      <div>
        <h1>LMU Leaderboard</h1>
        <p>Welcome to the LMU Leaderboard application!</p>
      </div>
      <Filter filter={filter} onFilterChange={handleFilterChange} />
      <Leaderboard />
    </div>

  );
}

export default App;