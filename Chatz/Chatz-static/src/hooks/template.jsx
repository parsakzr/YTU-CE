import { useEffect, useState } from 'react';

const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

const useFetch = (url) => {
    useEffect(() => {
        fetch(url)
        .then((res) => res.json())
        .then((data) => {
            setData(data);
            setLoading(false);
        })
        .catch((error) => {
            setError(error);
            setLoading(false);
        });
    }, [url]);
    
    return { data, loading, error };
};

export default useFetch;