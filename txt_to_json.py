import re
import json
import csv
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

DATA_DIR = Path("data")

OUTPUT_DIR = Path("json_data")

METADATA_FILE = Path("video.csv")


OUTPUT_DIR.mkdir(
    exist_ok=True
)


# ============================================================
# TIME CONVERSION
# ============================================================

def timestamp_to_seconds(timestamp):

    parts = timestamp.split(":")

    if len(parts) == 2:

        minutes = int(parts[0])

        seconds = int(parts[1])

        return (
            minutes * 60
            + seconds
        )


    if len(parts) == 3:

        hours = int(parts[0])

        minutes = int(parts[1])

        seconds = int(parts[2])

        return (
            hours * 3600
            + minutes * 60
            + seconds
        )


    raise ValueError(
        f"Invalid timestamp: {timestamp}"
    )


# ============================================================
# READ TXT
# ============================================================

def parse_txt(file_path):

    segments = []


    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()


    # Example:
    #
    # [01:20] Hello everyone
    #
    pattern = re.compile(
        r"^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.*)$"
    )


    for line in lines:

        line = line.strip()


        if not line:

            continue


        match = pattern.match(line)


        if not match:

            print(
                f"⚠️ Skipping invalid line "
                f"in {file_path.name}:"
            )

            print(line)

            continue


        timestamp = match.group(1)

        text = match.group(2).strip()


        if not text:

            continue


        start = timestamp_to_seconds(
            timestamp
        )


        segments.append({

            "start": start,

            "timestamp": timestamp,

            "text": text
        })


    return segments


# ============================================================
# LOAD CSV METADATA
# ============================================================

def load_metadata():

    metadata = {}


    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)


        for row in reader:

            filename = row[
                "filename"
            ].strip()


            metadata[filename] = {

                "video_id":
                    row["video_id"].strip(),

                "title":
                    row["title"].strip(),

                "language":
                    row["language"].strip()
            }


    return metadata


# ============================================================
# CONVERT ONE FILE
# ============================================================

def convert_file(
    txt_file,
    metadata
):

    filename = txt_file.name


    if filename not in metadata:

        print(
            f"⚠️ Metadata not found "
            f"for {filename}"
        )

        return


    info = metadata[
        filename
    ]


    segments = parse_txt(
        txt_file
    )


    if not segments:

        print(
            f"⚠️ No segments found "
            f"in {filename}"
        )

        return


    # --------------------------------------------------------
    # Calculate duration
    # --------------------------------------------------------

    duration = segments[-1]["start"]


    # --------------------------------------------------------
    # Create JSON
    # --------------------------------------------------------

    result = {

        "video_id":
            info["video_id"],

        "title":
            info["title"],

        "language":
            info["language"],

        "model":
            "unknown",

        "duration":
            duration,

        "segments":
            segments
    }


    output_file = (
        OUTPUT_DIR
        / f"{txt_file.stem}.json"
    )


    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            ensure_ascii=False,
            indent=2
        )


    print(
        f"✅ {filename} "
        f"→ {output_file.name} "
        f"({len(segments)} segments)"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n===================================="
    )

    print(
        "TXT → JSON CONVERTER"
    )

    print(
        "====================================\n"
    )


    metadata = load_metadata()


    txt_files = sorted(
        DATA_DIR.glob("*.txt")
    )


    print(
        f"Found TXT files: "
        f"{len(txt_files)}"
    )


    for txt_file in txt_files:

        convert_file(
            txt_file,
            metadata
        )


    print(
        "\n===================================="
    )

    print(
        "🎉 CONVERSION COMPLETED"
    )

    print(
        "===================================="
    )


if __name__ == "__main__":

    main()