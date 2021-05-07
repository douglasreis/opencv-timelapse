import os
import sys
import cv2
import time
import datetime
from pathlib import Path
from config import config


def fade_in_frames(img1, img2, numFrames):
    transition_frames = []
    for IN in range(0, numFrames):
        fadein = IN/float(numFrames)
        transition_img = cv2.addWeighted(img1, 1-fadein, img2, fadein, 0)
        transition_frames.append(transition_img)
    return transition_frames


def get_image_files(dir, fileExt="*", ordered=True):
    image_files = []
    if os.path.exists(dir):
        image_list = Path(dir).rglob(f"*.{fileExt}")
        if ordered:
            # key needs an specific lambda to deal with the order of months 1 & 10 for instance
            image_files = sorted(image_list, key=lambda x: (
                int(str(x).split('/')[-1].split('_')[4].split('.')[0])))
        else:
            image_files = image_list
    return image_files


def get_frames_for_video(timelapse_images, numFramesTransition):
    src_frames = []
    frames_with_transitions = []

    for i, tlImage in enumerate(timelapse_images):
        img = cv2.imread(str(tlImage))
        width = img.shape[0]
        height = img.shape[1]
        print(f"filename: {str(tlImage)}, height: {height}, width: {width}")

        if len(src_frames) > 0 and i < len(timelapse_images) - 1:
            frames_with_transitions.extend(fade_in_frames(
                src_frames[-1], img, numFramesTransition))

        src_frames.append(img)
        frames_with_transitions.append(img)

    return frames_with_transitions


def generate_timelapse_video(timelapse_images, height, width, outputFilename, fps=10, numFramesTransition=3):
    fourcc = cv2.VideoWriter_fourcc(*"MP4V")
    writer = cv2.VideoWriter(outputFilename, fourcc, fps, (height, width))

    for frame in get_frames_for_video(timelapse_images, numFramesTransition):
        writer.write(frame)
    writer.release()


def process_timelapse_video(basePath, dateToProcess=datetime.datetime.now(), hourly=False):
    date_pattern = f"{dateToProcess.year}##{dateToProcess.month}##{dateToProcess.day}"
    if hourly:
        date_pattern = f"{date_pattern}##{dateToProcess.hour}"
    image_dir = f"{basePath}/{date_pattern.replace('##', '/')}"

    video_filename = f"tl_{date_pattern.replace('##', '_')}.mp4"
    timelapse_images = get_image_files(image_dir, "jpg")
    if len(timelapse_images) > 0:
        print(f"Generating '{video_filename}' in '{image_dir}'")
        generate_timelapse_video(
            timelapse_images, 2048, 1536, video_filename)
    else:
        print("No images to generate video")


def run_loop(basePath, pause, config):
    runHour = config["runHour"]

    print(f"Pause : {pause} hours")

    while True:
        current_datetime = datetime.datetime.now()

        if current_datetime.hour == runHour:
            process_timelapse_video(basePath)
        else:
            print(f"Timelapse video generator will run at next {runHour} hour")

        if runHour != 0:
            hours_added = datetime.timedelta(hours=pause)
            print(
                f"Timelapse video generator paused until {datetime.datetime.now() + hours_added}")
            time.sleep(pause*60*24)


if(__name__ == '__main__'):
    if len(sys.argv) < 1:
        exit()
    else:
        try:
            pause_interval = int(sys.argv[1])
            basePath = config["basePath"]
            run_loop(basePath, pause_interval, config)
        except KeyboardInterrupt:
            print("Cancelling timelapse.py")
