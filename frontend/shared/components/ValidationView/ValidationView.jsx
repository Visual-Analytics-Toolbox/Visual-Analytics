
import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';

const fetch_annotation_tasks = async () => {
    const token = await electronAPI.get_value("apiToken");
    // const response = await fetch(`https://vat.berlin-united.com/api/image-validation/`, {
    //     headers: {
    //         'Authorization': `Token ${token}`
    //     }
    const response = await fetch(`http://127.0.0.1:8000/api/image-validation/`, {
        headers: {
            'Authorization': `Token `
        }
    });
    console.log(response)
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}


const ValidationView = ({ }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const images = useQuery({
        queryKey: ['images'],
        queryFn: () => fetch_annotation_tasks(),
        staleTime: 5 * 60 * 1000, // Cache data for 5 minutes
        cacheTime: 5 * 60 * 1000,
    });

    const handleNext = () => {
        if (images.data?.images && currentIndex < images.data.images.length - 1) {
            setCurrentIndex(prev => prev + 1);
        }
    };

    const handlePrevious = () => {
        if (currentIndex > 0) {
            setCurrentIndex(prev => prev - 1);
        }
    };

    return (
        <div className="view-content">
            <div className="panel-header">
                <h3>Validation View</h3>
            </div>
            <div className="max-w-2xl mx-auto p-4">
                <div className=" rounded-lg shadow-lg overflow-hidden">
                    <div className="relative pb-[56.25%]"> {/* 16:9 aspect ratio */}
                        {images.isLoading ? (
                            <div className="absolute inset-0 bg-gray-200 flex items-center justify-center">
                                <span className="text-gray-500">Loading...</span>
                            </div>
                        ) : images.isError ? (
                            <div className="absolute inset-0 bg-gray-200 flex items-center justify-center">
                                <span className="text-gray-500">Error loading image</span>
                            </div>
                        ) : images.data?.images?.length > 0 ? (
                            <img
                                src={images.data.images[currentIndex]}
                                alt={`Validation content ${currentIndex + 1}`}
                                className="absolute inset-0 w-full h-full object-cover"
                            />
                        ) : (
                            <div className="absolute inset-0 bg-gray-200 flex items-center justify-center">
                                <span className="text-gray-500">No images available</span>
                            </div>
                        )}
                    </div>
                    {images.data?.images?.length > 0 && (
                        <div className="mt-4 flex justify-center gap-4 p-4">
                            <button
                                onClick={handlePrevious}
                                disabled={currentIndex === 0}
                                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed"
                            >
                                Previous
                            </button>
                            <span className="px-4 py-2 bg-gray-800 text-white rounded-lg">
                                {currentIndex + 1} / {images.data.images.length}
                            </span>
                            <button
                                onClick={handleNext}
                                disabled={currentIndex === images.data.images.length - 1}
                                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed"
                            >
                                Next
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ValidationView;