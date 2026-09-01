
const Leaderboard = ({ filteredPlayers }) => {


  return (
    <div>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Track</th>
                    <th>Car</th>
                    <th>Average Five Laps Time</th>
                </tr>
            </thead>
            <tbody>
                {filteredPlayers.map(player => (
                    <tr key={player.id}>
                        <td>{player.name}</td>
                        <td>{player.track}</td>
                        <td>{player.car}</td>
                        <td>{player.avg_five}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
  );
}

export default Leaderboard;
