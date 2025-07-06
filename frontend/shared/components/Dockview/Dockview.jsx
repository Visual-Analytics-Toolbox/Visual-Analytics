import { DockviewReact } from "dockview";
import "dockview/dist/styles/dockview.css";
import React, { useState, useRef, useEffect } from "react";

const components = {
    default: (props) => {
        return (
            <div style={{ padding: "10px", color: "white" }}>
                Panel Content for: {props.api.title}
            </div>
        );
    },
};

export default function Dockview() {
    const [openPanels, setOpenPanels] = useState({});
    const dockviewApiRef = useRef(null);
    const [activeDropdown, setActiveDropdown] = useState(null); // State to track active dropdown
    const dropdownRefs = useRef({}); // Ref to store dropdown button/menu refs

    // Define your panel groups
    const panelGroups = [
        {
            id: "group1",
            label: "Group A Panels",
            panels: [
                { id: "panel_1", title: "Panel A1" },
                { id: "panel_2", title: "Panel A2" },
                { id: "panel_3", title: "Panel A3" },
            ],
        },
        {
            id: "group2",
            label: "Group B Panels",
            panels: [
                { id: "panel_4", title: "Panel B1" },
                { id: "panel_5", title: "Panel B2" },
            ],
        },
        {
            id: "group3",
            label: "Group C Panels",
            panels: [
                { id: "panel_6", title: "Panel C1" },
                { id: "panel_7", title: "Panel C2" },
                { id: "panel_8", title: "Panel C3" },
                { id: "panel_9", title: "Panel C4" },
            ],
        },
    ];

    const onReady = (event) => {
        dockviewApiRef.current = event.api;

        const initialPanels = {};

        const addPanelIfNotExist = (id, title) => {
            if (!event.api.getPanel(id)) {
                event.api.addPanel({
                    id: id,
                    component: "default",
                    title: title,
                });
                initialPanels[id] = true;
            }
        };

        // Add some initial panels from different groups for demonstration
        addPanelIfNotExist("panel_1", "Panel A1");
        addPanelIfNotExist("panel_4", "Panel B1");

        setOpenPanels(initialPanels);

        event.api.onDidRemovePanel((e) => {
            setOpenPanels((prev) => {
                const newState = { ...prev };
                delete newState[e.id];
                return newState;
            });
        });
    };

    const addPanelHandler = (panelId, panelTitle) => {
        if (dockviewApiRef.current) {
            if (!openPanels[panelId]) {
                dockviewApiRef.current.addPanel({
                    id: panelId,
                    component: "default",
                    title: panelTitle,
                });
                setOpenPanels((prev) => ({ ...prev, [panelId]: true }));
            } else {
                const panel = dockviewApiRef.current.getPanel(panelId);
                if (panel) {
                    panel.focus();
                }
            }
            setActiveDropdown(null); // Close dropdown after selection
        }
    };

    const toggleDropdown = (groupId) => {
        setActiveDropdown((prev) => (prev === groupId ? null : groupId));
    };

    // Effect for handling clicks outside the dropdown
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (activeDropdown && dropdownRefs.current[activeDropdown]) {
                const dropdownButton = dropdownRefs.current[activeDropdown].button;
                const dropdownMenu = dropdownRefs.current[activeDropdown].menu;

                if (
                    dropdownButton &&
                    !dropdownButton.contains(event.target) &&
                    dropdownMenu &&
                    !dropdownMenu.contains(event.target)
                ) {
                    setActiveDropdown(null);
                }
            }
        };

        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [activeDropdown]);

    return (
        <div
            className="App"
            style={{ display: "flex", flexDirection: "column", height: "100vh" }}
        >
            <div
                style={{
                    padding: "10px",
                    backgroundColor: "#333",
                    display: "flex",
                    gap: "10px",
                    marginBottom: "10px",
                    position: "relative", // Needed for dropdown positioning
                    zIndex: 10, // Ensure dropdown is above Dockview
                }}
            >
                {panelGroups.map((group) => (
                    <div
                        key={group.id}
                        style={{ position: "relative" }}
                        ref={(el) => {
                            // Store ref for the entire dropdown container
                            if (!dropdownRefs.current[group.id]) {
                                dropdownRefs.current[group.id] = {};
                            }
                            dropdownRefs.current[group.id].container = el;
                        }}
                    >
                        <button
                            onClick={() => toggleDropdown(group.id)}
                            ref={(el) => {
                                // Store ref for the button
                                if (!dropdownRefs.current[group.id]) {
                                    dropdownRefs.current[group.id] = {};
                                }
                                dropdownRefs.current[group.id].button = el;
                            }}
                            style={{
                                padding: "8px 15px",
                                backgroundColor: "#6c757d",
                                color: "white",
                                border: "none",
                                borderRadius: "4px",
                                cursor: "pointer",
                                whiteSpace: "nowrap",
                                display: "flex",
                                alignItems: "center",
                                gap: "5px",
                            }}
                        >
                            {group.label}
                            <span
                                style={{
                                    marginLeft: "5px",
                                    fontSize: "0.8em",
                                    transform:
                                        activeDropdown === group.id
                                            ? "rotate(180deg)"
                                            : "rotate(0deg)",
                                    transition: "transform 0.2s ease-in-out",
                                }}
                            >
                                &#9660; {/* Unicode down arrow */}
                            </span>
                        </button>
                        {activeDropdown === group.id && (
                            <div
                                ref={(el) => {
                                    // Store ref for the dropdown menu
                                    if (!dropdownRefs.current[group.id]) {
                                        dropdownRefs.current[group.id] = {};
                                    }
                                    dropdownRefs.current[group.id].menu = el;
                                }}
                                style={{
                                    position: "absolute",
                                    top: "100%", // Position below the button
                                    left: 0,
                                    backgroundColor: "#444",
                                    border: "1px solid #555",
                                    borderRadius: "4px",
                                    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
                                    marginTop: "5px",
                                    minWidth: "150px",
                                    zIndex: 20, // Ensure menu is above other dropdowns
                                }}
                            >
                                {group.panels.map((panel) => (
                                    <div
                                        key={panel.id}
                                        onClick={() => addPanelHandler(panel.id, panel.title)}
                                        style={{
                                            padding: "8px 15px",
                                            color: openPanels[panel.id] ? "#007bff" : "white", // Highlight if panel is open
                                            cursor: "pointer",
                                            "&:hover": {
                                                backgroundColor: "#555",
                                            },
                                        }}
                                    >
                                        {panel.title}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>
            <div style={{ flexGrow: 1 }}>
                <DockviewReact
                    className="dockview-theme-dark"
                    onReady={onReady}
                    components={components}
                />
            </div>
        </div>
    );
}