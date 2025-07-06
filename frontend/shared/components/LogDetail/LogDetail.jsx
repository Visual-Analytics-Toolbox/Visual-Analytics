import React, { useCallback, useRef, useEffect } from 'react';
import { FixedSizeList as List } from "react-window";
import AutoSizer from 'react-virtualized-auto-sizer';
import styles from './LogDetail.module.css';


const FRAME_COUNT = 20000;
const ITEM_WIDTH = 100; // Approximate width of each button + margin/padding
const ITEM_HEIGHT = 40; // Height of each button

// Helper to generate frame data (in a real app, this might come from your video source)
const getFrameData = (count) => {
    return Array.from({ length: count }, (_, i) => ({
        id: `frame-${i}`,
        frameNumber: i + 1,
        // Add more frame-specific data if needed, e.g., timestamp, thumbnail URL
    }));
};

const frames = getFrameData(FRAME_COUNT);

// Individual Button Component
const FrameButton = React.memo(({ index, style, data }) => {
    const frame = data[index];
    const handleClick = () => {
        console.log(`Clicked Frame: ${frame.frameNumber}`);
        // In a real application, you would pass this frame number/id
        // to a parent component or a video player to seek to this frame.
        // e.g., onFrameSelect(frame.frameNumber);
    };

    return (
        <button
            className={styles.frame_button}
            style={{ ...style, width: ITEM_WIDTH - 8 }} // Adjust width for padding/margin
            onClick={handleClick}
            title={`Go to Frame ${frame.frameNumber}`}
        >
            {frame.frameNumber}
        </button>
    );
});

// Main Component
const FrameButtonList = () => {
    const listRef = useRef();

    // Example of how to programmatically scroll to a specific frame
    const scrollToFrame = useCallback((frameNumber) => {
        if (listRef.current) {
            // Subtract 1 because frames are 1-indexed, but array is 0-indexed
            listRef.current.scrollToItem(frameNumber - 1, 'center');
        }
    }, []);

    // Effect to demonstrate scrolling to a specific frame after initial render
    useEffect(() => {
        // You can call scrollToFrame(someFrameNumber) from a parent component
        // or based on some application logic.
        // For demonstration, let's scroll to frame 1000 after 1 second.
        const timeoutId = setTimeout(() => {
            // scrollToFrame(1000);
        }, 1000);
        return () => clearTimeout(timeoutId);
    }, [scrollToFrame]);


    return (
        <div className={styles.frame_button_list_container}>
            <h3>Video Frame Selector (20,000 Frames)</h3>
            <p>Scroll horizontally to select a frame.</p>
            <div className={styles.virtualized_list_wrapper}>
                <AutoSizer>
                    {({ height, width }) => (
                        <List
                            ref={listRef}
                            className={styles.frame_list_scrollbar} // For custom scrollbar styling
                            height={height} // Height of the list container, including scrollbar space
                            itemCount={frames.length}
                            itemSize={ITEM_WIDTH} // This is the width of each item in the list
                            width={width}
                            layout="horizontal"
                            itemData={frames}
                            initialScrollOffset={0} // Start at the beginning
                        >
                            {FrameButton}
                        </List>
                    )}
                </AutoSizer>
            </div>
            {/* Example controls for programmatically scrolling */}
            <div style={{ marginTop: '20px' }}>
                <button onClick={() => scrollToFrame(1)}>Scroll to Frame 1</button>
                <button onClick={() => scrollToFrame(1000)}>Scroll to Frame 1000</button>
                <button onClick={() => scrollToFrame(FRAME_COUNT)}>Scroll to Last Frame</button>
            </div>
        </div>
    );
};

export default FrameButtonList;