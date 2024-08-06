import React, { useState, useEffect, useRef } from 'react';

function AutocompleteInput({ value, onChange, onSelect, placeholder }) {
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const wrapperRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [wrapperRef]);

  useEffect(() => {
    if (value) {
      fetchSuggestions(value);
    } else {
      setSuggestions([]);
    }
  }, [value]);

  const fetchSuggestions = async (input) => {
    try {
      const response = await fetch(`http://localhost:5000/autocomplete?q=${input}`);
      const data = await response.json();
      setSuggestions(data);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  };

  return (
    <div ref={wrapperRef} className="relative">
      <input
        type="text"
        value={value}
        onChange={(e) => {
          onChange(e.target.value);
          setShowSuggestions(true);
        }}
        onFocus={() => setShowSuggestions(true)}
        className="w-full p-2 border rounded"
        placeholder={placeholder}
      />
      {showSuggestions && suggestions.length > 0 && (
        <ul className="absolute z-10 w-full bg-white border rounded mt-1 max-h-60 overflow-auto">
          {suggestions.map((item, index) => (
            <li
              key={index}
              onClick={() => {
                onSelect(item);
                setShowSuggestions(false);
              }}
              className="p-2 hover:bg-blue-100 cursor-pointer"
            >
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function WikipathFinder() {
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const findPath = async (algorithm) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('http://localhost:5000/find_path', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ start, end, algorithm }),
      });

      const data = await response.json();

      if (response.ok) {
        setResults({ ...data, algorithm });
      } else {
        setError(data.error || 'An error occurred');
      }
    } catch (error) {
      setError('Network error: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Wikipedia Path Finder</h1>
      <div className="mb-4">
        <label htmlFor="start" className="block mb-2">Start Page:</label>
        <AutocompleteInput
          value={start}
          onChange={setStart}
          onSelect={setStart}
          placeholder="Enter start page"
        />
      </div>
      <div className="mb-4">
        <label htmlFor="end" className="block mb-2">End Page:</label>
        <AutocompleteInput
          value={end}
          onChange={setEnd}
          onSelect={setEnd}
          placeholder="Enter end page"
        />
      </div>
      <div className="flex space-x-4 mb-4">
        <button
          onClick={() => findPath('bfs')}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          disabled={isLoading}
        >
          Find Path (BFS)
        </button>
        <button
          onClick={() => findPath('dijkstra')}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          disabled={isLoading}
        >
          Find Path (Dijkstra)
        </button>
      </div>
      {isLoading && <p className="text-gray-600">Searching...</p>}
      {error && <p className="text-red-500">{error}</p>}
      {results && (
        <div className="bg-gray-100 p-4 rounded">
          <h2 className="text-xl font-semibold mb-2">Results ({results.algorithm.toUpperCase()}):</h2>
          <p>Path: {results.path.join(' → ')}</p>
          <p>Visited: {results.visited} pages</p>
          <p>Time taken: {results.time_taken.toFixed(4)} seconds</p>
        </div>
      )}
    </div>
  );
}

export default WikipathFinder;