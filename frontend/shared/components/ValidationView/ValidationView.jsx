
import { useQuery } from '@tanstack/react-query';
import React, { useState, useRef, useEffect } from 'react';
import { getToken, getUrl } from '@shared/components/SettingsView/SettingsView';
import { Stage, Layer, Rect, Transformer, Image as KonvaImage } from 'react-konva';
import styles from './ValidationView.module.css';

const fetch_annotation_tasks = async ({ currentOffset }) => {
    const token = await getToken();
    const url = await getUrl();

    const response = await fetch(`${url}/api/image-list/?limit=8&annotation=true&validated=false&offset=${currentOffset}`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

const URLImage = ({ src, x, y, width, height }) => {
    const [image, setImage] = useState(null);

    useEffect(() => {
        const img = new window.Image();
        img.src = src;

        img.onload = () => {
            setImage(img);
        };
    }, [src]);

    return (
        <KonvaImage
            image={image}
            x={x}
            y={y}
            width={width}
            height={height}
        />
    );
};

const ValidationView = ({ }) => {
    const [currentOffset, setCurrentOffset] = useState(0);
    const [selectedIds, setSelectedIds] = useState({}); // { [imageId]: boxId }
    const transformerRefs = useRef({}); // { [imageId]: transformerRef }

    const {
        data,
        error,
        isLoading,
        isFetching,
        isPreviousData,
    } = useQuery({
        queryKey: ['results', currentOffset], // The offset is part of the query key
        queryFn: () => fetch_annotation_tasks({ currentOffset }),
        keepPreviousData: true, // Optional: keeps old data visible while fetching new data
    });

    const handleBoxClick = (e) => {
        const shape = e.target;
        console.log("handleBoxClick", shape)

    };

    const handleStageClick = (e) => {
        //const shape = e.target;
        console.log("clicked on stage", e)
    };

    useEffect(() => {
        Object.entries(selectedIds).forEach(([imageId, boxId]) => {
            const transformer = transformerRefs.current[imageId];
            if (!transformer) return;

            if (boxId) {
                const stage = transformer.getStage();
                const selectedNode = stage.findOne('.' + boxId);
                if (selectedNode) {
                    transformer.nodes([selectedNode]);
                    transformer.getLayer().batchDraw();
                }
            } else {
                transformer.nodes([]);
                transformer.getLayer().batchDraw();
            }
        });
    }, [selectedIds]);

    if (error) {
        return <div>Error fetching images</div>;
    }

    if (isLoading) {
        return <div>Loading</div>;
    }

    console.log(data)



    const handleNextPage = () => {
        // Assuming the API response provides the next offset.
        // In this example, we'll parse it from the 'next' URL.
        if (data?.next) {
            const url = new URL(data.next);
            const nextOffset = url.searchParams.get("offset");
            if (nextOffset !== null) {
                setCurrentOffset(parseInt(nextOffset, 10));
            }
        }
    };

    // You'll need a similar function for "Previous" as well.
    const handlePreviousPage = () => {
        if (data?.previous) {
            const url = new URL(data.previous);
            const prevOffset = url.searchParams.get("offset");
            if (prevOffset !== null) {
                setCurrentOffset(parseInt(prevOffset, 10));
            } else {
                // Handle the case where there is no 'previous' link (e.g., set to 0)
                setCurrentOffset(0);
            }
        }
    };

    return (
        <div className="view-content">
            <div className="panel-header">
                <h3>Validation View</h3>
            </div>

            <div className={styles.image_grid}>
                {data.results.map((image, i) => (
                    <div className={styles.konva_overlay} key={i}>
                        <Stage
                            width={640}
                            height={480}
                            onClick={handleStageClick}
                            onTap={handleStageClick}
                        >
                            <Layer>
                                <URLImage
                                    src={`https://logs.berlin-united.com/${image.image_url}`}
                                    x={0}
                                    y={0}
                                    width={640}
                                    height={480}
                                />
                                {/* FIXME handle the case that annotations is empty */}
                                {image.annotations.map((box) => (
                                    <Rect
                                        className={box.id}
                                        key={box.id}
                                        x={box.data.x * 640}
                                        y={box.data.y * 480}
                                        width={box.data.width * 640}
                                        height={box.data.height * 480}
                                        stroke="000"
                                        opacity={0.5}
                                        strokeWidth={2}
                                        validated={box.validated}
                                        color={box.color}
                                        fill={box.validated == true ? "green" : box.color}
                                        dash={[10, 5]} // Optional: makes the line dashed
                                        draggable
                                    />

                                ))}
                                <Transformer
                                    ref={ref => transformerRefs.current[image.id] = ref}
                                    rotateEnabled={false}
                                    flipEnabled={false}
                                    anchorStroke="000"
                                    anchorFill="white"
                                    keepRatio={false}
                                    ignoreStroke={true}
                                    borderStrokeWidth={0}
                                    enabledAnchors={[
                                        "top-left",
                                        "top-right",
                                        "bottom-left",
                                        "bottom-right",
                                    ]}
                                    anchorCornerRadius={10}
                                />
                            </Layer>
                        </Stage>
                    </div>

                ))}
            </div>
            <div>
                <button onClick={handlePreviousPage} disabled={!data.previous}>
                    Previous
                </button>
                <button onClick={handleNextPage} disabled={!data.next}>
                    Next
                </button>
                {isFetching && <span>Fetching...</span>}
            </div>
        </div>
    );
};

export default ValidationView;