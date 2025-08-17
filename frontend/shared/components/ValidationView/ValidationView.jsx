
import { useQuery } from '@tanstack/react-query';
import React, { useState, useRef } from 'react';
import { getToken, getUrl } from '@shared/components/SettingsView/SettingsView';
import { Stage, Layer, Rect, Text } from 'react-konva';

const fetch_annotation_tasks = async () => {
    const token = await getToken();
    const url = await getUrl();
    const response = await fetch(`${url}/api/image-list/?annotation=true&validation=true`, {
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
    const [lines, setLines] = useState([]);
    const isDrawing = useRef(false);

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

    const handleMouseDown = (e) => {
        isDrawing.current = true;
        const pos = e.target.getStage().getPointerPosition();
        setLines([...lines, { points: [pos.x, pos.y], color: 'red', strokeWidth: 5 }]);
    };

    const handleMouseMove = (e) => {
        if (!isDrawing.current) {
            return;
        }
        const stage = e.target.getStage();
        const point = stage.getPointerPosition();
        let lastLine = lines[lines.length - 1];
        // add a new point to the current line
        lastLine.points = lastLine.points.concat([point.x, point.y]);

        // replace the last line with the updated one
        lines.splice(lines.length - 1, 1, lastLine);
        setLines([...lines]);
    };

    const handleMouseUp = () => {
        isDrawing.current = false;
    };

    return (
        <div className="view-content">
            <div className="panel-header">
                <h3>Validation View</h3>
            </div>
            <div className="max-w-2xl mx-auto p-4">
                <div className=" rounded-lg shadow-lg overflow-hidden">
                    <div style={{ position: 'relative', width: 640, height: 480 }}>
                        <img src={`https://logs.berlin-united.com/${images.data.results[currentIndex].image_url}`} alt="for annotation" style={{ display: 'block' }} />
                        <div style={{ position: 'absolute', top: 0, left: 0, 'width': '100%', 'height': '100%' }}>
                            <Stage
                                width={640}
                                height={480}
                                onMouseDown={handleMouseDown}
                                onMousemove={handleMouseMove}
                                onMouseup={handleMouseUp}
                            >
                                <Layer>
                                    {images.data.results[currentIndex].annotations.map((box) => (
                                        <React.Fragment key={box.id}>
                                            {/* Bounding Box */}
                                            <Rect
                                                x={box.data.x * 640}
                                                y={box.data.y * 480}
                                                width={box.data.width * 640}
                                                height={box.data.height * 480}
                                                stroke="yellow"
                                                strokeWidth={2}
                                                dash={[10, 5]} // Optional: makes the line dashed
                                            />
                                            {/* Label Text */}
                                            <Text
                                                x={box.x}
                                                y={box.y - 20} // Position the text slightly above the box
                                                text={box.label}
                                                fontSize={16}
                                                fill="yellow"
                                            />
                                        </React.Fragment>
                                    ))}
                                </Layer>
                            </Stage>
                        </div>

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