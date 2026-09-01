import playerData from '../../../data/player_data.json';
const Leaderboard = () => {
  return (
    <div>
        <ul>
            <li>{playerData.player_data.name} {playerData.player_data.track} {playerData.player_data.car} {playerData.player_data.avg_five}</li>
        </ul>
    </div>
  );
}

export default Leaderboard;
