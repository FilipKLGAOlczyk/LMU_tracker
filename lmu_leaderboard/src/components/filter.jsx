const Filter = () => {
    return (
        <div className="filter">
            <label htmlFor="track">Track:</label>
            <select id="track" name="track">
                <option value="SPA">SPA</option>
                <option value="MONZA">MONZA</option>
            <option value="SILVERSTONE">SILVERSTONE</option>
        </select>

        <label htmlFor="car">Car:</label>
        <select id="car" name="car">
            <option value="car A">Car A</option>
            <option value="car B">Car B</option>
            <option value="car C">Car C</option>
        </select>
        
        <button type="submit">Filter</button>
    </div>
    )
}
export default Filter;