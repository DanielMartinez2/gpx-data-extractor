import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract waypoint data from GPX files into structured TXT files."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to a GPX file or a directory containing GPX files.",
    )

    parser.add_argument(
        "--output",
        default="output",
        help="Directory where TXT files will be created. Default: output",
    )

    return parser.parse_args()


def get_namespace(root):
    match = re.match(r"\{(.+)\}", root.tag)

    if match:
        return {"gpx": match.group(1)}

    return {"gpx": ""}


def clean_html(text):
    return re.sub(r"<[^>]+>", "", text).strip()


def extract_distance_and_angle(description):
    if not description:
        return "", ""

    cells = re.findall(
        r"<td[^>]*>(.*?)</td>",
        description,
        flags=re.IGNORECASE | re.DOTALL,
    )

    cells = [clean_html(cell) for cell in cells]

    distance = ""
    angle = ""

    for index, value in enumerate(cells):
        label = value.lower()

        if label == "distance" and index + 1 < len(cells):
            distance = cells[index + 1]

        if label == "angle" and index + 1 < len(cells):
            angle = cells[index + 1]

    # Fallback for GPX descriptions without explicit labels
    if not distance and len(cells) >= 2:
        distance = cells[1]

    if not angle and len(cells) >= 4:
        angle = cells[-1]

    return distance, angle


def extract_waypoints(gpx_file):
    tree = ET.parse(gpx_file)
    root = tree.getroot()

    namespace = get_namespace(root)

    waypoints = []

    for index, waypoint in enumerate(root.findall("gpx:wpt", namespace)):
        latitude = waypoint.attrib.get("lat", "")
        longitude = waypoint.attrib.get("lon", "")

        elevation = waypoint.findtext(
            "gpx:ele",
            default="",
            namespaces=namespace,
        )

        name = waypoint.findtext(
            "gpx:name",
            default="",
            namespaces=namespace,
        )

        description = waypoint.findtext(
            "gpx:desc",
            default="",
            namespaces=namespace,
        )

        distance, angle = extract_distance_and_angle(description)

        if index == 0:
            distance = "0"

        waypoints.append(
            {
                "latitude": latitude,
                "longitude": longitude,
                "elevation": elevation,
                "distance": distance,
                "name": name,
                "description": description,
                "angle": angle,
            }
        )

    return waypoints


def write_txt(waypoints, output_file):
    header = (
        "type\tlatitude\tlongitude\taltitude (m)\t"
        "distance (km)\tname\tdesc\tangle\n"
    )

    with output_file.open("w", encoding="utf-8") as file:
        file.write(header)

        for waypoint in waypoints:
            line = (
                f"W\t"
                f"{waypoint['latitude']}\t"
                f"{waypoint['longitude']}\t"
                f"{waypoint['elevation']}\t"
                f"{waypoint['distance']}\t"
                f"{waypoint['name']}\t"
                f"{waypoint['description']}\t"
                f"{waypoint['angle']}\n"
            )

            file.write(line)


def process_file(gpx_file, output_directory):
    waypoints = extract_waypoints(gpx_file)

    output_file = output_directory / f"{gpx_file.stem}.txt"

    write_txt(waypoints, output_file)

    print(
        f"Processed: {gpx_file.name} "
        f"-> {output_file} "
        f"({len(waypoints)} waypoints)"
    )


def main():
    args = parse_arguments()

    input_path = Path(args.input)
    output_directory = Path(args.output)

    if not input_path.exists():
        raise SystemExit(f"Input path not found: {input_path}")

    output_directory.mkdir(parents=True, exist_ok=True)

    if input_path.is_file():
        if input_path.suffix.lower() != ".gpx":
            raise SystemExit("The input file must have a .gpx extension.")

        gpx_files = [input_path]

    else:
        gpx_files = sorted(input_path.glob("*.gpx"))

    if not gpx_files:
        raise SystemExit("No GPX files found.")

    for gpx_file in gpx_files:
        process_file(gpx_file, output_directory)

    print(f"\nFinished. {len(gpx_files)} file(s) processed.")


if __name__ == "__main__":
    main()