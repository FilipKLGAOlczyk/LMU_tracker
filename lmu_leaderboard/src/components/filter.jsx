import { useState, useMemo } from 'react';
const Filter = ({ filter, onFilterChange, players }) => {

    const [localFilter, setLocalFilter] = useState({ track: '', class: '', car: '' });
    const handleChange = (e) => {
        const { name, value } = e.target;
        setLocalFilter(prev => ({ ...prev, [name]: value }));
    }
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Filter submitted:', localFilter);
        onFilterChange(localFilter);
    }

   const uniqueTracks = useMemo(() => [...new Set(players.map(p => p.track).filter(Boolean))], [players]);
   const uniqueClasses = useMemo(() => [...new Set(players.map(p => p.class).filter(Boolean))], [players]);
   const uniqueCars = useMemo(() => [...new Set(players.map(p => p.car).filter(Boolean))], [players]);


    return (
        <div className="filter">
            <form onSubmit={handleSubmit}>

                <label htmlFor="track">Track:</label>
                <select id="track" name="track" value={localFilter.track} onChange={handleChange}>
                    <option value="">All Tracks</option>
                    {uniqueTracks.map(track => (
                        <option key={track} value={track}>{track}</option>
                    ))}
                </select>

                <label htmlFor="class">Class:</label>
                <select id="class" name="class" value={localFilter.class} onChange={handleChange}>
                    <option value="">All Classes</option>
                    {uniqueClasses.map(cls => (
                        <option key={cls} value={cls}>{cls}</option>
                    ))}
                </select>
            

                <label htmlFor="car">Car:</label>
                <select id="car" name="car" value={localFilter.car} onChange={handleChange}>
                    <option value="">All Cars</option>
                    {uniqueCars.map(car => (
                        <option key={car} value={car}>{car}</option>
                    ))}
                </select>
                
                <button type="submit">Filter</button>
            </form>
        </div>
    )
}
export default Filter;