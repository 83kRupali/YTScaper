import json
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

JSON_DIR = Path("transcripts")
CHUNK_DIR = Path("chunks1")

CHUNK_DURATION = 75


CHUNK_DIR.mkdir(
    exist_ok=True
)


# ============================================================
# TIME FORMAT
# ============================================================

def format_timestamp(seconds):

    seconds = int(seconds)

    hours = seconds // 3600

    minutes = (seconds % 3600) // 60

    secs = seconds % 60

    if hours > 0:

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{secs:02d}"
        )

    return (
        f"{minutes:02d}:"
        f"{secs:02d}"
    )


# ============================================================
# CREATE CHUNKS
# ============================================================

def create_chunks(video):

    segments = video["segments"]

    if not segments:
        return []


    chunks = []

    current_segments = []

    chunk_start = segments[0]["start"]


    for segment in segments:

        segment_start = segment["start"]


        # ----------------------------------------------------
        # Check chunk duration
        # ----------------------------------------------------

        if (
            segment_start - chunk_start
            >= CHUNK_DURATION
            and current_segments
        ):

            chunks.append(
                build_chunk(
                    video,
                    current_segments
                )
            )

            current_segments = []

            chunk_start = segment_start


        current_segments.append(
            segment
        )


    # --------------------------------------------------------
    # Add final chunk
    # --------------------------------------------------------

    if current_segments:

        chunks.append(
            build_chunk(
                video,
                current_segments
            )
        )


    return chunks


# ============================================================
# BUILD ONE CHUNK
# ============================================================

def build_chunk(
    video,
    segments
):

    start = segments[0]["start"]


    # End = start of next segment if available.
    # Otherwise use video duration.

    if len(segments) > 1:

        end = segments[-1]["start"]

    else:

        end = (
            start + 1
        )


    text_parts = []


    for segment in segments:

        text = segment["text"].strip()

        if text:

            text_parts.append(
                text
            )


    text = " ".join(
        text_parts
    )


    return {

        "chunk_id": None,

        "video_id":
            video["video_id"],

        "title":
            video["title"],

        "language":
            video["language"],

        "video_url":
            (
                "https://www.youtube.com/watch?v="
                + video["video_id"]
            ),

        "start":
            start,

        "end":
            end,

        "timestamp":
            format_timestamp(start),

        "text":
            text
    }


# ============================================================
# PROCESS JSON FILE
# ============================================================

def process_file(
    json_file
):

    print(
        f"\nProcessing: "
        f"{json_file.name}"
    )


    with open(
        json_file,
        "r",
        encoding="utf-8"
    ) as file:

        video = json.load(file)


    chunks = create_chunks(
        video
    )


    # --------------------------------------------------------
    # Add unique chunk IDs
    # --------------------------------------------------------

    for index, chunk in enumerate(
        chunks
    ):

        chunk["chunk_id"] = (
            f"{chunk['video_id']}_"
            f"chunk_{index + 1}"
        )


    # --------------------------------------------------------
    # Save chunks
    # --------------------------------------------------------

    output = {

        "video_id":
            video["video_id"],

        "title":
            video["title"],

        "language":
            video["language"],

        "duration":
            video["duration"],

        "total_chunks":
            len(chunks),

        "chunks":
            chunks
    }


    output_file = (
        CHUNK_DIR
        / f"{json_file.stem}_chunks.json"
    )


    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            ensure_ascii=False,
            indent=2
        )


    print(
        f"✅ Created "
        f"{len(chunks)} chunks"
    )

    print(
        f"📄 Saved: "
        f"{output_file}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n===================================="
    )

    print(
        "JSON → CHUNKING"
    )

    print(
        "===================================="
    )


    json_files = sorted(
        JSON_DIR.glob("*.json")
    )


    print(
        f"JSON files found: "
        f"{len(json_files)}"
    )


    for json_file in json_files:

        process_file(
            json_file
        )


    print(
        "\n===================================="
    )

    print(
        "🎉 CHUNKING COMPLETED"
    )

    print(
        "===================================="
    )


if __name__ == "__main__":

    main()






    