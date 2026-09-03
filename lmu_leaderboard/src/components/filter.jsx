import { useState } from 'react';
import playerData from '../../../data/player_data.json';
const Filter = ({ filter, onFilterChange }) => {

    const [localFilter, setLocalFilter] = useState({ track: '', car: '' });
    const handleChange = (e) => {
        const { name, value } = e.target;
        setLocalFilter(prev => ({ ...prev, [name]: value }));
    }
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Filter submitted:', localFilter);
        onFilterChange(localFilter);
    }

    const getUnique = (option) => {
        const options = new Set();
        playerData.player_data.forEach(player => {
            options.add(player[option]);
        });
        return Array.from(options);
    }
    
    
            

    return (
        <div className="filter">
            <form onSubmit={handleSubmit}>
                <label htmlFor="track">Track:</label>
                <select id="track" name="track" value={localFilter.track} onChange={handleChange}>
                    <option value="">All Tracks</option>
                    {getUnique('track').map(track => (
                        <option key={track} value={track}>{track}</option>
                    ))}
                </select>

            <label htmlFor="car">Car:</label>
            <select id="car" name="car" value={localFilter.car} onChange={handleChange}>
                <option value="">All Cars</option>
                {getUnique('car').map(car => (
                    <option key={car} value={car}>{car}</option>
                ))}
            </select>
            
            <button type="submit">Filter</button>
        </form>
    </div>
    )
}
export default Filter;