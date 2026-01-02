def format_readings(feast):
    readings = feast["readings"]["readings"]
    reading_dict = {}
    for reading in readings:
        reading_dict[reading["readingType"]] = reading["acronyme"]
    return f"{feast['annualText']}:\n" + "\n".join(reading_dict.values())


def format_heading(feast):
    headings = (f"Tema: {feast['feastHeading']}", feast["otherName"])
    return "\n".join(filter(bool, headings))


def format_altar(feast):
    return (
        f"Den liturgiska färgen är {feast['liturgicalColorDisplay'].lower()}. "
        f"{feast['altar']['fullText']}."
    )


def format_church_year(feast):
    return "\n".join(
        (feast["churchYearPart"]["name"], feast["churchYearPart"]["description"])
    )


def format_description(feast):
    components = (
        format_heading(feast),
        feast["feastText"],
        format_readings(feast),
        format_altar(feast),
        format_church_year(feast),
    )
    return "\n\n".join(filter(bool, components))
