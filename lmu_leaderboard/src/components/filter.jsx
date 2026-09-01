import { useState } from 'react';
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

    return (
        <div className="filter">
            <form onSubmit={handleSubmit}>
                <label htmlFor="track">Track:</label>
                <select id="track" name="track" value={localFilter.track} onChange={handleChange}>
                    <option value="">All Tracks</option>
                    <option value="SPA">SPA</option>
                    <option value="MONZA">MONZA</option>
                <option value="SILVERSTONE">SILVERSTONE</option>
            </select>

            <label htmlFor="car">Car:</label>
            <select id="car" name="car" value={localFilter.car} onChange={handleChange}>
                <option value="">All Cars</option>
                <option value="car A">Car A</option>
                <option value="car B">Car B</option>
                <option value="car C">Car C</option>
            </select>
            
            <button type="submit">Filter</button>
        </form>
    </div>
    )
}
export default Filter;