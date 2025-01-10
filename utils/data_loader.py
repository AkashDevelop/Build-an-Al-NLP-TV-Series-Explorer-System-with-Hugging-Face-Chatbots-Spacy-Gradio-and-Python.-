from glob import glob
import pandas as pd

def load_subtitle_data(dataset_path):
    # Get all subtitle file paths from the directory
    subtitle_paths = glob("/content/drive/MyDrive/subtitles/*.ass")

    scripts = []
    episodes_num = []

    for path in subtitle_paths:
        with open(path, 'r') as file:  # Correctly using `path` instead of `files[0]`
            # Read all lines in the file
            lines = file.readlines()

            # Remove any metadata (first 27 lines are assumed to be metadata)
            lines = lines[27:]

            # Initialize an empty list to store the dialogue text
            dialogues = []

            # Process each line to extract the dialogue text
            for line in lines:
                # Split the line by the first 9 commas, the 10th part will be the dialogue text
                parts = line.split(",", 9)

                # Check if there's a dialogue part (the 10th part)
                if len(parts) > 9:
                    dialogues.append(parts[9])  # Append the dialogue text (10th part)

            # Clean up and remove any empty dialogues
            dialogues = [dialogue.strip() for dialogue in dialogues if dialogue.strip()]

            # Remove `\N` in the text and join all dialogues into a single script
            dialogues = [dialogue.replace("\\N", " ") for dialogue in dialogues]
            script = " ".join(dialogues)

            # Extract the episode number from the file name
            # Assume the episode number is in the format `...-<episode_number>.ass`
            try:
                episode = int(path.split("-")[-1].split('.')[0].strip())
            except ValueError:
                episode = -1  # If extraction fails, set to -1 as a fallback

            # Append data to the lists
            scripts.append(script)
            episodes_num.append(episode)

    # Create a DataFrame from the collected data
    df = pd.DataFrame({"episode": episodes_num, "script": scripts})

    # Sort the DataFrame by the episode number
    df = df[df["episode"] > 0]  # Remove any entries with invalid episode numbers
    df = df.sort_values(by="episode").reset_index(drop=True)

    return df
