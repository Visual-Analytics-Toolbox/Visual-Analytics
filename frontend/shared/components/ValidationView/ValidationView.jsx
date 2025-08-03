
import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { getToken, getUrl } from '@shared/components/SettingsView/SettingsView';

const fetch_annotation_tasks = async () => {
    const token = await getToken();
    const url = await getUrl();
    const response = await fetch(`${url}/api/image-list/?include_annotations=1`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}


const ValidationView = ({ }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const images = useQuery({
        queryKey: ['results'],
        queryFn: () => fetch_annotation_tasks(),
        staleTime: 5 * 60 * 1000, // Cache data for 5 minutes
        cacheTime: 5 * 60 * 1000,
    });
    if (images.isError) {
        return <div>Error fetching images</div>;
    }

    if (images.isLoading) {
        return <div>Loading</div>;
    }

    console.log(images.data)
    const handleNext = () => {
        if (images.data.results && currentIndex < images.data.results.length - 1) {
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
                        <img
                            src={`https://logs.berlin-united.com/${images.data.results[currentIndex].image_url}`}
                            alt={`Validation content ${currentIndex + 1}`}
                            className="absolute inset-0 w-full h-full object-cover"
                        />
                    </div>

                    <div className="mt-4 flex justify-center gap-4 p-4">
                        <button
                            onClick={handlePrevious}
                            disabled={currentIndex === 0}
                            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed"
                        >
                            Previous
                        </button>
                        <span className="px-4 py-2 bg-gray-800 text-white rounded-lg">
                            {currentIndex + 1} / {images.data.results.length}
                        </span>
                        <button
                            onClick={handleNext}
                            disabled={currentIndex === images.data.results.length - 1}
                            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed"
                        >
                            Next
                        </button>
                    </div>
                    <div className="mt-4 flex justify-center gap-4 p-4">
                        <div className="w-full bg-gray-800 p-4 rounded-lg overflow-auto">
                            <pre className="text-white text-sm whitespace-pre-wrap">
                                {JSON.stringify(images.data.results[currentIndex].annotations, null, 2)}
                            </pre>
                        </div>
                    </div>


                </div>
            </div>
        </div>
    );
};

export default ValidationView;