import { useNavigate } from "react-router-dom";

import styles from './EventCard.module.css';
import robocup_img from '@shared/assets/robocup.jpeg';
import { PenLine } from "lucide-react"
import { Button } from "@shared/components/ui/button"
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@shared/components/ui/dialog"
import { Input } from "@shared/components/ui/input"
import { Label } from "@shared/components/ui/label"

export const EventCard = ({ event }) => {
    const navigate = useNavigate();

    return (
        <div className={styles.event_card}>
            <div className={styles.event_header} onClick={() => navigate(`/events/${event.id}`)}>
                <img src={robocup_img} alt="RoboCup Image" />
            </div>
            <div className={styles.event_content}>
                <p className={styles.event_title}>
                    Event: {event.name}
                </p>
                <Dialog>
                    <DialogTrigger asChild>
                        <PenLine />
                    </DialogTrigger>
                    <DialogContent className={styles.dialog_content}>
                        <DialogHeader>
                            <DialogTitle>Update Event</DialogTitle>
                        </DialogHeader>

                        <div className={styles.form_group}>
                            <label htmlFor="name">Name:</label>
                            <input type="text" id="name" value="" />
                        </div>
                        <div className={styles.form_group}>
                            <label htmlFor="folder">Folder:</label>
                            <input type="text" id="folder" value="" />
                        </div>
                        <div className={styles.form_group}>
                            <label htmlFor="country">Country:</label>
                            <input type="text" id="country" value="" />
                        </div>
                        <DialogFooter className="sm:justify-start">
                            <DialogClose asChild>
                                <Button type="button" variant="secondary">
                                    Close
                                </Button>
                            </DialogClose>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>

            </div>
            <div className={styles.event_footer}>
                <progress className={styles.event_progressbar} value="40" max="100">40%</progress>
            </div>
        </div>
    );
};

export const CreateEventCard = () => {
    return (
        <div className={styles.event_card}>
            <div className={styles.event_header}>
                <img src={robocup_img} alt="RoboCup Image" />
            </div>
            <div className={styles.event_content}>
                <Dialog>
                    <DialogTrigger asChild>
                        <Button variant="outline">Share</Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-md">
                        <DialogHeader>
                            <DialogTitle>Share link</DialogTitle>
                            <DialogDescription>
                                Anyone who has this link will be able to view this.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="flex items-center gap-2">
                            <div className="grid flex-1 gap-2">
                                <Label htmlFor="link" className="sr-only">
                                    Link
                                </Label>
                                <Input
                                    id="link"
                                    defaultValue="https://ui.shadcn.com/docs/installation"
                                    readOnly
                                />
                            </div>
                        </div>
                        <DialogFooter className="sm:justify-start">
                            <DialogClose asChild>
                                <Button type="button" variant="secondary">
                                    Close
                                </Button>
                            </DialogClose>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>
            <div className={styles.event_footer}>
                <progress className={styles.event_progressbar} value="40" max="100">40%</progress>
            </div>
        </div>
    );
};
